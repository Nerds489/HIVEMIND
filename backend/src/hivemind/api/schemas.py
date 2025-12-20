"""
HIVEMIND API Schemas

Pydantic models for API request/response validation.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# =============================================================================
# Session Schemas
# =============================================================================

class SessionCreate(BaseModel):
    """Request to create a new session."""

    user_id: str | None = Field(None, description="Optional user ID")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Optional session metadata")


class MessageResponse(BaseModel):
    """Message in a conversation."""

    id: str
    role: str
    content: str
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionResponse(BaseModel):
    """Session information."""

    session_id: str
    user_id: str | None
    created_at: datetime
    last_activity: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)
    message_count: int = 0


class SessionWithMessages(SessionResponse):
    """Session with messages."""

    messages: list[MessageResponse] = Field(default_factory=list)


# =============================================================================
# Completion/Task Schemas
# =============================================================================

class TaskPriorityEnum(str, Enum):
    """Task priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class CompletionRequest(BaseModel):
    """Request to submit a task for processing."""

    prompt: str = Field(..., description="The task prompt or question", min_length=1)
    session_id: str | None = Field(None, description="Optional session ID for context")
    priority: TaskPriorityEnum = Field(TaskPriorityEnum.NORMAL, description="Task priority")
    user_id: str | None = Field(None, description="Optional user ID")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Optional task metadata")


class TaskState(str, Enum):
    """Task execution states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentResultResponse(BaseModel):
    """Result from a single agent."""

    agent_id: str
    team_id: str
    success: bool
    execution_time: float


class TaskStatusResponse(BaseModel):
    """Task status and result information."""

    task_id: str
    state: TaskState
    prompt: str
    priority: str
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration: float | None = None

    # Routing info
    target_teams: list[str] = Field(default_factory=list)
    target_agents: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)

    # Results
    results: list[AgentResultResponse] = Field(default_factory=list)
    error: str | None = None

    # Session context
    session_id: str | None = None


class CompletionResponse(BaseModel):
    """Response from task submission."""

    task_id: str
    state: TaskState
    message: str = "Task submitted successfully"


class CompletionResult(BaseModel):
    """Final completion result with synthesized response."""

    task_id: str
    state: TaskState
    prompt: str
    response: str | None = None
    error: str | None = None
    duration: float | None = None
    created_at: datetime
    completed_at: datetime | None = None


# =============================================================================
# Agent/Team Schemas
# =============================================================================

class AgentCapabilityResponse(str, Enum):
    """Agent capabilities."""
    ARCHITECTURE = "architecture"
    BACKEND = "backend"
    FRONTEND = "frontend"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    DEVOPS = "devops"
    SECURITY_ARCHITECTURE = "security_architecture"
    PENETRATION_TESTING = "penetration_testing"
    MALWARE_ANALYSIS = "malware_analysis"
    WIRELESS_SECURITY = "wireless_security"
    COMPLIANCE = "compliance"
    INCIDENT_RESPONSE = "incident_response"
    CLOUD_ARCHITECTURE = "cloud_architecture"
    SYSTEMS_ADMIN = "systems_admin"
    NETWORKING = "networking"
    DATABASE = "database"
    SRE = "sre"
    AUTOMATION = "automation"
    TEST_STRATEGY = "test_strategy"
    TEST_AUTOMATION = "test_automation"
    PERFORMANCE_TESTING = "performance_testing"
    SECURITY_TESTING = "security_testing"
    MANUAL_TESTING = "manual_testing"
    TEST_DATA = "test_data"


class AgentStateResponse(str, Enum):
    """Agent states."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"


class AgentResponse(BaseModel):
    """Agent information."""

    id: str
    name: str
    team: str
    description: str
    state: AgentStateResponse
    capabilities: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)

    # Task info
    current_task_id: str | None = None
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0

    # Availability
    is_available: bool = True


class TeamResponse(BaseModel):
    """Team information."""

    id: str
    name: str
    description: str
    keywords: list[str] = Field(default_factory=list)
    agent_count: int = 0
    available_agents: int = 0
    availability: float = 0.0


class TeamWithAgents(TeamResponse):
    """Team with agent details."""

    agents: list[AgentResponse] = Field(default_factory=list)


# =============================================================================
# WebSocket Message Schemas
# =============================================================================

class WSMessageType(str, Enum):
    """WebSocket message types."""
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    TASK_UPDATE = "task_update"
    TASK_RESULT = "task_result"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


class WSMessage(BaseModel):
    """WebSocket message."""

    type: WSMessageType
    data: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WSSubscribeRequest(BaseModel):
    """Subscribe to task updates."""

    task_id: str


class WSUnsubscribeRequest(BaseModel):
    """Unsubscribe from task updates."""

    task_id: str


class WSTaskUpdate(BaseModel):
    """Task status update."""

    task_id: str
    state: str
    progress: float | None = None
    message: str | None = None


class WSTaskResult(BaseModel):
    """Task completion result."""

    task_id: str
    state: str
    response: str | None = None
    error: str | None = None


class WSError(BaseModel):
    """WebSocket error."""

    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


# =============================================================================
# Health Check Schemas
# =============================================================================

class HealthStatus(str, Enum):
    """Health check status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheck(BaseModel):
    """Health check response."""

    status: HealthStatus
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ReadinessCheck(BaseModel):
    """Readiness check response."""

    status: str
    version: str
    checks: dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Error Schemas
# =============================================================================

class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    message: str
    details: dict[str, Any] | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
