"""
HIVEMIND Team Definitions

Defines the 4 specialized teams and their agent compositions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hivemind.agents.base import Agent


class TeamID(str, Enum):
    """Team identifiers."""
    DEV = "DEV"      # Development Team
    SEC = "SEC"      # Security Team
    INF = "INF"      # Infrastructure Team
    QA = "QA"        # Quality Assurance Team


@dataclass
class TeamConfig:
    """Team configuration and metadata."""
    id: TeamID
    name: str
    description: str
    keywords: list[str]
    color: str  # For TUI display


# Team configurations
TEAM_CONFIGS: dict[TeamID, TeamConfig] = {
    TeamID.DEV: TeamConfig(
        id=TeamID.DEV,
        name="Development",
        description="Software development, architecture, and code quality",
        keywords=[
            "code", "implement", "build", "create", "function", "api",
            "develop", "program", "write", "fix", "bug", "feature",
            "refactor", "optimize", "class", "method", "module",
            "library", "framework", "design", "architecture",
        ],
        color="#39ff14",  # Matrix Green
    ),
    TeamID.SEC: TeamConfig(
        id=TeamID.SEC,
        name="Security",
        description="Security assessment, vulnerability analysis, and incident response",
        keywords=[
            "security", "vulnerability", "audit", "pentest", "encrypt",
            "auth", "authentication", "authorization", "exploit",
            "malware", "threat", "attack", "defense", "firewall",
            "intrusion", "forensic", "compliance", "risk", "breach",
        ],
        color="#ff0090",  # Neon Magenta
    ),
    TeamID.INF: TeamConfig(
        id=TeamID.INF,
        name="Infrastructure",
        description="Cloud infrastructure, deployment, and operations",
        keywords=[
            "deploy", "scale", "kubernetes", "docker", "server", "cloud",
            "aws", "azure", "gcp", "infrastructure", "network", "database",
            "monitoring", "logging", "terraform", "ansible", "ci/cd",
            "pipeline", "container", "cluster", "load", "balance",
        ],
        color="#00ffff",  # Electric Cyan
    ),
    TeamID.QA: TeamConfig(
        id=TeamID.QA,
        name="Quality Assurance",
        description="Testing, quality control, and performance validation",
        keywords=[
            "test", "quality", "bug", "regression", "performance",
            "automation", "selenium", "cypress", "jest", "pytest",
            "coverage", "integration", "unit", "e2e", "acceptance",
            "benchmark", "load", "stress", "validate", "verify",
        ],
        color="#9900ff",  # Electric Purple
    ),
}


@dataclass
class Team:
    """
    Represents a team of specialized agents.

    Teams group agents with related capabilities and are the primary
    unit of task routing in HIVEMIND.
    """

    config: TeamConfig
    agents: list[Agent] = field(default_factory=list)

    @property
    def id(self) -> TeamID:
        """Get team ID."""
        return self.config.id

    @property
    def name(self) -> str:
        """Get team name."""
        return self.config.name

    @property
    def size(self) -> int:
        """Get number of agents in team."""
        return len(self.agents)

    @property
    def available_agents(self) -> list[Agent]:
        """Get list of available agents."""
        return [a for a in self.agents if a.is_available]

    @property
    def busy_agents(self) -> list[Agent]:
        """Get list of busy agents."""
        return [a for a in self.agents if a.is_busy]

    @property
    def availability(self) -> float:
        """Get team availability ratio (0.0 to 1.0)."""
        if not self.agents:
            return 0.0
        return len(self.available_agents) / len(self.agents)

    def can_handle(self, keywords: list[str]) -> bool:
        """
        Check if this team can handle a task based on keywords.

        Args:
            keywords: Task keywords to match

        Returns:
            True if team has matching keywords
        """
        team_keywords = set(kw.lower() for kw in self.config.keywords)
        task_keywords = set(kw.lower() for kw in keywords)
        return bool(team_keywords & task_keywords)

    def get_best_agent(self, keywords: list[str]) -> Agent | None:
        """
        Get the best available agent for the given keywords.

        Args:
            keywords: Task keywords to match

        Returns:
            Best matching available agent, or None if none available
        """
        available = self.available_agents
        if not available:
            return None

        # Score agents by keyword match
        scored = []
        for agent in available:
            agent_keywords = set(kw.lower() for kw in agent.metadata.keywords)
            task_keywords = set(kw.lower() for kw in keywords)
            score = len(agent_keywords & task_keywords)
            scored.append((score, agent))

        # Sort by score descending, return best match
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else available[0]

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the team."""
        if agent not in self.agents:
            self.agents.append(agent)

    def remove_agent(self, agent_id: str) -> Agent | None:
        """Remove an agent from the team by ID."""
        for i, agent in enumerate(self.agents):
            if agent.id == agent_id:
                return self.agents.pop(i)
        return None

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID."""
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None


def create_team(team_id: TeamID) -> Team:
    """
    Create a new team instance.

    Args:
        team_id: The team identifier

    Returns:
        Configured Team instance
    """
    config = TEAM_CONFIGS.get(team_id)
    if not config:
        raise ValueError(f"Unknown team ID: {team_id}")
    return Team(config=config)
