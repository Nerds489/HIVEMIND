"""
Distributed Tracing Middleware

FastAPI middleware for OpenTelemetry distributed tracing.
"""

from __future__ import annotations

from typing import Callable

from fastapi import Request, Response
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from starlette.middleware.base import BaseHTTPMiddleware

from hivemind.observability import get_logger
from hivemind.observability.tracing import get_tracer

logger = get_logger(__name__)


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Distributed tracing middleware for FastAPI.

    Creates OpenTelemetry spans for each request with automatic context propagation.
    """

    def __init__(
        self,
        app,
        *,
        skip_paths: list[str] | None = None,
        capture_headers: bool = True,
        capture_query_params: bool = True,
    ):
        """
        Initialize tracing middleware.

        Args:
            app: FastAPI application
            skip_paths: Paths to skip tracing (e.g., /health, /metrics)
            capture_headers: Whether to capture request headers in span
            capture_query_params: Whether to capture query parameters in span
        """
        super().__init__(app)
        self.skip_paths = skip_paths or ["/health", "/metrics"]
        self.capture_headers = capture_headers
        self.capture_query_params = capture_query_params
        self.tracer = get_tracer()

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process request with tracing.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response from next middleware
        """
        # Skip tracing for certain paths
        if request.url.path in self.skip_paths:
            return await call_next(request)

        # Extract trace context from headers
        carrier = dict(request.headers)
        ctx = self.tracer.extract_context(carrier)

        # Create span for this request
        span_name = f"{request.method} {request.url.path}"

        # Set trace context
        with trace.context_api.attach(ctx):
            with self.tracer.span(
                span_name,
                kind=SpanKind.SERVER,
                attributes=self._get_span_attributes(request),
            ) as span:
                # Store span in request state for access by route handlers
                request.state.span = span

                try:
                    # Process request
                    response = await call_next(request)

                    # Add response attributes
                    span.set_attribute("http.status_code", response.status_code)

                    # Set span status based on HTTP status
                    if response.status_code >= 500:
                        span.set_status(Status(StatusCode.ERROR, "Server Error"))
                    elif response.status_code >= 400:
                        span.set_status(Status(StatusCode.ERROR, "Client Error"))
                    else:
                        span.set_status(Status(StatusCode.OK))

                    # Inject trace context into response headers
                    trace_headers: dict[str, str] = {}
                    self.tracer.inject_context(trace_headers)
                    for key, value in trace_headers.items():
                        response.headers[key] = value

                    return response

                except Exception as e:
                    # Record exception in span
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise

    def _get_span_attributes(self, request: Request) -> dict[str, str]:
        """
        Get OpenTelemetry span attributes from request.

        Args:
            request: FastAPI request

        Returns:
            Dict of span attributes
        """
        attributes = {
            "http.method": request.method,
            "http.url": str(request.url),
            "http.scheme": request.url.scheme,
            "http.host": request.url.hostname or "",
            "http.target": request.url.path,
        }

        # Add client info if available
        if request.client:
            attributes["http.client_ip"] = request.client.host

        # Add query parameters if enabled
        if self.capture_query_params and request.query_params:
            for key, value in request.query_params.items():
                # Avoid capturing sensitive parameters
                if key.lower() not in ["password", "token", "api_key", "secret"]:
                    attributes[f"http.query.{key}"] = value

        # Add selected headers if enabled
        if self.capture_headers:
            # Only capture safe headers
            safe_headers = [
                "user-agent",
                "content-type",
                "accept",
                "accept-language",
            ]
            for header in safe_headers:
                value = request.headers.get(header)
                if value:
                    attributes[f"http.header.{header}"] = value

        return attributes


def get_current_span(request: Request) -> trace.Span | None:
    """
    Get the current tracing span from request.

    Args:
        request: FastAPI request

    Returns:
        Current span or None if not available

    Usage:
        @app.get("/example")
        async def example(request: Request):
            span = get_current_span(request)
            if span:
                span.set_attribute("custom.attribute", "value")
            return {"message": "ok"}
    """
    return getattr(request.state, "span", None)


def add_span_event(
    request: Request,
    name: str,
    attributes: dict[str, str] | None = None,
) -> None:
    """
    Add an event to the current span.

    Args:
        request: FastAPI request
        name: Event name
        attributes: Event attributes

    Usage:
        @app.post("/task")
        async def create_task(request: Request, task: TaskCreate):
            add_span_event(request, "task.created", {"task_id": task.id})
            return {"id": task.id}
    """
    span = get_current_span(request)
    if span:
        span.add_event(name, attributes=attributes or {})
