"""
HIVEMIND Distributed Tracing

OpenTelemetry-based distributed tracing for request correlation across services.
"""

from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache
from typing import Any, Iterator

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import Span, Status, StatusCode, Tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from hivemind.config import get_settings


class TracingManager:
    """
    Distributed tracing manager for HIVEMIND.

    Provides OpenTelemetry-based tracing with support for:
    - OTLP export (Jaeger, Tempo, etc.)
    - Console export (development)
    - Context propagation
    - Span creation and management
    """

    def __init__(self) -> None:
        """Initialize tracing manager."""
        self._tracer: Tracer | None = None
        self._provider: TracerProvider | None = None
        self._propagator = TraceContextTextMapPropagator()

    def configure(
        self,
        service_name: str | None = None,
        service_version: str | None = None,
        endpoint: str | None = None,
        sample_rate: float | None = None,
        console_export: bool = False,
    ) -> None:
        """
        Configure distributed tracing.

        Args:
            service_name: Service name for traces
            service_version: Service version
            endpoint: OTLP exporter endpoint
            sample_rate: Sampling rate (0.0 to 1.0)
            console_export: Enable console export (for development)
        """
        settings = get_settings()
        obs_config = settings.observability

        if not obs_config.tracing_enabled:
            return

        # Create resource with service info
        resource = Resource.create({
            "service.name": service_name or obs_config.service_name,
            "service.version": service_version or obs_config.service_version,
            "deployment.environment": settings.env.value,
        })

        # Create tracer provider
        self._provider = TracerProvider(resource=resource)

        # Add OTLP exporter
        exporter_endpoint = endpoint or obs_config.tracing_endpoint
        if exporter_endpoint:
            otlp_exporter = OTLPSpanExporter(endpoint=exporter_endpoint)
            self._provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        # Add console exporter for development
        if console_export or settings.is_development:
            console_exporter = ConsoleSpanExporter()
            self._provider.add_span_processor(BatchSpanProcessor(console_exporter))

        # Set global tracer provider
        trace.set_tracer_provider(self._provider)

        # Create tracer
        self._tracer = trace.get_tracer(
            service_name or obs_config.service_name,
            service_version or obs_config.service_version,
        )

    @property
    def tracer(self) -> Tracer:
        """Get the configured tracer."""
        if self._tracer is None:
            # Return a no-op tracer if not configured
            return trace.get_tracer("hivemind")
        return self._tracer

    @contextmanager
    def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        kind: trace.SpanKind = trace.SpanKind.INTERNAL,
    ) -> Iterator[Span]:
        """
        Create a new span context.

        Args:
            name: Span name
            attributes: Span attributes
            kind: Span kind (INTERNAL, SERVER, CLIENT, PRODUCER, CONSUMER)

        Yields:
            The created span
        """
        with self.tracer.start_as_current_span(
            name,
            kind=kind,
            attributes=attributes or {},
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    def inject_context(self, carrier: dict[str, str]) -> None:
        """
        Inject trace context into carrier for propagation.

        Args:
            carrier: Dictionary to inject context into (e.g., HTTP headers)
        """
        self._propagator.inject(carrier)

    def extract_context(self, carrier: dict[str, str]) -> trace.Context:
        """
        Extract trace context from carrier.

        Args:
            carrier: Dictionary containing trace context

        Returns:
            Extracted trace context
        """
        return self._propagator.extract(carrier)

    def get_current_span(self) -> Span:
        """Get the current active span."""
        return trace.get_current_span()

    def add_event(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """
        Add an event to the current span.

        Args:
            name: Event name
            attributes: Event attributes
        """
        span = self.get_current_span()
        span.add_event(name, attributes=attributes or {})

    def set_attribute(self, key: str, value: Any) -> None:
        """
        Set an attribute on the current span.

        Args:
            key: Attribute key
            value: Attribute value
        """
        span = self.get_current_span()
        span.set_attribute(key, value)

    def set_error(self, exception: Exception) -> None:
        """
        Mark the current span as errored.

        Args:
            exception: The exception that occurred
        """
        span = self.get_current_span()
        span.set_status(Status(StatusCode.ERROR, str(exception)))
        span.record_exception(exception)

    def shutdown(self) -> None:
        """Shutdown the tracing provider."""
        if self._provider:
            self._provider.shutdown()


@lru_cache
def get_tracer() -> TracingManager:
    """Get cached tracing manager instance."""
    manager = TracingManager()
    settings = get_settings()

    if settings.observability.tracing_enabled:
        manager.configure()

    return manager


def trace_function(
    name: str | None = None,
    attributes: dict[str, Any] | None = None,
):
    """
    Decorator to trace a function.

    Usage:
        @trace_function("my_operation")
        async def my_function():
            ...
    """
    def decorator(func):
        import functools
        import inspect

        span_name = name or func.__name__

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                tracer = get_tracer()
                with tracer.span(span_name, attributes=attributes):
                    return await func(*args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                tracer = get_tracer()
                with tracer.span(span_name, attributes=attributes):
                    return func(*args, **kwargs)
            return sync_wrapper

    return decorator
