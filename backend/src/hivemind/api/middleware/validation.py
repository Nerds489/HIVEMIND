"""
Request Validation Middleware

FastAPI middleware for input sanitization and XSS/injection prevention.
"""

from __future__ import annotations

import json
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from hivemind.observability import get_logger
from hivemind.security.validation import ValidationError, sanitize_input

logger = get_logger(__name__)


class ValidationMiddleware(BaseHTTPMiddleware):
    """
    Request validation middleware for FastAPI.

    Sanitizes request bodies to prevent XSS and injection attacks.
    """

    def __init__(
        self,
        app,
        *,
        sanitize_json: bool = True,
        max_body_size: int = 10 * 1024 * 1024,  # 10MB
        skip_paths: list[str] | None = None,
    ):
        """
        Initialize validation middleware.

        Args:
            app: FastAPI application
            sanitize_json: Whether to sanitize JSON request bodies
            max_body_size: Maximum allowed request body size in bytes
            skip_paths: Paths to skip validation (e.g., file uploads)
        """
        super().__init__(app)
        self.sanitize_json = sanitize_json
        self.max_body_size = max_body_size
        self.skip_paths = skip_paths or []

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process request with validation.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response from next middleware
        """
        # Skip validation for certain paths
        if request.url.path in self.skip_paths:
            return await call_next(request)

        # Skip validation for GET requests (no body)
        if request.method == "GET":
            return await call_next(request)

        # Check content type
        content_type = request.headers.get("content-type", "")

        # Only validate JSON requests
        if "application/json" in content_type and self.sanitize_json:
            try:
                # Read request body
                body = await request.body()

                # Check body size
                if len(body) > self.max_body_size:
                    from fastapi.responses import JSONResponse
                    from fastapi import status

                    logger.warning(
                        f"Request body too large: {len(body)} bytes",
                        extra={
                            "path": request.url.path,
                            "size": len(body),
                            "max_size": self.max_body_size,
                        },
                    )

                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "error": "request_too_large",
                            "message": f"Request body exceeds maximum size of {self.max_body_size} bytes",
                        },
                    )

                # Parse and sanitize JSON
                if body:
                    try:
                        data = json.loads(body)
                        sanitized = self._sanitize_data(data)

                        # Replace request body with sanitized version
                        sanitized_body = json.dumps(sanitized).encode("utf-8")

                        async def receive():
                            return {"type": "http.request", "body": sanitized_body}

                        # Create new request with sanitized body
                        request._receive = receive

                        logger.debug(
                            "Request body sanitized",
                            extra={
                                "path": request.url.path,
                                "original_size": len(body),
                                "sanitized_size": len(sanitized_body),
                            },
                        )

                    except json.JSONDecodeError as e:
                        from fastapi.responses import JSONResponse
                        from fastapi import status

                        logger.warning(
                            f"Invalid JSON in request: {e}",
                            extra={"path": request.url.path, "error": str(e)},
                        )

                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "error": "invalid_json",
                                "message": "Request body contains invalid JSON",
                            },
                        )

            except Exception as e:
                logger.error(
                    f"Validation middleware error: {e}",
                    extra={"path": request.url.path, "error": str(e)},
                )
                # Fail open - allow request even if validation fails
                pass

        # Process request
        return await call_next(request)

    def _sanitize_data(self, data: any) -> any:
        """
        Recursively sanitize data structure.

        Args:
            data: Data to sanitize (dict, list, str, or primitive)

        Returns:
            Sanitized data
        """
        if isinstance(data, dict):
            return {
                key: self._sanitize_data(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, str):
            try:
                # Sanitize string values
                # Use lenient settings to avoid breaking valid input
                return sanitize_input(
                    data,
                    max_length=100000,  # 100KB per string
                    allow_empty=True,
                    strip=False,  # Preserve whitespace
                )
            except ValidationError:
                # If sanitization fails, return empty string
                logger.warning(
                    "Failed to sanitize string value",
                    extra={"length": len(data)},
                )
                return ""
        else:
            # Numbers, booleans, None - return as-is
            return data
