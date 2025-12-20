"""
Health Check Utilities

Component health checks for monitoring system dependencies.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

import redis.asyncio as redis
from qdrant_client import QdrantClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentHealth:
    """
    Health status for a single component.
    """

    def __init__(
        self,
        name: str,
        status: HealthStatus,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        """
        Initialize component health.

        Args:
            name: Component name
            status: Health status
            message: Optional status message
            details: Optional additional details
        """
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "name": self.name,
            "status": self.status.value,
        }
        if self.message:
            result["message"] = self.message
        if self.details:
            result["details"] = self.details
        return result


class HealthCheck:
    """
    Health check coordinator for all system components.

    Performs health checks on databases, caches, and message queues.
    """

    def __init__(self):
        """Initialize health check coordinator."""
        self.settings = get_settings()

    async def check_all(self) -> tuple[HealthStatus, dict[str, Any]]:
        """
        Check health of all components.

        Returns:
            Tuple of (overall_status, component_details)
        """
        components = []

        # Check each component
        components.append(await self.check_postgres())
        components.append(await self.check_redis())
        components.append(await self.check_qdrant())
        components.append(await self.check_rabbitmq())

        # Determine overall status
        statuses = [comp.status for comp in components]

        if all(s == HealthStatus.HEALTHY for s in statuses):
            overall_status = HealthStatus.HEALTHY
        elif any(s == HealthStatus.UNHEALTHY for s in statuses):
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.DEGRADED

        return overall_status, {
            "components": [comp.to_dict() for comp in components]
        }

    async def check_postgres(self) -> ComponentHealth:
        """
        Check PostgreSQL database health.

        Returns:
            Component health status
        """
        try:
            # Create temporary engine for health check
            engine = create_async_engine(
                self.settings.postgres.async_url,
                pool_pre_ping=True,
            )

            async with engine.begin() as conn:
                # Execute simple query
                result = await conn.execute(text("SELECT 1"))
                result.scalar()

            await engine.dispose()

            logger.debug("PostgreSQL health check: healthy")
            return ComponentHealth(
                name="postgres",
                status=HealthStatus.HEALTHY,
                message="Connected",
            )

        except Exception as e:
            logger.error(
                f"PostgreSQL health check failed: {e}",
                extra={"error": str(e)},
            )
            return ComponentHealth(
                name="postgres",
                status=HealthStatus.UNHEALTHY,
                message=f"Connection failed: {str(e)}",
            )

    async def check_redis(self) -> ComponentHealth:
        """
        Check Redis cache health.

        Returns:
            Component health status
        """
        try:
            # Create temporary Redis client
            client = redis.Redis(
                host=self.settings.redis.host,
                port=self.settings.redis.port,
                password=self.settings.redis.password.get_secret_value()
                if self.settings.redis.password
                else None,
                db=self.settings.redis.database,
                socket_timeout=5.0,
                socket_connect_timeout=5.0,
                decode_responses=True,
            )

            # Ping Redis
            await client.ping()

            # Get info
            info = await client.info()
            details = {
                "version": info.get("redis_version"),
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
            }

            await client.close()

            logger.debug("Redis health check: healthy")
            return ComponentHealth(
                name="redis",
                status=HealthStatus.HEALTHY,
                message="Connected",
                details=details,
            )

        except Exception as e:
            logger.error(
                f"Redis health check failed: {e}",
                extra={"error": str(e)},
            )
            return ComponentHealth(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                message=f"Connection failed: {str(e)}",
            )

    async def check_qdrant(self) -> ComponentHealth:
        """
        Check Qdrant vector database health.

        Returns:
            Component health status
        """
        try:
            # Create Qdrant client
            client = QdrantClient(
                host=self.settings.qdrant.host,
                port=self.settings.qdrant.port,
                api_key=self.settings.qdrant.api_key.get_secret_value()
                if self.settings.qdrant.api_key
                else None,
                https=self.settings.qdrant.https,
                timeout=5.0,
            )

            # Get collections
            collections = client.get_collections()

            details = {
                "collections_count": len(collections.collections),
                "collections": [col.name for col in collections.collections],
            }

            logger.debug("Qdrant health check: healthy")
            return ComponentHealth(
                name="qdrant",
                status=HealthStatus.HEALTHY,
                message="Connected",
                details=details,
            )

        except Exception as e:
            logger.error(
                f"Qdrant health check failed: {e}",
                extra={"error": str(e)},
            )
            return ComponentHealth(
                name="qdrant",
                status=HealthStatus.UNHEALTHY,
                message=f"Connection failed: {str(e)}",
            )

    async def check_rabbitmq(self) -> ComponentHealth:
        """
        Check RabbitMQ message queue health.

        Returns:
            Component health status
        """
        try:
            # Import here to avoid hard dependency
            import aio_pika

            # Create RabbitMQ connection
            connection = await aio_pika.connect_robust(
                self.settings.rabbitmq.url,
                timeout=5.0,
            )

            # Create channel
            channel = await connection.channel()

            # Get queue info (declare with passive=True to check without creating)
            try:
                queue = await channel.get_queue(
                    self.settings.rabbitmq.task_queue,
                    ensure=False,
                )
                details = {
                    "queue_name": self.settings.rabbitmq.task_queue,
                    "message_count": queue.declaration_result.message_count,
                    "consumer_count": queue.declaration_result.consumer_count,
                }
            except Exception:
                # Queue doesn't exist yet - that's okay
                details = {
                    "queue_name": self.settings.rabbitmq.task_queue,
                    "message": "Queue not yet created (normal on first start)",
                }

            await connection.close()

            logger.debug("RabbitMQ health check: healthy")
            return ComponentHealth(
                name="rabbitmq",
                status=HealthStatus.HEALTHY,
                message="Connected",
                details=details,
            )

        except ImportError:
            logger.warning("aio_pika not installed, skipping RabbitMQ health check")
            return ComponentHealth(
                name="rabbitmq",
                status=HealthStatus.DEGRADED,
                message="aio_pika not installed",
            )
        except Exception as e:
            logger.error(
                f"RabbitMQ health check failed: {e}",
                extra={"error": str(e)},
            )
            return ComponentHealth(
                name="rabbitmq",
                status=HealthStatus.UNHEALTHY,
                message=f"Connection failed: {str(e)}",
            )

    async def check_component(self, component: str) -> ComponentHealth:
        """
        Check a specific component.

        Args:
            component: Component name (postgres, redis, qdrant, rabbitmq)

        Returns:
            Component health status

        Raises:
            ValueError: If component name is invalid
        """
        check_methods = {
            "postgres": self.check_postgres,
            "redis": self.check_redis,
            "qdrant": self.check_qdrant,
            "rabbitmq": self.check_rabbitmq,
        }

        if component not in check_methods:
            raise ValueError(
                f"Unknown component: {component}. "
                f"Must be one of: {list(check_methods.keys())}"
            )

        return await check_methods[component]()


# Global health check instance
_health_check: HealthCheck | None = None


def get_health_check() -> HealthCheck:
    """
    Get or create global health check instance.

    Returns:
        Health check instance
    """
    global _health_check

    if _health_check is None:
        _health_check = HealthCheck()

    return _health_check
