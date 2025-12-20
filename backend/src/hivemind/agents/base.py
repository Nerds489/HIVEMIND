"""
HIVEMIND Agent Base Classes

Defines the core agent abstraction and state machine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AgentState(str, Enum):
    """Agent execution states."""
    IDLE = "idle"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    PAUSED = "paused"


class AgentCapability(str, Enum):
    """Agent capability categories."""
    # Development
    ARCHITECTURE = "architecture"
    BACKEND = "backend"
    FRONTEND = "frontend"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    DEVOPS = "devops"

    # Security
    SECURITY_ARCHITECTURE = "security_architecture"
    PENETRATION_TESTING = "penetration_testing"
    MALWARE_ANALYSIS = "malware_analysis"
    WIRELESS_SECURITY = "wireless_security"
    COMPLIANCE = "compliance"
    INCIDENT_RESPONSE = "incident_response"

    # Infrastructure
    CLOUD_ARCHITECTURE = "cloud_architecture"
    SYSTEMS_ADMIN = "systems_admin"
    NETWORKING = "networking"
    DATABASE = "database"
    SRE = "sre"
    AUTOMATION = "automation"

    # QA
    TEST_STRATEGY = "test_strategy"
    TEST_AUTOMATION = "test_automation"
    PERFORMANCE_TESTING = "performance_testing"
    SECURITY_TESTING = "security_testing"
    MANUAL_TESTING = "manual_testing"
    TEST_DATA = "test_data"


@dataclass
class AgentMetadata:
    """Agent metadata and configuration."""
    id: str
    name: str
    team: str
    description: str
    capabilities: list[AgentCapability]
    keywords: list[str]
    handoff_targets: list[str] = field(default_factory=list)
    escalation_path: list[str] = field(default_factory=list)
    system_prompt: str | None = None


@dataclass
class Agent:
    """
    Base agent class representing a specialized AI agent.

    Agents are the workers in the HIVEMIND system, each with specific
    expertise and capabilities. They execute tasks assigned by the
    Coordinator and report results back.
    """

    metadata: AgentMetadata
    state: AgentState = AgentState.IDLE
    current_task_id: str | None = None
    last_activity: datetime | None = None
    error_count: int = 0
    success_count: int = 0

    @property
    def id(self) -> str:
        """Get agent ID."""
        return self.metadata.id

    @property
    def name(self) -> str:
        """Get agent name."""
        return self.metadata.name

    @property
    def team(self) -> str:
        """Get agent team."""
        return self.metadata.team

    @property
    def is_available(self) -> bool:
        """Check if agent is available for new tasks."""
        return self.state in (AgentState.IDLE, AgentState.SUCCESS, AgentState.ERROR)

    @property
    def is_busy(self) -> bool:
        """Check if agent is currently busy."""
        return self.state in (AgentState.PENDING, AgentState.RUNNING)

    def can_handle(self, keywords: list[str]) -> bool:
        """
        Check if this agent can handle a task based on keywords.

        Args:
            keywords: Task keywords to match

        Returns:
            True if agent has matching capabilities
        """
        agent_keywords = set(kw.lower() for kw in self.metadata.keywords)
        task_keywords = set(kw.lower() for kw in keywords)
        return bool(agent_keywords & task_keywords)

    def transition_to(self, new_state: AgentState) -> None:
        """
        Transition agent to a new state.

        Args:
            new_state: Target state
        """
        self.state = new_state
        self.last_activity = datetime.utcnow()

        if new_state == AgentState.SUCCESS:
            self.success_count += 1
        elif new_state == AgentState.ERROR:
            self.error_count += 1

    def assign_task(self, task_id: str) -> None:
        """
        Assign a task to this agent.

        Args:
            task_id: ID of the task to assign
        """
        self.current_task_id = task_id
        self.transition_to(AgentState.PENDING)

    def start_execution(self) -> None:
        """Mark agent as running."""
        self.transition_to(AgentState.RUNNING)

    def complete_task(self, success: bool = True) -> None:
        """
        Complete the current task.

        Args:
            success: Whether the task completed successfully
        """
        self.current_task_id = None
        self.transition_to(AgentState.SUCCESS if success else AgentState.ERROR)

    def reset(self) -> None:
        """Reset agent to idle state."""
        self.current_task_id = None
        self.transition_to(AgentState.IDLE)

    def to_dict(self) -> dict[str, Any]:
        """Convert agent to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "state": self.state.value,
            "current_task_id": self.current_task_id,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "capabilities": [c.value for c in self.metadata.capabilities],
        }
