"""
HIVEMIND TUI Engine Package

Provides the engine layer connecting TUI to backend services.
"""

from .client import APIClient
from .state import AppState
from .websocket import WebSocketClient

__all__ = ["APIClient", "AppState", "WebSocketClient"]
