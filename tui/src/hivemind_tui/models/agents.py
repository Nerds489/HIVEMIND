"""
Agent models for HIVEMIND TUI.

Defines agent structures, teams, and status management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class AgentStatus(str, Enum):
    """Agent status enumeration."""

    IDLE = "idle"
    BUSY = "busy"
    THINKING = "thinking"
    RESPONDING = "responding"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class Agent:
    """Represents an AI agent."""

    id: str
    name: str
    description: str
    status: AgentStatus = AgentStatus.IDLE
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    team_id: Optional[str] = None

    def __str__(self) -> str:
        """String representation of agent."""
        return f"{self.name} ({self.id}) - {self.status.value}"

    def to_dict(self) -> dict:
        """Convert agent to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
            "team_id": self.team_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Agent":
        """Create agent from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            status=AgentStatus(data.get("status", "idle")),
            capabilities=data.get("capabilities", []),
            metadata=data.get("metadata", {}),
            team_id=data.get("team_id"),
        )

    def is_available(self) -> bool:
        """Check if agent is available for tasks."""
        return self.status in (AgentStatus.IDLE, AgentStatus.THINKING)

    def set_status(self, status: AgentStatus) -> None:
        """Update agent status.

        Args:
            status: New status
        """
        self.status = status


@dataclass
class Team:
    """Represents a team of agents."""

    id: str
    name: str
    description: str
    agents: List[Agent] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def __str__(self) -> str:
        """String representation of team."""
        return f"{self.name} ({len(self.agents)} agents)"

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the team.

        Args:
            agent: Agent to add
        """
        agent.team_id = self.id
        self.agents.append(agent)

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the team.

        Args:
            agent_id: ID of agent to remove

        Returns:
            True if agent was removed, False if not found
        """
        for i, agent in enumerate(self.agents):
            if agent.id == agent_id:
                agent.team_id = None
                self.agents.pop(i)
                return True
        return False

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID.

        Args:
            agent_id: Agent ID to find

        Returns:
            Agent if found, None otherwise
        """
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None

    def get_available_agents(self) -> List[Agent]:
        """Get all available agents in the team.

        Returns:
            List of available agents
        """
        return [agent for agent in self.agents if agent.is_available()]

    def to_dict(self) -> dict:
        """Convert team to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agents": [agent.to_dict() for agent in self.agents],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        """Create team from dictionary."""
        team = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            metadata=data.get("metadata", {}),
        )
        for agent_data in data.get("agents", []):
            team.add_agent(Agent.from_dict(agent_data))
        return team
