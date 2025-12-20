"""HIVEMIND TUI - Textual-based Terminal User Interface for HIVEMIND."""

__version__ = "0.1.0"
__author__ = "HIVEMIND Team"
__description__ = "Textual-based TUI for HIVEMIND multi-agent system"

# Lazy import to avoid requiring textual for sub-modules
__all__ = ["HivemindApp"]


def __getattr__(name):
    """Lazy load HivemindApp to avoid requiring textual for sub-modules."""
    if name == "HivemindApp":
        from .app import HivemindApp
        return HivemindApp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
