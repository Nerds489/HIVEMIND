"""
HIVEMIND Context Manager

Manages conversation context, session state, and history with Redis-backed storage
and sliding window context management.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import redis.asyncio as aioredis
from redis.asyncio import Redis

from hivemind.config import get_settings
from hivemind.observability.logging import LoggerMixin
from hivemind.observability.metrics import get_metrics


@dataclass
class Message:
    """A single message in a conversation."""
    id: str
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Message:
        """Create message from dictionary."""
        return cls(
            id=data["id"],
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )


@dataclass
class ConversationContext:
    """Context for a conversation session."""
    session_id: str
    user_id: str | None = None
    messages: list[Message] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.last_activity = datetime.utcnow()

    def get_messages(
        self,
        limit: int | None = None,
        roles: list[str] | None = None,
    ) -> list[Message]:
        """
        Get messages from the conversation.

        Args:
            limit: Maximum number of messages to return (most recent)
            roles: Filter by message roles

        Returns:
            List of messages
        """
        messages = self.messages

        if roles:
            messages = [m for m in messages if m.role in roles]

        if limit:
            messages = messages[-limit:]

        return messages

    def get_context_window(
        self,
        max_messages: int = 50,
        max_chars: int | None = None,
    ) -> list[Message]:
        """
        Get a sliding window of recent context.

        Args:
            max_messages: Maximum number of messages
            max_chars: Maximum total characters (if set)

        Returns:
            List of messages in the window
        """
        messages = self.messages[-max_messages:]

        if max_chars:
            # Trim from oldest messages to fit character limit
            total_chars = sum(len(m.content) for m in messages)
            while total_chars > max_chars and len(messages) > 1:
                removed = messages.pop(0)
                total_chars -= len(removed.content)

        return messages

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "messages": [m.to_dict() for m in self.messages],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationContext:
        """Create context from dictionary."""
        return cls(
            session_id=data["session_id"],
            user_id=data.get("user_id"),
            messages=[Message.from_dict(m) for m in data.get("messages", [])],
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_activity=datetime.fromisoformat(data["last_activity"]),
        )


class ContextManager(LoggerMixin):
    """
    Manages conversation context and session state with Redis backing.

    Features:
    - Session creation and lifecycle management
    - Conversation history storage and retrieval
    - Sliding window context for limiting context size
    - Message tracking and metadata
    - Redis-backed persistence with TTL
    - Session expiration and cleanup
    """

    def __init__(
        self,
        redis_client: Redis | None = None,
        session_ttl: int | None = None,
        default_window_size: int = 50,
    ) -> None:
        """
        Initialize the ContextManager.

        Args:
            redis_client: Redis client (will create if not provided)
            session_ttl: Session TTL in seconds
            default_window_size: Default context window size
        """
        self._redis = redis_client
        self._settings = get_settings()
        self.session_ttl = session_ttl or self._settings.redis.session_ttl
        self.default_window_size = default_window_size

        # In-memory cache of active contexts
        self._contexts: dict[str, ConversationContext] = {}

        self._metrics = get_metrics()

        self.logger.info(
            "ContextManager initialized",
            session_ttl=self.session_ttl,
            default_window_size=default_window_size,
        )

    async def _get_redis(self) -> Redis:
        """Get or create Redis client."""
        if self._redis is None:
            redis_config = self._settings.redis
            self._redis = await aioredis.from_url(
                redis_config.url,
                max_connections=redis_config.max_connections,
                socket_timeout=redis_config.socket_timeout,
                socket_connect_timeout=redis_config.socket_connect_timeout,
            )
            self.logger.info("Redis client created")

        return self._redis

    def _get_session_key(self, session_id: str) -> str:
        """Get Redis key for a session."""
        prefix = self._settings.redis.key_prefix
        return f"{prefix}session:{session_id}"

    async def create_session(
        self,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationContext:
        """
        Create a new conversation session.

        Args:
            user_id: Optional user ID
            metadata: Optional session metadata

        Returns:
            ConversationContext instance
        """
        session_id = str(uuid.uuid4())

        context = ConversationContext(
            session_id=session_id,
            user_id=user_id,
            metadata=metadata or {},
        )

        # Store in memory cache
        self._contexts[session_id] = context

        # Persist to Redis
        await self._save_context(context)

        # Update metrics
        self._metrics.sessions_total.inc()
        self._metrics.sessions_active.inc()

        self.logger.info(
            "Session created",
            session_id=session_id,
            user_id=user_id,
        )

        return context

    async def get_session(self, session_id: str) -> ConversationContext | None:
        """
        Get a session by ID.

        Args:
            session_id: Session ID

        Returns:
            ConversationContext or None if not found
        """
        # Check memory cache first
        if session_id in self._contexts:
            return self._contexts[session_id]

        # Load from Redis
        context = await self._load_context(session_id)

        if context:
            # Cache in memory
            self._contexts[session_id] = context

        return context

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """
        Add a message to a session.

        Args:
            session_id: Session ID
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional message metadata

        Returns:
            Created Message instance
        """
        context = await self.get_session(session_id)

        if not context:
            raise ValueError(f"Session not found: {session_id}")

        message = Message(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            metadata=metadata or {},
        )

        context.add_message(message)

        # Persist to Redis
        await self._save_context(context)

        self.logger.debug(
            "Message added",
            session_id=session_id,
            message_id=message.id,
            role=role,
        )

        return message

    async def get_messages(
        self,
        session_id: str,
        limit: int | None = None,
        roles: list[str] | None = None,
    ) -> list[Message]:
        """
        Get messages from a session.

        Args:
            session_id: Session ID
            limit: Maximum number of messages
            roles: Filter by roles

        Returns:
            List of messages
        """
        context = await self.get_session(session_id)

        if not context:
            return []

        return context.get_messages(limit=limit, roles=roles)

    async def get_context_window(
        self,
        session_id: str,
        max_messages: int | None = None,
        max_chars: int | None = None,
    ) -> list[Message]:
        """
        Get a sliding window of context for a session.

        Args:
            session_id: Session ID
            max_messages: Maximum messages in window
            max_chars: Maximum characters in window

        Returns:
            List of messages in the window
        """
        context = await self.get_session(session_id)

        if not context:
            return []

        return context.get_context_window(
            max_messages=max_messages or self.default_window_size,
            max_chars=max_chars,
        )

    async def update_metadata(
        self,
        session_id: str,
        metadata: dict[str, Any],
        merge: bool = True,
    ) -> None:
        """
        Update session metadata.

        Args:
            session_id: Session ID
            metadata: Metadata to set
            merge: If True, merge with existing; if False, replace
        """
        context = await self.get_session(session_id)

        if not context:
            raise ValueError(f"Session not found: {session_id}")

        if merge:
            context.metadata.update(metadata)
        else:
            context.metadata = metadata

        # Persist to Redis
        await self._save_context(context)

        self.logger.debug(
            "Metadata updated",
            session_id=session_id,
        )

    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session ID

        Returns:
            True if deleted, False if not found
        """
        # Remove from memory cache
        if session_id in self._contexts:
            context = self._contexts.pop(session_id)

            # Update metrics
            duration = (datetime.utcnow() - context.created_at).total_seconds()
            self._metrics.session_duration_seconds.observe(duration)
            self._metrics.sessions_active.dec()

        # Remove from Redis
        redis = await self._get_redis()
        key = self._get_session_key(session_id)
        result = await redis.delete(key)

        self.logger.info("Session deleted", session_id=session_id)

        return result > 0

    async def list_sessions(
        self,
        user_id: str | None = None,
    ) -> list[str]:
        """
        List all session IDs.

        Args:
            user_id: Optional filter by user ID

        Returns:
            List of session IDs
        """
        # For now, just return from memory cache
        # In production, you'd scan Redis keys
        sessions = list(self._contexts.keys())

        if user_id:
            sessions = [
                sid for sid in sessions
                if self._contexts[sid].user_id == user_id
            ]

        return sessions

    async def cleanup_expired(self) -> int:
        """
        Clean up expired sessions.

        Returns:
            Number of sessions cleaned up
        """
        # Redis handles TTL automatically, but we clean up memory cache
        count = 0
        expired = []

        for session_id, context in self._contexts.items():
            age = (datetime.utcnow() - context.last_activity).total_seconds()
            if age > self.session_ttl:
                expired.append(session_id)

        for session_id in expired:
            await self.delete_session(session_id)
            count += 1

        if count > 0:
            self.logger.info("Expired sessions cleaned", count=count)

        return count

    async def _save_context(self, context: ConversationContext) -> None:
        """
        Save context to Redis.

        Args:
            context: Context to save
        """
        redis = await self._get_redis()
        key = self._get_session_key(context.session_id)

        # Serialize context
        data = json.dumps(context.to_dict())

        # Save with TTL
        await redis.setex(key, self.session_ttl, data)

    async def _load_context(self, session_id: str) -> ConversationContext | None:
        """
        Load context from Redis.

        Args:
            session_id: Session ID

        Returns:
            ConversationContext or None
        """
        redis = await self._get_redis()
        key = self._get_session_key(session_id)

        # Load data
        data = await redis.get(key)

        if not data:
            return None

        # Deserialize
        context_dict = json.loads(data)
        return ConversationContext.from_dict(context_dict)

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self.logger.info("Redis connection closed")
