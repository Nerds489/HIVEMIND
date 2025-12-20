"""
HIVEMIND FastAPI Application Server

Main entry point for the REST and WebSocket API.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app

from hivemind import __version__
from hivemind.config import get_settings
from hivemind.observability import configure_logging, get_health_check, get_logger, get_metrics

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    settings = get_settings()

    # Startup
    logger.info(
        "Starting HIVEMIND Backend",
        version=__version__,
        environment=settings.env.value,
    )

    # Configure observability
    configure_logging()

    # Set service info in metrics
    metrics = get_metrics()
    metrics.set_service_info(
        version=__version__,
        environment=settings.env.value,
    )

    # Initialize database connections
    # TODO: Initialize PostgreSQL connection pool
    # TODO: Initialize Qdrant client
    # TODO: Initialize Redis client
    # TODO: Initialize RabbitMQ connection

    logger.info("HIVEMIND Backend started successfully")

    yield

    # Shutdown
    logger.info("Shutting down HIVEMIND Backend")

    # Close connections
    # TODO: Close database connections
    # TODO: Close message queue connections

    logger.info("HIVEMIND Backend shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()

    app = FastAPI(
        title="HIVEMIND API",
        description="Multi-Agent AI Orchestration System - 24 Agents | 4 Teams | 1 Unified Intelligence",
        version=__version__,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        openapi_url="/openapi.json" if settings.is_development else None,
        lifespan=lifespan,
    )

    # Add middleware in correct order (bottom executes first)
    # Order matters: outer middleware wraps inner middleware

    # 1. CORS (outermost - must be first to handle preflight)
    if settings.api.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.api.cors_origins,
            allow_credentials=settings.api.cors_allow_credentials,
            allow_methods=settings.api.cors_allow_methods,
            allow_headers=settings.api.cors_allow_headers,
        )

    # 2. Trusted Host (security)
    if settings.is_production:
        # In production, restrict to specific hosts
        # Note: Configure allowed hosts via environment or config
        # app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.hivemind.com"])
        pass

    # 3. Request Logging (log all requests)
    from hivemind.api.middleware.logging import RequestLoggingMiddleware
    app.add_middleware(
        RequestLoggingMiddleware,
        skip_paths=["/health", "/ready", "/metrics"],
    )

    # 4. Distributed Tracing (trace all requests)
    from hivemind.api.middleware.tracing import TracingMiddleware
    app.add_middleware(
        TracingMiddleware,
        skip_paths=["/health", "/ready", "/metrics"],
    )

    # 5. Rate Limiting (enforce rate limits)
    from hivemind.api.middleware.rate_limit import (
        RateLimitMiddleware,
        get_endpoint_limits,
    )
    app.add_middleware(
        RateLimitMiddleware,
        endpoint_limits=get_endpoint_limits(),
    )

    # 6. Request Validation (sanitize input - innermost)
    from hivemind.api.middleware.validation import ValidationMiddleware
    app.add_middleware(
        ValidationMiddleware,
        skip_paths=["/metrics"],  # Skip metrics endpoint
    )

    # Mount Prometheus metrics endpoint
    if settings.observability.metrics_enabled:
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)

    # Register exception handlers
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle uncaught exceptions."""
        logger.exception(
            "Unhandled exception",
            path=request.url.path,
            method=request.method,
            error=str(exc),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
            },
        )

    # Register routes
    register_routes(app)

    return app


def register_routes(app: FastAPI) -> None:
    """Register all API routes."""

    # Health check endpoints
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        """
        Basic health check endpoint (liveness probe).

        Returns OK if the service is running.
        """
        return {
            "status": "healthy",
            "version": __version__,
        }

    @app.get("/ready", tags=["Health"])
    async def readiness_check() -> dict:
        """
        Readiness check endpoint (readiness probe).

        Verifies all dependencies are accessible before accepting traffic.
        """
        health_checker = get_health_check()
        overall_status, details = await health_checker.check_all()

        # Return 503 if not ready
        if overall_status != "healthy":
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": overall_status,
                    "version": __version__,
                    **details,
                },
            )

        return {
            "status": overall_status,
            "version": __version__,
            **details,
        }

    @app.get("/health/component/{component}", tags=["Health"])
    async def component_health_check(component: str) -> dict:
        """
        Check health of a specific component.

        Args:
            component: Component name (postgres, redis, qdrant, rabbitmq)
        """
        health_checker = get_health_check()

        try:
            result = await health_checker.check_component(component)
            return result.to_dict()
        except ValueError as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "invalid_component",
                    "message": str(e),
                },
            )

    # API version info
    @app.get("/", tags=["Info"])
    async def root() -> dict:
        """API root endpoint."""
        return {
            "name": "HIVEMIND API",
            "version": __version__,
            "description": "24 Agents | 4 Teams | 1 Unified Intelligence",
            "docs": "/docs",
        }

    # Import and register route modules
    from hivemind.api.routes import agents_router, completions_router, sessions_router
    from hivemind.api.websocket import router as websocket_router

    app.include_router(sessions_router)
    app.include_router(completions_router)
    app.include_router(agents_router)
    app.include_router(websocket_router)


# Create application instance
app = create_app()


def main() -> None:
    """Run the server using uvicorn."""
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "hivemind.api.server:app",
        host=settings.api.host,
        port=settings.api.port,
        workers=settings.api.workers if settings.is_production else 1,
        reload=settings.is_development,
        log_level=settings.observability.log_level.value.lower(),
    )


if __name__ == "__main__":
    main()
