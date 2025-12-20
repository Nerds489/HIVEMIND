"""
Application state management for HIVEMIND TUI.

Manages current session, messages, agents, and connection status.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Callable, Any

from ..models.agents import Agent, AgentStatus
from ..models.messages import Conversation, Message, MessageRole


class ConnectionStatus(str, Enum):
    """Connection status enumeration."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    RECONNECTING = "reconnecting"


@dataclass
class AppState:
    """Application state container with reactive updates."""

    # Session
    session_id: Optional[str] = None
    session_created_at: Optional[datetime] = None

    # Conversation
    conversation: Conversation = field(default_factory=Conversation)

    # Agents
    agents: List[Agent] = field(default_factory=list)
    selected_agent: Optional[Agent] = None

    # Connection
    connection_status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    last_error: Optional[str] = None

    # UI State
    is_processing: bool = False
    status_message: str = ""

    # Observers for reactive updates
    _observers: List[Callable[[str, Any], None]] = field(default_factory=list, repr=False)

    def __post_init__(self):
        """Initialize state after creation."""
        if self.conversation.session_id is None and self.session_id:
            self.conversation.session_id = self.session_id

    def add_observer(self, callback: Callable[[str, Any], None]) -> None:
        """Add an observer for state changes.

        Args:
            callback: Function called on state changes with (field_name, new_value)
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback: Callable[[str, Any], None]) -> None:
        """Remove an observer.

        Args:
            callback: Observer callback to remove
        """
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self, field_name: str, value: Any) -> None:
        """Notify observers of state change.

        Args:
            field_name: Name of changed field
            value: New value
        """
        for observer in self._observers:
            try:
                observer(field_name, value)
            except Exception:
                # Ignore observer errors
                pass

    def set_session(self, session_id: str, created_at: Optional[datetime] = None) -> None:
        """Set current session.

        Args:
            session_id: Session identifier
            created_at: Session creation time
        """
        self.session_id = session_id
        self.session_created_at = created_at or datetime.now()
        self.conversation.session_id = session_id
        self._notify_observers("session_id", session_id)

    def clear_session(self) -> None:
        """Clear current session."""
        self.session_id = None
        self.session_created_at = None
        self.conversation.session_id = None
        self._notify_observers("session_id", None)

    def add_message(
        self,
        role: MessageRole,
        content: str,
        agent_id: Optional[str] = None,
        **metadata,
    ) -> Message:
        """Add a message to the conversation.

        Args:
            role: Message role
            content: Message content
            agent_id: Optional agent ID
            **metadata: Additional metadata

        Returns:
            Created message
        """
        message = self.conversation.add(role, content, agent_id, **metadata)
        self._notify_observers("message_added", message)
        return message

    def clear_messages(self) -> None:
        """Clear all messages from conversation."""
        self.conversation.clear()
        self._notify_observers("messages_cleared", None)

    def set_agents(self, agents: List[Agent]) -> None:
        """Set available agents.

        Args:
            agents: List of agents
        """
        self.agents = agents
        # Update selected agent if it's in the new list
        if self.selected_agent:
            for agent in agents:
                if agent.id == self.selected_agent.id:
                    self.selected_agent = agent
                    break
        self._notify_observers("agents", agents)

    def select_agent(self, agent_id: Optional[str]) -> bool:
        """Select an agent by ID.

        Args:
            agent_id: Agent ID to select (None to deselect)

        Returns:
            True if agent was selected, False if not found
        """
        if agent_id is None:
            self.selected_agent = None
            self._notify_observers("selected_agent", None)
            return True

        for agent in self.agents:
            if agent.id == agent_id:
                self.selected_agent = agent
                self._notify_observers("selected_agent", agent)
                return True
        return False

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent if found, None otherwise
        """
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None

    def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        """Update an agent's status.

        Args:
            agent_id: Agent ID
            status: New status

        Returns:
            True if agent was updated, False if not found
        """
        agent = self.get_agent(agent_id)
        if agent:
            agent.set_status(status)
            self._notify_observers("agent_status", {"agent_id": agent_id, "status": status})
            return True
        return False

    def set_connection_status(self, status: ConnectionStatus, error: Optional[str] = None) -> None:
        """Set connection status.

        Args:
            status: New connection status
            error: Optional error message
        """
        self.connection_status = status
        self.last_error = error
        self._notify_observers("connection_status", status)

        if error:
            self._notify_observers("error", error)

    def set_processing(self, is_processing: bool, message: str = "") -> None:
        """Set processing state.

        Args:
            is_processing: Whether currently processing
            message: Optional status message
        """
        self.is_processing = is_processing
        self.status_message = message
        self._notify_observers("processing", is_processing)

        if message:
            self._notify_observers("status_message", message)

    def is_connected(self) -> bool:
        """Check if connected to backend.

        Returns:
            True if connected
        """
        return self.connection_status == ConnectionStatus.CONNECTED

    def has_session(self) -> bool:
        """Check if there is an active session.

        Returns:
            True if session exists
        """
        return self.session_id is not None

    def get_message_count(self) -> int:
        """Get total message count.

        Returns:
            Number of messages
        """
        return len(self.conversation)

    def get_last_message(self, role: Optional[MessageRole] = None) -> Optional[Message]:
        """Get the last message.

        Args:
            role: Optional role filter

        Returns:
            Last message or None
        """
        return self.conversation.get_last_message(role)

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary.

        Returns:
            State as dictionary
        """
        return {
            "session_id": self.session_id,
            "session_created_at": self.session_created_at.isoformat() if self.session_created_at else None,
            "message_count": len(self.conversation),
            "agent_count": len(self.agents),
            "selected_agent": self.selected_agent.id if self.selected_agent else None,
            "connection_status": self.connection_status.value,
            "is_processing": self.is_processing,
            "last_error": self.last_error,
        }

    def __str__(self) -> str:
        """String representation of state."""
        return (
            f"AppState(session={self.session_id}, "
            f"messages={len(self.conversation)}, "
            f"agents={len(self.agents)}, "
            f"status={self.connection_status.value})"
        )


class StateManager:
    """Manages application state with async support."""

    def __init__(self):
        """Initialize state manager."""
        self.state = AppState()
        self._lock = asyncio.Lock()

    async def update(self, **kwargs) -> None:
        """Update state atomically.

        Args:
            **kwargs: State fields to update
        """
        async with self._lock:
            for key, value in kwargs.items():
                if hasattr(self.state, key):
                    setattr(self.state, key, value)
                    self.state._notify_observers(key, value)

    async def get_snapshot(self) -> Dict[str, Any]:
        """Get thread-safe state snapshot.

        Returns:
            State dictionary
        """
        async with self._lock:
            return self.state.to_dict()

    def add_observer(self, callback: Callable[[str, Any], None]) -> None:
        """Add state observer.

        Args:
            callback: Observer callback
        """
        self.state.add_observer(callback)

    def remove_observer(self, callback: Callable[[str, Any], None]) -> None:
        """Remove state observer.

        Args:
            callback: Observer callback
        """
        self.state.remove_observer(callback)
