"""
Task Checkpointing for Recovery

Enables long-running tasks to save their progress and resume from
the last checkpoint in case of failure or restart.
"""

from __future__ import annotations

import asyncio
import functools
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

import redis.asyncio as redis

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class CheckpointManager:
    """
    Checkpoint manager for task state persistence.

    Stores task progress in Redis with TTL for automatic cleanup.
    """

    def __init__(self):
        """Initialize checkpoint manager."""
        self.settings = get_settings()
        self._redis: redis.Redis | None = None

    async def connect(self) -> None:
        """Connect to Redis."""
        if self._redis and await self._redis.ping():
            return

        redis_config = self.settings.redis

        try:
            self._redis = redis.Redis(
                host=redis_config.host,
                port=redis_config.port,
                password=redis_config.password.get_secret_value()
                if redis_config.password
                else None,
                db=redis_config.database,
                socket_timeout=redis_config.socket_timeout,
                socket_connect_timeout=redis_config.socket_connect_timeout,
                decode_responses=False,
            )

            await self._redis.ping()

            logger.info(
                "Checkpoint manager connected to Redis",
                extra={
                    "redis_host": redis_config.host,
                    "redis_port": redis_config.port,
                },
            )

        except Exception as e:
            logger.error(
                f"Failed to connect to Redis for checkpointing: {e}",
                extra={"error": str(e)},
            )
            raise

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
            self._redis = None
            logger.info("Checkpoint manager disconnected from Redis")

    async def save_checkpoint(
        self,
        task_id: str,
        checkpoint_data: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """
        Save task checkpoint.

        Args:
            task_id: Unique task identifier
            checkpoint_data: State data to persist
            ttl: Time-to-live in seconds (defaults to config)
        """
        if not self._redis:
            await self.connect()

        ttl = ttl or self.settings.resilience.checkpoint_retention
        key = self._checkpoint_key(task_id)

        # Add metadata
        checkpoint = {
            "task_id": task_id,
            "data": checkpoint_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            await self._redis.setex(
                key,
                ttl,
                json.dumps(checkpoint),
            )

            logger.debug(
                f"Checkpoint saved for task '{task_id}'",
                extra={
                    "task_id": task_id,
                    "ttl": ttl,
                    "data_size": len(json.dumps(checkpoint_data)),
                },
            )

        except Exception as e:
            logger.error(
                f"Failed to save checkpoint for task '{task_id}': {e}",
                extra={"task_id": task_id, "error": str(e)},
            )
            raise

    async def load_checkpoint(self, task_id: str) -> dict[str, Any] | None:
        """
        Load task checkpoint.

        Args:
            task_id: Unique task identifier

        Returns:
            Checkpoint data or None if not found
        """
        if not self._redis:
            await self.connect()

        key = self._checkpoint_key(task_id)

        try:
            data = await self._redis.get(key)

            if data is None:
                logger.debug(
                    f"No checkpoint found for task '{task_id}'",
                    extra={"task_id": task_id},
                )
                return None

            checkpoint = json.loads(data.decode("utf-8"))

            logger.info(
                f"Checkpoint loaded for task '{task_id}'",
                extra={
                    "task_id": task_id,
                    "timestamp": checkpoint.get("timestamp"),
                },
            )

            return checkpoint["data"]

        except Exception as e:
            logger.error(
                f"Failed to load checkpoint for task '{task_id}': {e}",
                extra={"task_id": task_id, "error": str(e)},
            )
            return None

    async def delete_checkpoint(self, task_id: str) -> None:
        """
        Delete task checkpoint.

        Args:
            task_id: Unique task identifier
        """
        if not self._redis:
            await self.connect()

        key = self._checkpoint_key(task_id)

        try:
            await self._redis.delete(key)

            logger.debug(
                f"Checkpoint deleted for task '{task_id}'",
                extra={"task_id": task_id},
            )

        except Exception as e:
            logger.error(
                f"Failed to delete checkpoint for task '{task_id}': {e}",
                extra={"task_id": task_id, "error": str(e)},
            )

    async def list_checkpoints(self, pattern: str = "*") -> list[str]:
        """
        List all checkpoint task IDs matching pattern.

        Args:
            pattern: Redis key pattern (default: all)

        Returns:
            List of task IDs
        """
        if not self._redis:
            await self.connect()

        prefix = self.settings.redis.key_prefix + "checkpoint:"
        full_pattern = prefix + pattern

        try:
            keys = []
            async for key in self._redis.scan_iter(match=full_pattern):
                task_id = key.decode("utf-8").replace(prefix, "")
                keys.append(task_id)

            return keys

        except Exception as e:
            logger.error(
                f"Failed to list checkpoints: {e}",
                extra={"error": str(e)},
            )
            return []

    def _checkpoint_key(self, task_id: str) -> str:
        """Generate Redis key for checkpoint."""
        return f"{self.settings.redis.key_prefix}checkpoint:{task_id}"


# Global checkpoint manager instance
_checkpoint_manager: CheckpointManager | None = None


async def get_checkpoint_manager() -> CheckpointManager:
    """
    Get or create global checkpoint manager instance.

    Returns:
        Checkpoint manager instance
    """
    global _checkpoint_manager

    if _checkpoint_manager is None:
        _checkpoint_manager = CheckpointManager()
        await _checkpoint_manager.connect()

    return _checkpoint_manager


def checkpoint_task(
    task_id_param: str = "task_id",
    checkpoint_interval: int | None = None,
) -> Callable[[F], F]:
    """
    Decorator to add automatic checkpointing to async tasks.

    Args:
        task_id_param: Name of parameter containing task ID
        checkpoint_interval: Seconds between auto-checkpoints

    Returns:
        Decorated function with checkpointing

    Example:
        @checkpoint_task(task_id_param="task_id", checkpoint_interval=60)
        async def long_running_task(task_id: str, context: dict):
            # Task will checkpoint every 60 seconds
            pass
    """
    interval = checkpoint_interval or get_settings().resilience.checkpoint_interval

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract task ID from parameters
            task_id = kwargs.get(task_id_param)
            if task_id is None and args:
                # Try to get from positional args
                import inspect

                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                if task_id_param in params:
                    idx = params.index(task_id_param)
                    if idx < len(args):
                        task_id = args[idx]

            if task_id is None:
                logger.warning(
                    f"Task ID parameter '{task_id_param}' not found, checkpointing disabled",
                    extra={"function": func.__name__},
                )
                return await func(*args, **kwargs)

            manager = await get_checkpoint_manager()

            # Try to load existing checkpoint
            checkpoint_data = await manager.load_checkpoint(task_id)
            if checkpoint_data:
                # Inject checkpoint data into kwargs
                kwargs["_checkpoint"] = checkpoint_data

            # Set up periodic checkpointing in background
            checkpoint_task_handle = None

            async def periodic_checkpoint():
                while True:
                    await asyncio.sleep(interval)
                    # Extract state from context if available
                    context = kwargs.get("context", {})
                    await manager.save_checkpoint(task_id, context)

            if get_settings().resilience.checkpoint_enabled:
                checkpoint_task_handle = asyncio.create_task(periodic_checkpoint())

            try:
                result = await func(*args, **kwargs)

                # Save final checkpoint on success
                await manager.save_checkpoint(
                    task_id, {"status": "completed", "result": str(result)[:1000]}
                )

                return result

            except Exception as e:
                # Save checkpoint on failure
                await manager.save_checkpoint(
                    task_id,
                    {
                        "status": "failed",
                        "error": str(e),
                        "context": kwargs.get("context", {}),
                    },
                )
                raise

            finally:
                # Cancel periodic checkpointing
                if checkpoint_task_handle:
                    checkpoint_task_handle.cancel()
                    try:
                        await checkpoint_task_handle
                    except asyncio.CancelledError:
                        pass

        return wrapper  # type: ignore

    return decorator
