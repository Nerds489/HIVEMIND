"""
Rate Limiting Middleware

FastAPI middleware for per-endpoint and per-user rate limiting.
"""

from __future__ import annotations

import time
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from hivemind.observability import get_logger
from hivemind.security.rate_limit import RateLimitExceeded, get_rate_limiter

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for FastAPI.

    Enforces per-endpoint and per-user rate limits using Redis-based sliding window.
    """

    def __init__(
        self,
        app,
        *,
        default_requests: int = 100,
        default_window: int = 60,
        endpoint_limits: dict[str, tuple[int, int]] | None = None,
    ):
        """
        Initialize rate limiting middleware.

        Args:
            app: FastAPI application
            default_requests: Default max requests per window
            default_window: Default window size in seconds
            endpoint_limits: Per-endpoint limits as {path: (requests, window)}
        """
        super().__init__(app)
        self.default_requests = default_requests
        self.default_window = default_window
        self.endpoint_limits = endpoint_limits or {}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process request with rate limiting.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response from next middleware or 429 if rate limited
        """
        # Skip rate limiting for health checks and metrics
        if request.url.path in ["/health", "/ready", "/metrics"]:
            return await call_next(request)

        # Determine rate limit for this endpoint
        path = request.url.path
        max_requests, window = self.endpoint_limits.get(
            path,
            (self.default_requests, self.default_window),
        )

        # Build identifier from IP and optional user ID
        identifier = self._get_identifier(request)

        try:
            # Check rate limit
            limiter = await get_rate_limiter()
            allowed, retry_after = await limiter.check_rate_limit(
                identifier=identifier,
                max_requests=max_requests,
                window_seconds=window,
            )

            if not allowed:
                logger.warning(
                    f"Rate limit exceeded for {identifier}",
                    extra={
                        "identifier": identifier,
                        "path": path,
                        "retry_after": retry_after,
                    },
                )

                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "rate_limit_exceeded",
                        "message": f"Rate limit exceeded. Retry after {int(retry_after)} seconds.",
                        "retry_after": int(retry_after),
                    },
                    headers={
                        "Retry-After": str(int(retry_after)),
                        "X-RateLimit-Limit": str(max_requests),
                        "X-RateLimit-Window": str(window),
                    },
                )

            # Get current status for response headers
            status_info = await limiter.get_rate_limit_status(
                identifier=identifier,
                window_seconds=window,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers to response
            response.headers["X-RateLimit-Limit"] = str(max_requests)
            response.headers["X-RateLimit-Remaining"] = str(status_info.get("remaining", 0))
            response.headers["X-RateLimit-Window"] = str(window)

            return response

        except RateLimitExceeded as e:
            # Should not happen as we check before, but handle anyway
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "rate_limit_exceeded",
                    "message": str(e),
                    "retry_after": int(e.retry_after),
                },
                headers={
                    "Retry-After": str(int(e.retry_after)),
                },
            )
        except Exception as e:
            # Fail open - allow request if rate limiter fails
            logger.error(
                f"Rate limiter error: {e}",
                extra={"error": str(e), "path": path},
            )
            return await call_next(request)

    def _get_identifier(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting.

        Uses user ID from token if available, otherwise IP address.

        Args:
            request: FastAPI request

        Returns:
            Unique identifier string
        """
        # Try to extract user ID from Authorization header
        user_id = None
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            # Import here to avoid circular dependency
            from hivemind.api.middleware.auth import get_user_id_from_token
            user_id = get_user_id_from_token(token)

        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        # Check for forwarded IP first (if behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"

        return f"ip:{ip}"


def get_endpoint_limits() -> dict[str, tuple[int, int]]:
    """
    Get rate limits for specific endpoints.

    Returns:
        Dict mapping endpoint paths to (requests, window_seconds) tuples

    Usage:
        Customize rate limits for specific endpoints:
        - Authentication endpoints: stricter limits
        - Public endpoints: generous limits
        - Compute-intensive endpoints: lower limits
    """
    return {
        # Authentication - strict limits
        "/api/v1/auth/login": (10, 60),  # 10 requests per minute
        "/api/v1/auth/register": (5, 300),  # 5 requests per 5 minutes
        "/api/v1/auth/refresh": (20, 60),  # 20 requests per minute

        # Completions - moderate limits (compute-intensive)
        "/api/v1/completions": (30, 60),  # 30 requests per minute
        "/api/v1/completions/stream": (20, 60),  # 20 requests per minute

        # Tasks - moderate limits
        "/api/v1/tasks": (50, 60),  # 50 requests per minute

        # Sessions - generous limits (lightweight)
        "/api/v1/sessions": (100, 60),  # 100 requests per minute

        # Public endpoints - very generous
        "/api/v1/status": (1000, 60),  # 1000 requests per minute
    }
