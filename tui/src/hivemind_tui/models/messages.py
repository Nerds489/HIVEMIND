"""
Message models for HIVEMIND TUI.

Defines message structures, roles, and conversation management.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class MessageRole(str, Enum):
    """Message role enumeration."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
    ERROR = "error"


@dataclass
class Message:
    """Represents a single message in a conversation."""

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def __str__(self) -> str:
        """String representation of message."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        if self.agent_id:
            return f"[{time_str}] [{self.agent_id}] {self.role.value}: {self.content}"
        return f"[{time_str}] {self.role.value}: {self.content}"

    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "agent_id": self.agent_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create message from dictionary."""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            agent_id=data.get("agent_id"),
            metadata=data.get("metadata", {}),
        )


class Conversation:
    """Manages a conversation history."""

    def __init__(self, session_id: Optional[str] = None):
        """Initialize conversation.

        Args:
            session_id: Optional session identifier
        """
        self.session_id = session_id
        self.messages: List[Message] = []
        self.created_at = datetime.now()

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation.

        Args:
            message: Message to add
        """
        self.messages.append(message)

    def add(self, role: MessageRole, content: str, agent_id: Optional[str] = None, **metadata) -> Message:
        """Add a new message to the conversation.

        Args:
            role: Message role
            content: Message content
            agent_id: Optional agent identifier
            **metadata: Additional metadata

        Returns:
            Created message
        """
        message = Message(role=role, content=content, agent_id=agent_id, metadata=metadata)
        self.add_message(message)
        return message

    def clear(self) -> None:
        """Clear all messages from conversation."""
        self.messages.clear()

    def get_messages(self, role: Optional[MessageRole] = None) -> List[Message]:
        """Get messages, optionally filtered by role.

        Args:
            role: Optional role filter

        Returns:
            List of messages
        """
        if role is None:
            return self.messages.copy()
        return [msg for msg in self.messages if msg.role == role]

    def get_last_message(self, role: Optional[MessageRole] = None) -> Optional[Message]:
        """Get the last message, optionally filtered by role.

        Args:
            role: Optional role filter

        Returns:
            Last message or None
        """
        messages = self.get_messages(role)
        return messages[-1] if messages else None

    def to_api_format(self) -> List[dict]:
        """Convert conversation to API format.

        Returns:
            List of message dictionaries for API
        """
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in self.messages
            if msg.role in (MessageRole.USER, MessageRole.ASSISTANT, MessageRole.SYSTEM)
        ]

    def __len__(self) -> int:
        """Get number of messages in conversation."""
        return len(self.messages)

    def __iter__(self):
        """Iterate over messages."""
        return iter(self.messages)
