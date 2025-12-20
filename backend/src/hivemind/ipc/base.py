"""
HIVEMIND IPC Base Types

Base message types and interfaces for inter-process communication.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

import msgpack


class MessageType(str, Enum):
    """Message type enumeration."""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    COMMAND = "command"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class MessagePriority(int, Enum):
    """Message priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3
    CRITICAL = 4


@dataclass
class AgentMessage:
    """
    Base message structure for agent communication.

    All IPC messages are serialized using msgpack for efficiency.
    """

    # Required fields
    message_id: str = field(default_factory=lambda: str(uuid4()))
    message_type: MessageType = MessageType.REQUEST
    sender: str = ""
    recipient: Optional[str] = None

    # Payload
    payload: dict[str, Any] = field(default_factory=dict)

    # Metadata
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: MessagePriority = MessagePriority.NORMAL
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

    # Headers for routing and tracing
    headers: dict[str, Any] = field(default_factory=dict)

    # TTL and retry
    ttl_seconds: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3

    def to_bytes(self) -> bytes:
        """
        Serialize message to msgpack bytes.

        Returns:
            Serialized message bytes
        """
        data = {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "sender": self.sender,
            "recipient": self.recipient,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
            "headers": self.headers,
            "ttl_seconds": self.ttl_seconds,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
        }
        return msgpack.packb(data, use_bin_type=True)

    @classmethod
    def from_bytes(cls, data: bytes) -> "AgentMessage":
        """
        Deserialize message from msgpack bytes.

        Args:
            data: Serialized message bytes

        Returns:
            Deserialized AgentMessage

        Raises:
            ValueError: If deserialization fails
        """
        try:
            decoded = msgpack.unpackb(data, raw=False)

            return cls(
                message_id=decoded["message_id"],
                message_type=MessageType(decoded["message_type"]),
                sender=decoded["sender"],
                recipient=decoded.get("recipient"),
                payload=decoded.get("payload", {}),
                timestamp=datetime.fromisoformat(decoded["timestamp"]),
                priority=MessagePriority(decoded.get("priority", MessagePriority.NORMAL.value)),
                correlation_id=decoded.get("correlation_id"),
                reply_to=decoded.get("reply_to"),
                headers=decoded.get("headers", {}),
                ttl_seconds=decoded.get("ttl_seconds"),
                retry_count=decoded.get("retry_count", 0),
                max_retries=decoded.get("max_retries", 3),
            )
        except Exception as e:
            raise ValueError(f"Failed to deserialize message: {e}")

    def create_reply(
        self,
        payload: dict[str, Any],
        sender: str,
        message_type: MessageType = MessageType.RESPONSE,
    ) -> "AgentMessage":
        """
        Create a reply message to this message.

        Args:
            payload: Reply payload
            sender: Reply sender ID
            message_type: Type of reply message

        Returns:
            New AgentMessage as reply
        """
        return AgentMessage(
            message_type=message_type,
            sender=sender,
            recipient=self.sender,
            payload=payload,
            correlation_id=self.message_id,
            priority=self.priority,
            headers=self.headers.copy(),
        )

    def create_error_reply(
        self,
        error: str,
        sender: str,
        error_code: Optional[str] = None,
    ) -> "AgentMessage":
        """
        Create an error reply message.

        Args:
            error: Error description
            sender: Reply sender ID
            error_code: Optional error code

        Returns:
            New AgentMessage as error reply
        """
        return AgentMessage(
            message_type=MessageType.ERROR,
            sender=sender,
            recipient=self.sender,
            payload={
                "error": error,
                "error_code": error_code,
                "original_message_id": self.message_id,
            },
            correlation_id=self.message_id,
            priority=MessagePriority.HIGH,
            headers=self.headers.copy(),
        )

    def increment_retry(self) -> bool:
        """
        Increment retry count.

        Returns:
            True if retry is allowed, False if max retries exceeded
        """
        self.retry_count += 1
        return self.retry_count <= self.max_retries

    def is_expired(self) -> bool:
        """
        Check if message has expired based on TTL.

        Returns:
            True if message is expired, False otherwise
        """
        if self.ttl_seconds is None:
            return False

        age_seconds = (datetime.utcnow() - self.timestamp).total_seconds()
        return age_seconds > self.ttl_seconds

    def to_dict(self) -> dict[str, Any]:
        """
        Convert message to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "sender": self.sender,
            "recipient": self.recipient,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
            "headers": self.headers,
            "ttl_seconds": self.ttl_seconds,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
        }

    def __repr__(self) -> str:
        return (
            f"AgentMessage(id={self.message_id[:8]}, "
            f"type={self.message_type.value}, "
            f"from={self.sender}, "
            f"to={self.recipient}, "
            f"priority={self.priority.value})"
        )
