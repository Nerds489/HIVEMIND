"""
HIVEMIND Metrics Collection

Prometheus-based metrics for monitoring agent activity, task performance, and system health.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from prometheus_client import Counter, Gauge, Histogram, Info, CollectorRegistry, REGISTRY

if TYPE_CHECKING:
    from prometheus_client.metrics import MetricWrapperBase


class MetricsManager:
    """
    Centralized metrics management for HIVEMIND.

    Provides pre-defined metrics for:
    - Task execution (counts, latencies, errors)
    - Agent utilization
    - API request handling
    - IPC messaging
    - Database operations
    """

    def __init__(self, registry: CollectorRegistry | None = None) -> None:
        """
        Initialize metrics manager.

        Args:
            registry: Prometheus registry (defaults to global REGISTRY)
        """
        self.registry = registry or REGISTRY
        self._init_metrics()

    def _init_metrics(self) -> None:
        """Initialize all HIVEMIND metrics."""

        # =========================================================================
        # Service Info
        # =========================================================================
        self.service_info = Info(
            "hivemind_service",
            "HIVEMIND service information",
            registry=self.registry,
        )

        # =========================================================================
        # Task Metrics
        # =========================================================================
        self.tasks_total = Counter(
            "hivemind_tasks_total",
            "Total number of tasks processed",
            ["status", "team", "agent"],
            registry=self.registry,
        )

        self.tasks_in_progress = Gauge(
            "hivemind_tasks_in_progress",
            "Number of tasks currently in progress",
            ["team", "agent"],
            registry=self.registry,
        )

        self.task_duration_seconds = Histogram(
            "hivemind_task_duration_seconds",
            "Task execution duration in seconds",
            ["team", "agent"],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0),
            registry=self.registry,
        )

        self.task_queue_size = Gauge(
            "hivemind_task_queue_size",
            "Number of tasks waiting in queue",
            ["priority"],
            registry=self.registry,
        )

        # =========================================================================
        # Agent Metrics
        # =========================================================================
        self.agents_active = Gauge(
            "hivemind_agents_active",
            "Number of active agents",
            ["team"],
            registry=self.registry,
        )

        self.agent_state = Gauge(
            "hivemind_agent_state",
            "Current agent state (0=idle, 1=pending, 2=running, 3=error)",
            ["team", "agent"],
            registry=self.registry,
        )

        self.agent_executions_total = Counter(
            "hivemind_agent_executions_total",
            "Total agent executions",
            ["team", "agent", "status"],
            registry=self.registry,
        )

        # =========================================================================
        # CLI Execution Metrics
        # =========================================================================
        self.cli_executions_total = Counter(
            "hivemind_cli_executions_total",
            "Total CLI executions",
            ["cli_type", "status"],  # cli_type: claude, codex
            registry=self.registry,
        )

        self.cli_duration_seconds = Histogram(
            "hivemind_cli_duration_seconds",
            "CLI execution duration in seconds",
            ["cli_type"],
            buckets=(1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0),
            registry=self.registry,
        )

        self.cli_tokens_used = Counter(
            "hivemind_cli_tokens_used",
            "Total tokens used by CLI",
            ["cli_type", "token_type"],  # token_type: input, output
            registry=self.registry,
        )

        # =========================================================================
        # API Metrics
        # =========================================================================
        self.http_requests_total = Counter(
            "hivemind_http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status_code"],
            registry=self.registry,
        )

        self.http_request_duration_seconds = Histogram(
            "hivemind_http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint"],
            buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
            registry=self.registry,
        )

        self.websocket_connections = Gauge(
            "hivemind_websocket_connections",
            "Current WebSocket connections",
            registry=self.registry,
        )

        self.grpc_requests_total = Counter(
            "hivemind_grpc_requests_total",
            "Total gRPC requests",
            ["method", "status"],
            registry=self.registry,
        )

        # =========================================================================
        # IPC Metrics
        # =========================================================================
        self.ipc_messages_total = Counter(
            "hivemind_ipc_messages_total",
            "Total IPC messages",
            ["transport", "direction"],  # transport: zeromq, redis, rabbitmq
            registry=self.registry,
        )

        self.ipc_message_size_bytes = Histogram(
            "hivemind_ipc_message_size_bytes",
            "IPC message size in bytes",
            ["transport"],
            buckets=(100, 1000, 10000, 100000, 1000000),
            registry=self.registry,
        )

        self.rabbitmq_queue_depth = Gauge(
            "hivemind_rabbitmq_queue_depth",
            "RabbitMQ queue depth",
            ["queue"],
            registry=self.registry,
        )

        self.dlq_messages_total = Counter(
            "hivemind_dlq_messages_total",
            "Messages sent to dead letter queue",
            ["reason"],
            registry=self.registry,
        )

        # =========================================================================
        # Database Metrics
        # =========================================================================
        self.db_connections_active = Gauge(
            "hivemind_db_connections_active",
            "Active database connections",
            ["database"],  # postgres, qdrant, redis
            registry=self.registry,
        )

        self.db_queries_total = Counter(
            "hivemind_db_queries_total",
            "Total database queries",
            ["database", "operation"],
            registry=self.registry,
        )

        self.db_query_duration_seconds = Histogram(
            "hivemind_db_query_duration_seconds",
            "Database query duration in seconds",
            ["database", "operation"],
            buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0),
            registry=self.registry,
        )

        self.vector_search_results = Histogram(
            "hivemind_vector_search_results",
            "Number of results from vector search",
            ["collection"],
            buckets=(0, 1, 5, 10, 25, 50, 100),
            registry=self.registry,
        )

        # =========================================================================
        # Resilience Metrics
        # =========================================================================
        self.circuit_breaker_state = Gauge(
            "hivemind_circuit_breaker_state",
            "Circuit breaker state (0=closed, 1=open, 2=half-open)",
            ["service"],
            registry=self.registry,
        )

        self.retries_total = Counter(
            "hivemind_retries_total",
            "Total retry attempts",
            ["operation", "attempt"],
            registry=self.registry,
        )

        self.checkpoints_created = Counter(
            "hivemind_checkpoints_created",
            "Checkpoints created for recovery",
            ["task_type"],
            registry=self.registry,
        )

        # =========================================================================
        # Session Metrics
        # =========================================================================
        self.sessions_active = Gauge(
            "hivemind_sessions_active",
            "Active user sessions",
            registry=self.registry,
        )

        self.sessions_total = Counter(
            "hivemind_sessions_total",
            "Total sessions created",
            registry=self.registry,
        )

        self.session_duration_seconds = Histogram(
            "hivemind_session_duration_seconds",
            "Session duration in seconds",
            buckets=(60, 300, 600, 1800, 3600, 7200, 14400),
            registry=self.registry,
        )

    def set_service_info(
        self,
        version: str,
        environment: str,
        **labels: str,
    ) -> None:
        """Set service information labels."""
        self.service_info.info({
            "version": version,
            "environment": environment,
            **labels,
        })


@lru_cache
def get_metrics() -> MetricsManager:
    """Get cached metrics manager instance."""
    return MetricsManager()
