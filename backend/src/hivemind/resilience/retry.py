"""
Retry Logic with Exponential Backoff

Tenacity-based retry decorators with configurable backoff strategies,
jitter, and failure callbacks.
"""

from __future__ import annotations

import asyncio
import functools
from typing import Any, Callable, TypeVar, cast

from tenacity import (
    AsyncRetrying,
    Retrying,
    RetryError,
    before_sleep_log,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
)

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


class RetryConfig:
    """Retry configuration with sensible defaults."""

    def __init__(
        self,
        max_retries: int | None = None,
        base_delay: float | None = None,
        max_delay: float | None = None,
        exponential_base: float | None = None,
        jitter: bool | None = None,
        retry_exceptions: tuple[type[Exception], ...] = (Exception,),
    ):
        """
        Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Exponential backoff multiplier
            jitter: Whether to add random jitter to delays
            retry_exceptions: Tuple of exception types to retry on
        """
        settings = get_settings()
        resilience = settings.resilience

        self.max_retries = max_retries or resilience.max_retries
        self.base_delay = base_delay or resilience.retry_base_delay
        self.max_delay = max_delay or resilience.retry_max_delay
        self.exponential_base = exponential_base or resilience.retry_exponential_base
        self.jitter = jitter if jitter is not None else resilience.retry_jitter
        self.retry_exceptions = retry_exceptions


def retry(
    max_retries: int | None = None,
    base_delay: float | None = None,
    max_delay: float | None = None,
    exponential_base: float | None = None,
    jitter: bool | None = None,
    retry_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """
    Retry decorator for synchronous functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Exponential backoff multiplier
        jitter: Whether to add random jitter to delays
        retry_exceptions: Tuple of exception types to retry on

    Returns:
        Decorated function with retry logic

    Example:
        @retry(max_retries=3, base_delay=1.0)
        def unstable_operation():
            # May fail and be retried
            pass
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        retry_exceptions=retry_exceptions,
    )

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Build wait strategy
            if config.jitter:
                wait_strategy = wait_random_exponential(
                    multiplier=config.base_delay,
                    max=config.max_delay,
                )
            else:
                wait_strategy = wait_exponential(
                    multiplier=config.base_delay,
                    max=config.max_delay,
                    exp_base=config.exponential_base,
                )

            retryer = Retrying(
                stop=stop_after_attempt(config.max_retries),
                wait=wait_strategy,
                retry=retry_if_exception_type(config.retry_exceptions),
                before_sleep=before_sleep_log(logger, "WARNING"),
                reraise=True,
            )

            try:
                return retryer(func, *args, **kwargs)
            except RetryError as e:
                logger.error(
                    f"Function {func.__name__} failed after {config.max_retries} retries",
                    extra={
                        "function": func.__name__,
                        "max_retries": config.max_retries,
                        "last_exception": str(e.last_attempt.exception()),
                    },
                )
                raise e.last_attempt.exception() from e

        return cast(F, wrapper)

    return decorator


def async_retry(
    max_retries: int | None = None,
    base_delay: float | None = None,
    max_delay: float | None = None,
    exponential_base: float | None = None,
    jitter: bool | None = None,
    retry_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """
    Retry decorator for async functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Exponential backoff multiplier
        jitter: Whether to add random jitter to delays
        retry_exceptions: Tuple of exception types to retry on

    Returns:
        Decorated async function with retry logic

    Example:
        @async_retry(max_retries=3, base_delay=1.0)
        async def unstable_async_operation():
            # May fail and be retried
            pass
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        retry_exceptions=retry_exceptions,
    )

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Build wait strategy
            if config.jitter:
                wait_strategy = wait_random_exponential(
                    multiplier=config.base_delay,
                    max=config.max_delay,
                )
            else:
                wait_strategy = wait_exponential(
                    multiplier=config.base_delay,
                    max=config.max_delay,
                    exp_base=config.exponential_base,
                )

            retryer = AsyncRetrying(
                stop=stop_after_attempt(config.max_retries),
                wait=wait_strategy,
                retry=retry_if_exception_type(config.retry_exceptions),
                before_sleep=before_sleep_log(logger, "WARNING"),
                reraise=True,
            )

            try:
                return await retryer(func, *args, **kwargs)
            except RetryError as e:
                logger.error(
                    f"Async function {func.__name__} failed after {config.max_retries} retries",
                    extra={
                        "function": func.__name__,
                        "max_retries": config.max_retries,
                        "last_exception": str(e.last_attempt.exception()),
                    },
                )
                raise e.last_attempt.exception() from e

        return cast(F, wrapper)

    return decorator


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int | None = None,
    base_delay: float | None = None,
    max_delay: float | None = None,
    retry_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> T:
    """
    Execute a function with retry and exponential backoff (functional style).

    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        retry_exceptions: Tuple of exception types to retry on

    Returns:
        Function result

    Raises:
        Last exception if all retries fail

    Example:
        result = retry_with_backoff(
            lambda: risky_operation(),
            max_retries=3,
            base_delay=1.0
        )
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        retry_exceptions=retry_exceptions,
    )

    wait_strategy = wait_exponential(
        multiplier=config.base_delay,
        max=config.max_delay,
        exp_base=config.exponential_base,
    )

    retryer = Retrying(
        stop=stop_after_attempt(config.max_retries),
        wait=wait_strategy,
        retry=retry_if_exception_type(config.retry_exceptions),
        before_sleep=before_sleep_log(logger, "WARNING"),
        reraise=True,
    )

    try:
        return retryer(func)
    except RetryError as e:
        logger.error(
            f"Function failed after {config.max_retries} retries",
            extra={
                "max_retries": config.max_retries,
                "last_exception": str(e.last_attempt.exception()),
            },
        )
        raise e.last_attempt.exception() from e
