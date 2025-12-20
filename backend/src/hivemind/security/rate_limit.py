"""
Rate Limiting

Redis-based rate limiting middleware to prevent abuse and ensure fair usage.
Uses sliding window algorithm for accurate rate limiting.
"""

from __future__ import annotations

import asyncio
import functools
import time
from typing import Any, Callable, TypeVar

import redis.asyncio as redis

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: float):
        """
        Initialize exception.

        Args:
            retry_after: Seconds until rate limit resets
        """
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after:.1f} seconds")


class RateLimiter:
    """
    Redis-based rate limiter using sliding window algorithm.

    Tracks requests per identifier (e.g., user ID, IP address) within
    a time window and enforces limits.
    """

    def __init__(self):
        """Initialize rate limiter."""
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
                decode_responses=True,
            )

            await self._redis.ping()

            logger.info(
                "Rate limiter connected to Redis",
                extra={
                    "redis_host": redis_config.host,
                    "redis_port": redis_config.port,
                },
            )

        except Exception as e:
            logger.error(
                f"Failed to connect to Redis for rate limiting: {e}",
                extra={"error": str(e)},
            )
            raise

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
            self._redis = None
            logger.info("Rate limiter disconnected from Redis")

    async def check_rate_limit(
        self,
        identifier: str,
        max_requests: int | None = None,
        window_seconds: int | None = None,
    ) -> tuple[bool, float]:
        """
        Check if request is within rate limit.

        Args:
            identifier: Unique identifier (user ID, IP, etc.)
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds

        Returns:
            Tuple of (allowed, retry_after_seconds)

        Raises:
            RateLimitExceeded: If rate limit is exceeded
        """
        if not self._redis:
            await self.connect()

        security = self.settings.security
        max_requests = max_requests or security.rate_limit_requests
        window = window_seconds or security.rate_limit_window

        key = self._rate_limit_key(identifier)
        now = time.time()
        window_start = now - window

        try:
            # Use Redis sorted set for sliding window
            async with self._redis.pipeline(transaction=True) as pipe:
                # Remove old entries outside window
                pipe.zremrangebyscore(key, 0, window_start)
                # Count requests in current window
                pipe.zcard(key)
                # Add current request timestamp
                pipe.zadd(key, {str(now): now})
                # Set expiry on key
                pipe.expire(key, window)

                results = await pipe.execute()

            request_count = results[1]  # Count from zcard

            if request_count >= max_requests:
                # Calculate retry after time
                oldest_timestamp = await self._redis.zrange(key, 0, 0)
                if oldest_timestamp:
                    retry_after = float(oldest_timestamp[0]) + window - now
                else:
                    retry_after = window

                logger.warning(
                    f"Rate limit exceeded for '{identifier}'",
                    extra={
                        "identifier": identifier,
                        "request_count": request_count,
                        "max_requests": max_requests,
                        "window_seconds": window,
                        "retry_after": retry_after,
                    },
                )

                return False, max(0, retry_after)

            logger.debug(
                f"Rate limit check passed for '{identifier}'",
                extra={
                    "identifier": identifier,
                    "request_count": request_count + 1,
                    "max_requests": max_requests,
                },
            )

            return True, 0.0

        except Exception as e:
            logger.error(
                f"Rate limit check failed: {e}",
                extra={"identifier": identifier, "error": str(e)},
            )
            # Fail open - allow request if Redis is down
            return True, 0.0

    async def reset_rate_limit(self, identifier: str) -> None:
        """
        Reset rate limit for identifier.

        Args:
            identifier: Unique identifier to reset
        """
        if not self._redis:
            await self.connect()

        key = self._rate_limit_key(identifier)

        try:
            await self._redis.delete(key)

            logger.info(
                f"Rate limit reset for '{identifier}'",
                extra={"identifier": identifier},
            )

        except Exception as e:
            logger.error(
                f"Failed to reset rate limit: {e}",
                extra={"identifier": identifier, "error": str(e)},
            )

    async def get_rate_limit_status(
        self,
        identifier: str,
        window_seconds: int | None = None,
    ) -> dict[str, Any]:
        """
        Get current rate limit status for identifier.

        Args:
            identifier: Unique identifier
            window_seconds: Time window in seconds

        Returns:
            Dict with request count and window info
        """
        if not self._redis:
            await self.connect()

        window = window_seconds or self.settings.security.rate_limit_window
        key = self._rate_limit_key(identifier)
        now = time.time()
        window_start = now - window

        try:
            # Remove old entries and count
            async with self._redis.pipeline(transaction=True) as pipe:
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                results = await pipe.execute()

            request_count = results[1]

            return {
                "identifier": identifier,
                "request_count": request_count,
                "window_seconds": window,
                "max_requests": self.settings.security.rate_limit_requests,
                "remaining": max(
                    0,
                    self.settings.security.rate_limit_requests - request_count,
                ),
            }

        except Exception as e:
            logger.error(
                f"Failed to get rate limit status: {e}",
                extra={"identifier": identifier, "error": str(e)},
            )
            return {
                "identifier": identifier,
                "error": str(e),
            }

    def _rate_limit_key(self, identifier: str) -> str:
        """Generate Redis key for rate limit."""
        return f"{self.settings.redis.key_prefix}rate_limit:{identifier}"


# Global rate limiter instance
_rate_limiter: RateLimiter | None = None


async def get_rate_limiter() -> RateLimiter:
    """
    Get or create global rate limiter instance.

    Returns:
        Rate limiter instance
    """
    global _rate_limiter

    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
        await _rate_limiter.connect()

    return _rate_limiter


def rate_limit(
    identifier_param: str = "user_id",
    max_requests: int | None = None,
    window_seconds: int | None = None,
) -> Callable[[F], F]:
    """
    Decorator to add rate limiting to async functions.

    Args:
        identifier_param: Name of parameter containing identifier
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds

    Returns:
        Decorated function with rate limiting

    Raises:
        RateLimitExceeded: If rate limit is exceeded

    Example:
        @rate_limit(identifier_param="user_id", max_requests=100, window_seconds=60)
        async def api_endpoint(user_id: str, data: dict):
            # Protected endpoint
            pass
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract identifier from parameters
            identifier = kwargs.get(identifier_param)

            if identifier is None and args:
                # Try to get from positional args
                import inspect

                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                if identifier_param in params:
                    idx = params.index(identifier_param)
                    if idx < len(args):
                        identifier = args[idx]

            if identifier is None:
                logger.warning(
                    f"Rate limit identifier '{identifier_param}' not found, skipping rate limit",
                    extra={"function": func.__name__},
                )
                return await func(*args, **kwargs)

            limiter = await get_rate_limiter()

            # Check rate limit
            allowed, retry_after = await limiter.check_rate_limit(
                identifier=str(identifier),
                max_requests=max_requests,
                window_seconds=window_seconds,
            )

            if not allowed:
                raise RateLimitExceeded(retry_after)

            return await func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


async def check_rate_limit(
    identifier: str,
    max_requests: int | None = None,
    window_seconds: int | None = None,
) -> bool:
    """
    Check rate limit for identifier (convenience function).

    Args:
        identifier: Unique identifier
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds

    Returns:
        True if within limit, False otherwise

    Raises:
        RateLimitExceeded: If rate limit is exceeded
    """
    limiter = await get_rate_limiter()
    allowed, retry_after = await limiter.check_rate_limit(
        identifier, max_requests, window_seconds
    )

    if not allowed:
        raise RateLimitExceeded(retry_after)

    return True
