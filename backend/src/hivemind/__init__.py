"""
HIVEMIND - Multi-Agent AI Orchestration System

A production-grade system for orchestrating 24 specialized AI agents
across 4 functional teams, presenting as a unified intelligence.

24 Agents | 4 Teams | 1 Unified Intelligence
"""

__version__ = "2.0.0"
__author__ = "HIVEMIND Contributors"
__license__ = "MIT"

from hivemind.config import Settings, get_settings

__all__ = [
    "__version__",
    "Settings",
    "get_settings",
]
