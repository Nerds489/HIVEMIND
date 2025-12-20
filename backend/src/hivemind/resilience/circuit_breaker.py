"""
Circuit Breaker Pattern

Pybreaker wrapper for fail-fast behavior to prevent cascading failures.
Automatically opens circuit after threshold failures and recovers after timeout.
"""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

import pybreaker

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class CircuitBreaker:
    """
    Circuit breaker for protecting external service calls.

    States:
        - CLOSED: Normal operation, requests pass through
        - OPEN: Circuit tripped, requests fail immediately
        - HALF_OPEN: Testing if service recovered
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int | None = None,
        recovery_timeout: float | None = None,
        expected_exception: type[Exception] = Exception,
    ):
        """
        Initialize circuit breaker.

        Args:
            name: Unique identifier for this circuit
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type that triggers circuit
        """
        settings = get_settings()
        resilience = settings.resilience

        self.name = name
        self.failure_threshold = failure_threshold or resilience.circuit_failure_threshold
        self.recovery_timeout = recovery_timeout or resilience.circuit_recovery_timeout

        # Create pybreaker circuit breaker
        self._breaker = pybreaker.CircuitBreaker(
            fail_max=self.failure_threshold,
            reset_timeout=self.recovery_timeout,
            exclude=[KeyboardInterrupt, SystemExit],
            name=self.name,
            listeners=[CircuitBreakerListener(self.name)],
        )

        logger.info(
            f"Circuit breaker '{name}' initialized",
            extra={
                "circuit_name": name,
                "failure_threshold": self.failure_threshold,
                "recovery_timeout": self.recovery_timeout,
            },
        )

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Execute function through circuit breaker.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerError: If circuit is open
        """
        try:
            return self._breaker.call(func, *args, **kwargs)
        except pybreaker.CircuitBreakerError as e:
            logger.warning(
                f"Circuit breaker '{self.name}' is open",
                extra={
                    "circuit_name": self.name,
                    "state": str(self._breaker.current_state),
                },
            )
            raise

    @property
    def state(self) -> str:
        """Get current circuit state."""
        return str(self._breaker.current_state)

    @property
    def is_open(self) -> bool:
        """Check if circuit is open."""
        return self._breaker.current_state == pybreaker.STATE_OPEN

    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed."""
        return self._breaker.current_state == pybreaker.STATE_CLOSED

    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        return self._breaker.fail_counter

    def reset(self) -> None:
        """Manually reset circuit to closed state."""
        self._breaker.call_succeeded()
        logger.info(
            f"Circuit breaker '{self.name}' manually reset",
            extra={"circuit_name": self.name},
        )


class CircuitBreakerListener(pybreaker.CircuitBreakerListener):
    """Listener for circuit breaker state changes."""

    def __init__(self, circuit_name: str):
        """Initialize listener with circuit name."""
        self.circuit_name = circuit_name

    def state_change(
        self, cb: pybreaker.CircuitBreaker, old_state: str, new_state: str
    ) -> None:
        """Handle state change events."""
        logger.warning(
            f"Circuit breaker '{self.circuit_name}' state changed",
            extra={
                "circuit_name": self.circuit_name,
                "old_state": str(old_state),
                "new_state": str(new_state),
                "failure_count": cb.fail_counter,
            },
        )

    def before_call(self, cb: pybreaker.CircuitBreaker, func: Callable) -> None:
        """Called before executing function."""
        logger.debug(
            f"Circuit breaker '{self.circuit_name}' executing call",
            extra={
                "circuit_name": self.circuit_name,
                "function": func.__name__,
                "state": str(cb.current_state),
            },
        )

    def success(self, cb: pybreaker.CircuitBreaker) -> None:
        """Called after successful execution."""
        logger.debug(
            f"Circuit breaker '{self.circuit_name}' call succeeded",
            extra={
                "circuit_name": self.circuit_name,
                "state": str(cb.current_state),
            },
        )

    def failure(self, cb: pybreaker.CircuitBreaker, exc: Exception) -> None:
        """Called after failed execution."""
        logger.warning(
            f"Circuit breaker '{self.circuit_name}' call failed",
            extra={
                "circuit_name": self.circuit_name,
                "state": str(cb.current_state),
                "failure_count": cb.fail_counter,
                "exception": str(exc),
            },
        )


# Global circuit breaker registry
_circuit_breakers: dict[str, CircuitBreaker] = {}


def get_circuit_breaker(
    name: str,
    failure_threshold: int | None = None,
    recovery_timeout: float | None = None,
) -> CircuitBreaker:
    """
    Get or create a circuit breaker by name.

    Args:
        name: Circuit breaker name
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before attempting recovery

    Returns:
        Circuit breaker instance
    """
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(
            name=name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )
    return _circuit_breakers[name]


def circuit_breaker(
    name: str | None = None,
    failure_threshold: int | None = None,
    recovery_timeout: float | None = None,
) -> Callable[[F], F]:
    """
    Decorator to wrap function with circuit breaker.

    Args:
        name: Circuit breaker name (defaults to function name)
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before attempting recovery

    Returns:
        Decorated function with circuit breaker protection

    Example:
        @circuit_breaker(name="external_api", failure_threshold=5)
        def call_external_api():
            # Protected call
            pass
    """

    def decorator(func: F) -> F:
        circuit_name = name or f"circuit_{func.__module__}.{func.__name__}"
        cb = get_circuit_breaker(
            name=circuit_name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return cb.call(func, *args, **kwargs)

        # Attach circuit breaker to wrapper for introspection
        wrapper._circuit_breaker = cb  # type: ignore

        return wrapper  # type: ignore

    return decorator
