"""
FastAPI Middleware Package

Middleware components for security, observability, and request handling.
"""

from hivemind.api.middleware.auth import (
    get_current_user,
    optional_auth,
    require_role,
)
from hivemind.api.middleware.logging import RequestLoggingMiddleware
from hivemind.api.middleware.rate_limit import RateLimitMiddleware
from hivemind.api.middleware.tracing import TracingMiddleware
from hivemind.api.middleware.validation import ValidationMiddleware

__all__ = [
    "get_current_user",
    "optional_auth",
    "require_role",
    "RequestLoggingMiddleware",
    "RateLimitMiddleware",
    "TracingMiddleware",
    "ValidationMiddleware",
]
