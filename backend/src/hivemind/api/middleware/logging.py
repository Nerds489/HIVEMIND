"""
Request Logging Middleware

FastAPI middleware for logging all incoming requests and responses.
"""

from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from hivemind.observability import get_logger, log_context

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Request logging middleware for FastAPI.

    Logs all incoming requests with timing, status codes, and correlation IDs.
    """

    def __init__(
        self,
        app,
        *,
        skip_paths: list[str] | None = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
    ):
        """
        Initialize request logging middleware.

        Args:
            app: FastAPI application
            skip_paths: Paths to skip logging (e.g., /health, /metrics)
            log_request_body: Whether to log request bodies (careful with sensitive data)
            log_response_body: Whether to log response bodies (careful with sensitive data)
        """
        super().__init__(app)
        self.skip_paths = skip_paths or ["/health", "/metrics"]
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process request with logging.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response from next middleware
        """
        # Skip logging for certain paths
        if request.url.path in self.skip_paths:
            return await call_next(request)

        # Generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Add correlation ID to request state
        request.state.correlation_id = correlation_id

        # Start timing
        start_time = time.time()

        # Extract request info
        request_info = {
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_host": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }

        # Log request body if enabled (be careful with sensitive data)
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    request_info["body_size"] = len(body)
                    # Don't log the actual body content by default for security
            except Exception:
                pass

        # Add context for all logs in this request
        with log_context(**request_info):
            logger.info(
                f"Request started: {request.method} {request.url.path}",
                extra=request_info,
            )

            # Process request
            try:
                response = await call_next(request)

                # Calculate duration
                duration = time.time() - start_time

                # Extract response info
                response_info = {
                    **request_info,
                    "status_code": response.status_code,
                    "duration_seconds": round(duration, 4),
                }

                # Add response size if available
                if hasattr(response, "headers"):
                    content_length = response.headers.get("content-length")
                    if content_length:
                        response_info["response_size"] = int(content_length)

                # Log based on status code
                if response.status_code >= 500:
                    logger.error(
                        f"Request failed: {request.method} {request.url.path} - {response.status_code}",
                        extra=response_info,
                    )
                elif response.status_code >= 400:
                    logger.warning(
                        f"Request error: {request.method} {request.url.path} - {response.status_code}",
                        extra=response_info,
                    )
                else:
                    logger.info(
                        f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                        extra=response_info,
                    )

                # Add correlation ID to response headers
                response.headers["X-Correlation-ID"] = correlation_id

                return response

            except Exception as e:
                # Calculate duration even on error
                duration = time.time() - start_time

                logger.exception(
                    f"Request exception: {request.method} {request.url.path}",
                    extra={
                        **request_info,
                        "duration_seconds": round(duration, 4),
                        "error": str(e),
                    },
                )
                raise


def get_correlation_id(request: Request) -> str:
    """
    Get correlation ID from request.

    Args:
        request: FastAPI request

    Returns:
        Correlation ID string

    Usage:
        @app.get("/example")
        async def example(request: Request):
            correlation_id = get_correlation_id(request)
            return {"correlation_id": correlation_id}
    """
    return getattr(request.state, "correlation_id", "unknown")
