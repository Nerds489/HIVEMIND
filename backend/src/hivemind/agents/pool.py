"""
HIVEMIND Agent Pool

Manages all 24 agents across the 4 teams.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from hivemind.agents.base import Agent, AgentCapability, AgentMetadata, AgentState
from hivemind.agents.teams import Team, TeamID, create_team, TEAM_CONFIGS
from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)


# Default agent definitions when no config file is available
DEFAULT_AGENTS: list[dict] = [
    # Development Team (DEV-001 to DEV-006)
    {
        "id": "DEV-001",
        "name": "Architect",
        "team": "DEV",
        "description": "System design and architecture decisions",
        "capabilities": ["architecture"],
        "keywords": ["architecture", "design", "system", "pattern", "structure", "diagram"],
    },
    {
        "id": "DEV-002",
        "name": "Backend Developer",
        "team": "DEV",
        "description": "Server-side code, APIs, and databases",
        "capabilities": ["backend"],
        "keywords": ["backend", "api", "server", "database", "endpoint", "rest", "graphql"],
    },
    {
        "id": "DEV-003",
        "name": "Frontend Developer",
        "team": "DEV",
        "description": "UI/UX and client-side applications",
        "capabilities": ["frontend"],
        "keywords": ["frontend", "ui", "ux", "react", "vue", "angular", "css", "html", "javascript"],
    },
    {
        "id": "DEV-004",
        "name": "Code Reviewer",
        "team": "DEV",
        "description": "Code quality and design patterns",
        "capabilities": ["code_review"],
        "keywords": ["review", "quality", "refactor", "pattern", "clean", "style", "lint"],
    },
    {
        "id": "DEV-005",
        "name": "Technical Writer",
        "team": "DEV",
        "description": "Documentation and API guides",
        "capabilities": ["documentation"],
        "keywords": ["document", "readme", "guide", "api", "docs", "comment", "explain"],
    },
    {
        "id": "DEV-006",
        "name": "DevOps Liaison",
        "team": "DEV",
        "description": "CI/CD and deployment pipelines",
        "capabilities": ["devops"],
        "keywords": ["cicd", "pipeline", "deploy", "build", "release", "github", "gitlab"],
    },

    # Security Team (SEC-001 to SEC-006)
    {
        "id": "SEC-001",
        "name": "Security Architect",
        "team": "SEC",
        "description": "Threat modeling and secure design",
        "capabilities": ["security_architecture"],
        "keywords": ["threat", "model", "secure", "design", "risk", "framework"],
    },
    {
        "id": "SEC-002",
        "name": "Penetration Tester",
        "team": "SEC",
        "description": "Offensive security and vulnerability testing",
        "capabilities": ["penetration_testing"],
        "keywords": ["pentest", "exploit", "vulnerability", "attack", "hack", "ctf"],
    },
    {
        "id": "SEC-003",
        "name": "Malware Analyst",
        "team": "SEC",
        "description": "Reverse engineering and threat analysis",
        "capabilities": ["malware_analysis"],
        "keywords": ["malware", "reverse", "binary", "analysis", "threat", "ioc"],
    },
    {
        "id": "SEC-004",
        "name": "Wireless Security Expert",
        "team": "SEC",
        "description": "WiFi, Bluetooth, and RF security",
        "capabilities": ["wireless_security"],
        "keywords": ["wireless", "wifi", "bluetooth", "rf", "radio", "signal"],
    },
    {
        "id": "SEC-005",
        "name": "Compliance Auditor",
        "team": "SEC",
        "description": "Regulatory compliance (SOC2, GDPR, PCI)",
        "capabilities": ["compliance"],
        "keywords": ["compliance", "audit", "soc2", "gdpr", "pci", "hipaa", "policy"],
    },
    {
        "id": "SEC-006",
        "name": "Incident Responder",
        "team": "SEC",
        "description": "Forensics and incident management",
        "capabilities": ["incident_response"],
        "keywords": ["incident", "forensic", "response", "breach", "investigate"],
    },

    # Infrastructure Team (INF-001 to INF-006)
    {
        "id": "INF-001",
        "name": "Infrastructure Architect",
        "team": "INF",
        "description": "Cloud architecture and design",
        "capabilities": ["cloud_architecture"],
        "keywords": ["cloud", "aws", "azure", "gcp", "architecture", "infrastructure"],
    },
    {
        "id": "INF-002",
        "name": "Systems Administrator",
        "team": "INF",
        "description": "Server management and configuration",
        "capabilities": ["systems_admin"],
        "keywords": ["linux", "windows", "server", "admin", "configure", "manage"],
    },
    {
        "id": "INF-003",
        "name": "Network Engineer",
        "team": "INF",
        "description": "Networking and connectivity",
        "capabilities": ["networking"],
        "keywords": ["network", "firewall", "vpc", "dns", "routing", "load"],
    },
    {
        "id": "INF-004",
        "name": "Database Administrator",
        "team": "INF",
        "description": "Database optimization and backup",
        "capabilities": ["database"],
        "keywords": ["database", "sql", "postgres", "mysql", "mongo", "redis", "backup"],
    },
    {
        "id": "INF-005",
        "name": "Site Reliability Engineer",
        "team": "INF",
        "description": "Monitoring, observability, and SLOs",
        "capabilities": ["sre"],
        "keywords": ["monitoring", "alert", "slo", "sli", "observability", "prometheus"],
    },
    {
        "id": "INF-006",
        "name": "Automation Engineer",
        "team": "INF",
        "description": "Terraform, Ansible, and Infrastructure as Code",
        "capabilities": ["automation"],
        "keywords": ["terraform", "ansible", "iac", "automation", "script", "provision"],
    },

    # QA Team (QA-001 to QA-006)
    {
        "id": "QA-001",
        "name": "QA Architect",
        "team": "QA",
        "description": "Test strategy and quality processes",
        "capabilities": ["test_strategy"],
        "keywords": ["strategy", "quality", "process", "framework", "methodology"],
    },
    {
        "id": "QA-002",
        "name": "Test Automation Engineer",
        "team": "QA",
        "description": "Automated testing and frameworks",
        "capabilities": ["test_automation"],
        "keywords": ["automation", "selenium", "cypress", "playwright", "framework"],
    },
    {
        "id": "QA-003",
        "name": "Performance Tester",
        "team": "QA",
        "description": "Load testing and performance analysis",
        "capabilities": ["performance_testing"],
        "keywords": ["performance", "load", "stress", "benchmark", "jmeter", "k6"],
    },
    {
        "id": "QA-004",
        "name": "Security Tester",
        "team": "QA",
        "description": "SAST/DAST and vulnerability scanning",
        "capabilities": ["security_testing"],
        "keywords": ["sast", "dast", "scan", "security", "vulnerability", "owasp"],
    },
    {
        "id": "QA-005",
        "name": "Manual QA Tester",
        "team": "QA",
        "description": "Exploratory testing and UAT",
        "capabilities": ["manual_testing"],
        "keywords": ["manual", "exploratory", "uat", "acceptance", "usability"],
    },
    {
        "id": "QA-006",
        "name": "Test Data Manager",
        "team": "QA",
        "description": "Test data and fixtures",
        "capabilities": ["test_data"],
        "keywords": ["data", "fixture", "mock", "seed", "generate", "synthetic"],
    },
]


class AgentPool:
    """
    Manages all agents across all teams.

    The AgentPool is the central registry for all 24 agents, providing
    methods for agent lookup, team management, and task routing.
    """

    def __init__(self) -> None:
        """Initialize the agent pool."""
        self._teams: dict[TeamID, Team] = {}
        self._agents: dict[str, Agent] = {}
        self._initialized = False

    @property
    def teams(self) -> dict[TeamID, Team]:
        """Get all teams."""
        return self._teams

    @property
    def agents(self) -> dict[str, Agent]:
        """Get all agents."""
        return self._agents

    @property
    def total_agents(self) -> int:
        """Get total number of agents."""
        return len(self._agents)

    @property
    def available_agents(self) -> list[Agent]:
        """Get all available agents."""
        return [a for a in self._agents.values() if a.is_available]

    @property
    def busy_agents(self) -> list[Agent]:
        """Get all busy agents."""
        return [a for a in self._agents.values() if a.is_busy]

    def initialize(self, config_path: Path | None = None) -> None:
        """
        Initialize the agent pool from configuration.

        Args:
            config_path: Path to agents configuration file
        """
        if self._initialized:
            return

        # Create teams
        for team_id in TeamID:
            self._teams[team_id] = create_team(team_id)

        # Load agent definitions
        agents_data = self._load_agents_config(config_path)

        # Create agents and assign to teams
        for agent_data in agents_data:
            agent = self._create_agent(agent_data)
            self._agents[agent.id] = agent

            team_id = TeamID(agent.team)
            if team_id in self._teams:
                self._teams[team_id].add_agent(agent)

        self._initialized = True
        logger.info(
            "Agent pool initialized",
            total_agents=len(self._agents),
            teams=len(self._teams),
        )

    def _load_agents_config(self, config_path: Path | None = None) -> list[dict]:
        """Load agent configuration from file or defaults."""
        if config_path is None:
            settings = get_settings()
            config_path = settings.agents_config_path

        if config_path and config_path.exists():
            try:
                with open(config_path) as f:
                    data = json.load(f)
                    return data.get("agents", data)
            except Exception as e:
                logger.warning(
                    "Failed to load agents config, using defaults",
                    path=str(config_path),
                    error=str(e),
                )

        return DEFAULT_AGENTS

    def _create_agent(self, data: dict) -> Agent:
        """Create an agent from configuration data."""
        capabilities = [
            AgentCapability(c) if isinstance(c, str) else c
            for c in data.get("capabilities", [])
        ]

        metadata = AgentMetadata(
            id=data["id"],
            name=data["name"],
            team=data["team"],
            description=data.get("description", ""),
            capabilities=capabilities,
            keywords=data.get("keywords", []),
            handoff_targets=data.get("handoff_targets", []),
            escalation_path=data.get("escalation_path", []),
            system_prompt=data.get("system_prompt"),
        )

        return Agent(metadata=metadata)

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID."""
        return self._agents.get(agent_id)

    def get_team(self, team_id: TeamID) -> Team | None:
        """Get a team by ID."""
        return self._teams.get(team_id)

    def get_agents_by_team(self, team_id: TeamID) -> list[Agent]:
        """Get all agents in a team."""
        team = self._teams.get(team_id)
        return team.agents if team else []

    def find_agents_by_keywords(self, keywords: list[str]) -> list[Agent]:
        """
        Find agents that can handle the given keywords.

        Args:
            keywords: Keywords to match

        Returns:
            List of matching agents, sorted by relevance
        """
        matches = []
        for agent in self._agents.values():
            if agent.can_handle(keywords):
                # Score by number of matching keywords
                agent_keywords = set(kw.lower() for kw in agent.metadata.keywords)
                task_keywords = set(kw.lower() for kw in keywords)
                score = len(agent_keywords & task_keywords)
                matches.append((score, agent))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches]

    def find_teams_by_keywords(self, keywords: list[str]) -> list[Team]:
        """
        Find teams that can handle the given keywords.

        Args:
            keywords: Keywords to match

        Returns:
            List of matching teams
        """
        return [t for t in self._teams.values() if t.can_handle(keywords)]

    def get_best_agent_for_task(self, keywords: list[str]) -> Agent | None:
        """
        Get the best available agent for a task.

        Args:
            keywords: Task keywords

        Returns:
            Best matching available agent, or None
        """
        # Find matching teams
        teams = self.find_teams_by_keywords(keywords)
        if not teams:
            # Fallback to any available agent
            available = self.available_agents
            return available[0] if available else None

        # Get best agent from matching teams
        for team in teams:
            agent = team.get_best_agent(keywords)
            if agent:
                return agent

        return None

    def __iter__(self) -> Iterator[Agent]:
        """Iterate over all agents."""
        return iter(self._agents.values())

    def __len__(self) -> int:
        """Get number of agents."""
        return len(self._agents)


# Global agent pool instance
_agent_pool: AgentPool | None = None


def get_agent_pool() -> AgentPool:
    """Get the global agent pool instance."""
    global _agent_pool
    if _agent_pool is None:
        _agent_pool = AgentPool()
        _agent_pool.initialize()
    return _agent_pool
