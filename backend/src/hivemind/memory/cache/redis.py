"""
Redis cache for fast temporary storage.

Provides session context caching, TTL-based expiration, and key management.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

import redis.asyncio as aioredis

from hivemind.config import get_settings


class RedisCache:
    """
    Redis-based cache for temporary memory storage.

    Provides fast access to session contexts, agent states, and other
    temporary data with automatic expiration.
    """

    def __init__(self, client: aioredis.Redis | None = None):
        """
        Initialize Redis cache.

        Args:
            client: Optional Redis client. If None, creates from config.
        """
        if client is None:
            settings = get_settings()
            client = aioredis.from_url(
                settings.redis.url,
                max_connections=settings.redis.max_connections,
                socket_timeout=settings.redis.socket_timeout,
                socket_connect_timeout=settings.redis.socket_connect_timeout,
                retry_on_timeout=settings.redis.retry_on_timeout,
                decode_responses=True,
            )
        self._client = client
        self._settings = get_settings()

    async def close(self) -> None:
        """Close the Redis connection."""
        await self._client.close()

    def _make_key(self, *parts: str | UUID) -> str:
        """
        Create a prefixed cache key.

        Args:
            parts: Key parts to join

        Returns:
            Prefixed key string
        """
        key_parts = [str(part) for part in parts]
        key = ":".join(key_parts)
        return f"{self._settings.redis.key_prefix}{key}"

    # =========================================================================
    # Basic Operations
    # =========================================================================

    async def get(self, key: str) -> str | None:
        """
        Get a value by key.

        Args:
            key: Cache key (will be prefixed automatically)

        Returns:
            Value or None if not found
        """
        full_key = self._make_key(key)
        return await self._client.get(full_key)

    async def get_json(self, key: str) -> Any | None:
        """
        Get a JSON value by key.

        Args:
            key: Cache key (will be prefixed automatically)

        Returns:
            Deserialized JSON or None if not found
        """
        value = await self.get(key)
        if value is not None:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ) -> None:
        """
        Set a value with optional TTL.

        Args:
            key: Cache key (will be prefixed automatically)
            value: Value to store
            ttl: Time to live in seconds. Uses default if None.
        """
        full_key = self._make_key(key)
        if ttl is None:
            ttl = self._settings.redis.default_ttl
        await self._client.set(full_key, value, ex=ttl)

    async def set_json(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        """
        Set a JSON value with optional TTL.

        Args:
            key: Cache key (will be prefixed automatically)
            value: Value to serialize and store
            ttl: Time to live in seconds. Uses default if None.
        """
        json_value = json.dumps(value)
        await self.set(key, json_value, ttl)

    async def delete(self, key: str) -> None:
        """
        Delete a key.

        Args:
            key: Cache key (will be prefixed automatically)
        """
        full_key = self._make_key(key)
        await self._client.delete(full_key)

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists.

        Args:
            key: Cache key (will be prefixed automatically)

        Returns:
            True if key exists
        """
        full_key = self._make_key(key)
        return bool(await self._client.exists(full_key))

    async def expire(self, key: str, ttl: int) -> None:
        """
        Set expiration on an existing key.

        Args:
            key: Cache key (will be prefixed automatically)
            ttl: Time to live in seconds
        """
        full_key = self._make_key(key)
        await self._client.expire(full_key, ttl)

    async def ttl(self, key: str) -> int:
        """
        Get remaining TTL for a key.

        Args:
            key: Cache key (will be prefixed automatically)

        Returns:
            Remaining seconds, -1 if no expiration, -2 if key doesn't exist
        """
        full_key = self._make_key(key)
        return await self._client.ttl(full_key)

    # =========================================================================
    # Hash Operations
    # =========================================================================

    async def hget(self, key: str, field: str) -> str | None:
        """
        Get a hash field value.

        Args:
            key: Hash key (will be prefixed automatically)
            field: Field name

        Returns:
            Field value or None if not found
        """
        full_key = self._make_key(key)
        return await self._client.hget(full_key, field)

    async def hget_json(self, key: str, field: str) -> Any | None:
        """
        Get a hash field as JSON.

        Args:
            key: Hash key (will be prefixed automatically)
            field: Field name

        Returns:
            Deserialized JSON or None if not found
        """
        value = await self.hget(key, field)
        if value is not None:
            return json.loads(value)
        return None

    async def hset(self, key: str, field: str, value: str) -> None:
        """
        Set a hash field value.

        Args:
            key: Hash key (will be prefixed automatically)
            field: Field name
            value: Field value
        """
        full_key = self._make_key(key)
        await self._client.hset(full_key, field, value)

    async def hset_json(self, key: str, field: str, value: Any) -> None:
        """
        Set a hash field as JSON.

        Args:
            key: Hash key (will be prefixed automatically)
            field: Field name
            value: Value to serialize
        """
        json_value = json.dumps(value)
        await self.hset(key, field, json_value)

    async def hgetall(self, key: str) -> dict[str, str]:
        """
        Get all fields and values from a hash.

        Args:
            key: Hash key (will be prefixed automatically)

        Returns:
            Dictionary of field->value
        """
        full_key = self._make_key(key)
        return await self._client.hgetall(full_key)

    async def hdel(self, key: str, *fields: str) -> None:
        """
        Delete hash fields.

        Args:
            key: Hash key (will be prefixed automatically)
            fields: Field names to delete
        """
        full_key = self._make_key(key)
        await self._client.hdel(full_key, *fields)

    # =========================================================================
    # List Operations
    # =========================================================================

    async def lpush(self, key: str, *values: str) -> None:
        """
        Push values to the head of a list.

        Args:
            key: List key (will be prefixed automatically)
            values: Values to push
        """
        full_key = self._make_key(key)
        await self._client.lpush(full_key, *values)

    async def rpush(self, key: str, *values: str) -> None:
        """
        Push values to the tail of a list.

        Args:
            key: List key (will be prefixed automatically)
            values: Values to push
        """
        full_key = self._make_key(key)
        await self._client.rpush(full_key, *values)

    async def lpop(self, key: str) -> str | None:
        """
        Pop a value from the head of a list.

        Args:
            key: List key (will be prefixed automatically)

        Returns:
            Popped value or None if list is empty
        """
        full_key = self._make_key(key)
        return await self._client.lpop(full_key)

    async def rpop(self, key: str) -> str | None:
        """
        Pop a value from the tail of a list.

        Args:
            key: List key (will be prefixed automatically)

        Returns:
            Popped value or None if list is empty
        """
        full_key = self._make_key(key)
        return await self._client.rpop(full_key)

    async def lrange(self, key: str, start: int = 0, end: int = -1) -> list[str]:
        """
        Get a range of values from a list.

        Args:
            key: List key (will be prefixed automatically)
            start: Start index
            end: End index (-1 for end of list)

        Returns:
            List of values
        """
        full_key = self._make_key(key)
        return await self._client.lrange(full_key, start, end)

    async def llen(self, key: str) -> int:
        """
        Get the length of a list.

        Args:
            key: List key (will be prefixed automatically)

        Returns:
            List length
        """
        full_key = self._make_key(key)
        return await self._client.llen(full_key)

    # =========================================================================
    # Session Context Operations
    # =========================================================================

    async def store_session_context(
        self,
        session_id: UUID,
        context: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """
        Store session context data.

        Args:
            session_id: Session ID
            context: Context data
            ttl: Time to live. Uses session TTL if None.
        """
        key = f"session:{session_id}:context"
        if ttl is None:
            ttl = self._settings.redis.session_ttl
        await self.set_json(key, context, ttl)

    async def get_session_context(
        self,
        session_id: UUID,
    ) -> dict[str, Any] | None:
        """
        Get session context data.

        Args:
            session_id: Session ID

        Returns:
            Context data or None if not found
        """
        key = f"session:{session_id}:context"
        return await self.get_json(key)

    async def update_session_context(
        self,
        session_id: UUID,
        updates: dict[str, Any],
    ) -> None:
        """
        Update session context (merge with existing).

        Args:
            session_id: Session ID
            updates: Updates to merge
        """
        context = await self.get_session_context(session_id) or {}
        context.update(updates)
        await self.store_session_context(session_id, context)

    async def delete_session_context(self, session_id: UUID) -> None:
        """
        Delete session context.

        Args:
            session_id: Session ID
        """
        key = f"session:{session_id}:context"
        await self.delete(key)

    # =========================================================================
    # Agent State Operations
    # =========================================================================

    async def store_agent_state(
        self,
        agent_id: str,
        task_id: UUID,
        state: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """
        Store agent state for a task.

        Args:
            agent_id: Agent ID
            task_id: Task ID
            state: Agent state
            ttl: Time to live. Uses default if None.
        """
        key = f"agent:{agent_id}:task:{task_id}:state"
        await self.set_json(key, state, ttl)

    async def get_agent_state(
        self,
        agent_id: str,
        task_id: UUID,
    ) -> dict[str, Any] | None:
        """
        Get agent state for a task.

        Args:
            agent_id: Agent ID
            task_id: Task ID

        Returns:
            Agent state or None if not found
        """
        key = f"agent:{agent_id}:task:{task_id}:state"
        return await self.get_json(key)

    async def delete_agent_state(
        self,
        agent_id: str,
        task_id: UUID,
    ) -> None:
        """
        Delete agent state.

        Args:
            agent_id: Agent ID
            task_id: Task ID
        """
        key = f"agent:{agent_id}:task:{task_id}:state"
        await self.delete(key)

    # =========================================================================
    # Task Queue Operations
    # =========================================================================

    async def enqueue_task(
        self,
        queue_name: str,
        task_data: dict[str, Any],
    ) -> None:
        """
        Add a task to a queue.

        Args:
            queue_name: Queue name
            task_data: Task data
        """
        key = f"queue:{queue_name}"
        await self.rpush(key, json.dumps(task_data))

    async def dequeue_task(
        self,
        queue_name: str,
    ) -> dict[str, Any] | None:
        """
        Remove and return a task from a queue.

        Args:
            queue_name: Queue name

        Returns:
            Task data or None if queue is empty
        """
        key = f"queue:{queue_name}"
        value = await self.lpop(key)
        if value:
            return json.loads(value)
        return None

    async def queue_length(self, queue_name: str) -> int:
        """
        Get the length of a queue.

        Args:
            queue_name: Queue name

        Returns:
            Queue length
        """
        key = f"queue:{queue_name}"
        return await self.llen(key)

    # =========================================================================
    # Utility Operations
    # =========================================================================

    async def ping(self) -> bool:
        """
        Ping Redis to check connection.

        Returns:
            True if connected
        """
        try:
            return await self._client.ping()
        except Exception:
            return False

    async def flushdb(self) -> None:
        """
        Flush all keys in the current database.

        WARNING: This deletes all data in the database!
        """
        await self._client.flushdb()
