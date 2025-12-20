"""
HIVEMIND Router

Intelligent task routing to teams and agents based on keyword matching
and capability analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from hivemind.agents.base import Agent
from hivemind.agents.teams import Team, TeamID, TEAM_CONFIGS
from hivemind.config import get_settings
from hivemind.observability.logging import LoggerMixin
from hivemind.observability.metrics import get_metrics

if TYPE_CHECKING:
    from hivemind.agents.pool import AgentPool


@dataclass
class RoutingScore:
    """Score for a routing candidate."""
    team: Team
    agent: Agent | None
    score: float
    matched_keywords: list[str] = field(default_factory=list)

    def __lt__(self, other: RoutingScore) -> bool:
        """Compare routing scores."""
        return self.score < other.score


class Router(LoggerMixin):
    """
    Router for directing tasks to appropriate teams and agents.

    Uses keyword-based matching to route tasks to the most suitable
    teams and agents based on their capabilities and specializations.

    Supports:
    - Single-team routing (most tasks)
    - Multi-team routing (complex tasks requiring multiple specializations)
    - Agent-level routing within teams
    - Fallback routing when no good match is found
    """

    def __init__(
        self,
        teams: dict[TeamID, Team] | None = None,
        agent_pool: AgentPool | None = None,
        multi_team_threshold: float = 0.7,
        min_match_score: float = 0.3,
    ) -> None:
        """
        Initialize the Router.

        Args:
            teams: Dictionary of teams by TeamID
            agent_pool: Optional agent pool for accessing all agents
            multi_team_threshold: Score threshold for multi-team routing (0.0-1.0)
            min_match_score: Minimum score for a valid match (0.0-1.0)
        """
        self.teams = teams or {}
        self.agent_pool = agent_pool
        self.multi_team_threshold = multi_team_threshold
        self.min_match_score = min_match_score

        self._metrics = get_metrics()

        self.logger.info(
            "Router initialized",
            team_count=len(self.teams),
            multi_team_threshold=multi_team_threshold,
            min_match_score=min_match_score,
        )

    def extract_keywords(self, prompt: str) -> list[str]:
        """
        Extract keywords from a prompt.

        Args:
            prompt: The task prompt

        Returns:
            List of extracted keywords
        """
        # Convert to lowercase and split
        words = prompt.lower().split()

        # Filter out common stop words
        stop_words = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "should",
            "could", "may", "might", "can", "must", "i", "you", "he", "she", "it",
            "we", "they", "what", "which", "who", "when", "where", "why", "how",
            "this", "that", "these", "those", "to", "from", "in", "on", "at", "by",
            "for", "with", "about", "as", "of", "and", "or", "but", "not", "if",
            "then", "so", "because", "while", "there", "here", "just", "now", "some",
        }

        # Extract significant words (length > 2, not stop words)
        keywords = []
        for word in words:
            cleaned = word.strip(".,;:!?()[]{}\"'")
            if len(cleaned) > 2 and cleaned not in stop_words:
                keywords.append(cleaned)

        return keywords

    def match_keywords(
        self,
        task_keywords: list[str],
        target_keywords: list[str],
    ) -> tuple[float, list[str]]:
        """
        Match task keywords against target keywords.

        Args:
            task_keywords: Keywords from the task
            target_keywords: Keywords from team/agent

        Returns:
            Tuple of (match_score, matched_keywords)
        """
        if not task_keywords or not target_keywords:
            return 0.0, []

        # Convert to lowercase sets for case-insensitive matching
        task_set = {kw.lower() for kw in task_keywords}
        target_set = {kw.lower() for kw in target_keywords}

        # Find intersection
        matched = task_set & target_set

        if not matched:
            return 0.0, []

        # Calculate score based on match ratio
        # Score considers both coverage of task keywords and target keywords
        task_coverage = len(matched) / len(task_set)
        target_coverage = len(matched) / len(target_set)

        # Use harmonic mean to balance both coverages
        score = 2 * (task_coverage * target_coverage) / (task_coverage + target_coverage)

        return score, list(matched)

    def score_team(self, task_keywords: list[str], team: Team) -> RoutingScore:
        """
        Score how well a team matches the task keywords.

        Args:
            task_keywords: Keywords from the task
            team: Team to score

        Returns:
            RoutingScore for the team
        """
        team_keywords = team.config.keywords
        score, matched = self.match_keywords(task_keywords, team_keywords)

        return RoutingScore(
            team=team,
            agent=None,
            score=score,
            matched_keywords=matched,
        )

    def score_agent(
        self,
        task_keywords: list[str],
        agent: Agent,
        team: Team,
    ) -> RoutingScore:
        """
        Score how well an agent matches the task keywords.

        Args:
            task_keywords: Keywords from the task
            agent: Agent to score
            team: Team the agent belongs to

        Returns:
            RoutingScore for the agent
        """
        agent_keywords = agent.metadata.keywords
        score, matched = self.match_keywords(task_keywords, agent_keywords)

        return RoutingScore(
            team=team,
            agent=agent,
            score=score,
            matched_keywords=matched,
        )

    def route_to_teams(self, keywords: list[str]) -> list[RoutingScore]:
        """
        Route keywords to the most appropriate teams.

        Args:
            keywords: Task keywords

        Returns:
            List of RoutingScore objects, sorted by score descending
        """
        scores = []

        for team in self.teams.values():
            score = self.score_team(keywords, team)
            if score.score >= self.min_match_score:
                scores.append(score)

        # Sort by score descending
        scores.sort(reverse=True)

        self.logger.debug(
            "Teams scored",
            keyword_count=len(keywords),
            team_scores=[(s.team.id.value, s.score) for s in scores[:3]],
        )

        return scores

    def route_to_agents(
        self,
        keywords: list[str],
        team: Team,
    ) -> list[RoutingScore]:
        """
        Route keywords to the most appropriate agents within a team.

        Args:
            keywords: Task keywords
            team: Team to search within

        Returns:
            List of RoutingScore objects, sorted by score descending
        """
        scores = []

        for agent in team.agents:
            if not agent.is_available:
                continue

            score = self.score_agent(keywords, agent, team)
            if score.score >= self.min_match_score:
                scores.append(score)

        # Sort by score descending
        scores.sort(reverse=True)

        self.logger.debug(
            "Agents scored",
            team=team.id.value,
            keyword_count=len(keywords),
            agent_scores=[(s.agent.id if s.agent else None, s.score) for s in scores[:3]],
        )

        return scores

    def route(
        self,
        keywords: list[str] | str,
        max_teams: int = 3,
        max_agents_per_team: int = 2,
    ) -> list[tuple[Team | None, Agent | None]]:
        """
        Route a task to appropriate teams and agents.

        Args:
            keywords: Task keywords (list or string)
            max_teams: Maximum number of teams to route to
            max_agents_per_team: Maximum agents per team

        Returns:
            List of (team, agent) tuples for execution
        """
        # Extract keywords if string provided
        if isinstance(keywords, str):
            keywords = self.extract_keywords(keywords)

        self.logger.info(
            "Routing task",
            keywords=keywords,
            max_teams=max_teams,
            max_agents_per_team=max_agents_per_team,
        )

        # Score all teams
        team_scores = self.route_to_teams(keywords)

        if not team_scores:
            self.logger.warning("No teams matched keywords", keywords=keywords)
            return []

        # Determine if we need multi-team routing
        routes = []

        # If top team has very high score, single-team routing
        if team_scores[0].score >= self.multi_team_threshold:
            selected_teams = team_scores[:1]
        else:
            # Multi-team routing - include teams with good scores
            selected_teams = [
                s for s in team_scores[:max_teams]
                if s.score >= self.min_match_score
            ]

        # For each selected team, find best agents
        for team_score in selected_teams:
            team = team_score.team

            # Score agents in this team
            agent_scores = self.route_to_agents(keywords, team)

            if not agent_scores:
                # No available agents, fallback to any available agent
                available = team.available_agents
                if available:
                    routes.append((team, available[0]))
                    self.logger.info(
                        "Using fallback agent",
                        team=team.id.value,
                        agent=available[0].id,
                    )
                else:
                    self.logger.warning(
                        "No available agents in team",
                        team=team.id.value,
                    )
                continue

            # Add best matching agents
            for agent_score in agent_scores[:max_agents_per_team]:
                if agent_score.agent:
                    routes.append((team, agent_score.agent))

        self.logger.info(
            "Routing complete",
            route_count=len(routes),
            routes=[
                (t.id.value, a.id if a else None)
                for t, a in routes
            ],
        )

        return routes

    def get_best_match(
        self,
        keywords: list[str] | str,
    ) -> tuple[Team | None, Agent | None]:
        """
        Get the single best match for keywords.

        Args:
            keywords: Task keywords

        Returns:
            Tuple of (team, agent) for the best match
        """
        routes = self.route(keywords, max_teams=1, max_agents_per_team=1)

        if not routes:
            return None, None

        return routes[0]

    def can_route(self, keywords: list[str] | str) -> bool:
        """
        Check if the router can find a route for the given keywords.

        Args:
            keywords: Task keywords

        Returns:
            True if at least one route can be found
        """
        if isinstance(keywords, str):
            keywords = self.extract_keywords(keywords)

        team_scores = self.route_to_teams(keywords)
        return len(team_scores) > 0

    def get_routing_summary(
        self,
        keywords: list[str] | str,
    ) -> dict[str, any]:
        """
        Get a summary of routing options for keywords.

        Args:
            keywords: Task keywords

        Returns:
            Dictionary with routing analysis
        """
        if isinstance(keywords, str):
            keywords = self.extract_keywords(keywords)

        team_scores = self.route_to_teams(keywords)

        summary = {
            "keywords": keywords,
            "team_scores": [
                {
                    "team": s.team.id.value,
                    "score": s.score,
                    "matched_keywords": s.matched_keywords,
                }
                for s in team_scores
            ],
            "recommended_teams": [
                s.team.id.value for s in team_scores
                if s.score >= self.multi_team_threshold
            ],
            "multi_team_needed": (
                len(team_scores) > 0 and
                team_scores[0].score < self.multi_team_threshold
            ),
        }

        return summary

    def add_team(self, team: Team) -> None:
        """
        Add a team to the router.

        Args:
            team: Team to add
        """
        self.teams[team.id] = team
        self.logger.info("Team added to router", team=team.id.value)

    def remove_team(self, team_id: TeamID) -> None:
        """
        Remove a team from the router.

        Args:
            team_id: Team ID to remove
        """
        if team_id in self.teams:
            del self.teams[team_id]
            self.logger.info("Team removed from router", team=team_id.value)

    def get_team(self, team_id: TeamID) -> Team | None:
        """
        Get a team by ID.

        Args:
            team_id: Team ID

        Returns:
            Team instance or None
        """
        return self.teams.get(team_id)
