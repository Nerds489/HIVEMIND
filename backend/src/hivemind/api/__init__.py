"""
HIVEMIND API Module

Provides REST, WebSocket, and gRPC interfaces for the orchestration system.
"""

from hivemind.api.server import app, create_app

__all__ = ["app", "create_app"]
