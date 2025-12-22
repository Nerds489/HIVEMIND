"""
HIVEMIND API Dependencies

FastAPI dependency injection for core components.
"""

from __future__ import annotations

from functools import lru_cache
from typing import AsyncIterator

from fastapi import Depends, HTTPException, Header, status

from hivemind.agents.pool import AgentPool, get_agent_pool
from hivemind.config import get_settings
from hivemind.core.context import ContextManager
from hivemind.core.coordinator import Coordinator
from hivemind.core.dispatcher import Dispatcher
from hivemind.core.router import Router
from hivemind.observability import get_logger

logger = get_logger(__name__)


# =============================================================================
# Component Dependencies
# =============================================================================

@lru_cache
def get_router_singleton() -> Router:
    """
    Get the global Router instance.

    Returns:
        Router instance
    """
    agent_pool = get_agent_pool()
    router = Router(
        teams=agent_pool.teams,
        agent_pool=agent_pool,
    )
    logger.info("Router singleton created")
    return router


@lru_cache
def get_dispatcher_singleton() -> Dispatcher:
    """
    Get the global Dispatcher instance.

    Returns:
        Dispatcher instance
    """
    dispatcher = Dispatcher()
    logger.info("Dispatcher singleton created")
    return dispatcher


@lru_cache
def get_context_manager_singleton() -> ContextManager:
    """
    Get the global ContextManager instance.

    Returns:
        ContextManager instance
    """
    context_manager = ContextManager()
    logger.info("ContextManager singleton created")
    return context_manager


@lru_cache
def get_coordinator_singleton() -> Coordinator:
    """
    Get the global Coordinator instance.

    Returns:
        Coordinator instance
    """
    router = get_router_singleton()
    dispatcher = get_dispatcher_singleton()
    context_manager = get_context_manager_singleton()

    coordinator = Coordinator(
        router=router,
        dispatcher=dispatcher,
        context_manager=context_manager,
    )
    logger.info("Coordinator singleton created")
    return coordinator


def get_agent_pool_dependency() -> AgentPool:
    """
    Dependency for getting the AgentPool.

    Returns:
        AgentPool instance
    """
    return get_agent_pool()


def get_router(
    router: Router = Depends(get_router_singleton),
) -> Router:
    """
    Dependency for getting the Router.

    Args:
        router: Router singleton

    Returns:
        Router instance
    """
    return router


def get_dispatcher(
    dispatcher: Dispatcher = Depends(get_dispatcher_singleton),
) -> Dispatcher:
    """
    Dependency for getting the Dispatcher.

    Args:
        dispatcher: Dispatcher singleton

    Returns:
        Dispatcher instance
    """
    return dispatcher


def get_context_manager(
    context_manager: ContextManager = Depends(get_context_manager_singleton),
) -> ContextManager:
    """
    Dependency for getting the ContextManager.

    Args:
        context_manager: ContextManager singleton

    Returns:
        ContextManager instance
    """
    return context_manager


def get_coordinator(
    coordinator: Coordinator = Depends(get_coordinator_singleton),
) -> Coordinator:
    """
    Dependency for getting the Coordinator.

    Args:
        coordinator: Coordinator singleton

    Returns:
        Coordinator instance
    """
    return coordinator


# =============================================================================
# Authentication Dependencies (Optional)
# =============================================================================

async def verify_api_key(
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> str | None:
    """
    Verify API key from request header.

    Args:
        x_api_key: API key from header

    Returns:
        API key if valid, None if not required

    Raises:
        HTTPException: If API key is invalid
    """
    settings = get_settings()

    # If API keys are disabled, allow all requests
    if not settings.security.api_keys_enabled:
        return None

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # In production, you would validate against a database or secret store
    # For now, we just check if a key is provided
    # TODO: Implement proper API key validation

    return x_api_key


async def get_current_user(
    api_key: str | None = Depends(verify_api_key),
) -> str | None:
    """
    Get the current user from the API key.

    Args:
        api_key: Verified API key

    Returns:
        User ID or None if anonymous
    """
    if not api_key:
        return None

    # In production, you would look up the user associated with the API key
    # For now, we just return None for anonymous access
    # TODO: Implement user lookup from API key

    return None


# =============================================================================
# Pagination Dependencies
# =============================================================================

class PaginationParams:
    """Pagination parameters."""

    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Initialize pagination parameters.

        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return
        """
        self.skip = max(0, skip)
        self.limit = min(max(1, limit), 1000)  # Cap at 1000


def get_pagination_params(
    skip: int = 0,
    limit: int = 100,
) -> PaginationParams:
    """
    Dependency for pagination parameters.

    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return

    Returns:
        PaginationParams instance
    """
    return PaginationParams(skip=skip, limit=limit)


# =============================================================================
# Cleanup Dependencies
# =============================================================================

async def lifespan_context() -> AsyncIterator[None]:
    """
    Application lifespan context.

    Handles initialization and cleanup of resources.
    """
    # Startup
    logger.info("Initializing dependencies")

    # Initialize singletons
    get_agent_pool()
    get_router_singleton()
    get_dispatcher_singleton()
    get_context_manager_singleton()
    get_coordinator_singleton()

    yield

    # Shutdown
    logger.info("Cleaning up dependencies")

    # Close context manager Redis connection
    context_manager = get_context_manager_singleton()
    await context_manager.close()

    logger.info("Dependencies cleaned up")
