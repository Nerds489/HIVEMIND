"""
HIVEMIND Structured Logging

Production-grade logging with structlog, supporting JSON and console output formats.
"""

from __future__ import annotations

import logging
import sys
from functools import lru_cache
from typing import Any

import structlog
from structlog.types import Processor

from hivemind.config import LogLevel, get_settings


def add_service_context(
    logger: logging.Logger,
    method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Add service context to log entries."""
    settings = get_settings()
    event_dict["service"] = settings.observability.service_name
    event_dict["version"] = settings.observability.service_version
    event_dict["environment"] = settings.env.value
    return event_dict


def configure_logging(
    level: LogLevel | None = None,
    format_: str | None = None,
    log_file: str | None = None,
) -> None:
    """
    Configure structured logging for HIVEMIND.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_: Output format ('json' or 'console')
        log_file: Optional file path for log output
    """
    settings = get_settings()

    log_level = level or settings.observability.log_level
    log_format = format_ or settings.observability.log_format

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.value),
    )

    # Common processors for all formats
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        add_service_context,
    ]

    # Format-specific processors
    if log_format == "json":
        processors: list[Processor] = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:  # console
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Add file handler if specified
    file_path = log_file or settings.observability.log_file
    if file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(getattr(logging, log_level.value))

        # Use JSON format for file logging
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger().addHandler(file_handler)


@lru_cache(maxsize=128)
def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (defaults to 'hivemind')

    Returns:
        Configured structlog BoundLogger
    """
    return structlog.get_logger(name or "hivemind")


class LoggerMixin:
    """Mixin class providing a logger property."""

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


def log_context(**kwargs: Any) -> structlog.contextvars.bound_contextvars:
    """
    Context manager for adding context to logs.

    Usage:
        with log_context(request_id="123", user_id="456"):
            logger.info("Processing request")
    """
    return structlog.contextvars.bound_contextvars(**kwargs)
