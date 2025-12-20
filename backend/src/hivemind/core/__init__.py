"""
HIVEMIND Core Module

Contains the central orchestration components:
- Coordinator: Central task management and routing
- Router: Semantic task routing to agents/teams
- Dispatcher: Concurrency control and task execution
- Context: Conversation and session management
"""

__all__ = [
    "Coordinator",
    "Router",
    "Dispatcher",
    "ContextManager",
]

# Lazy imports to avoid circular dependencies
def __getattr__(name: str):
    if name == "Coordinator":
        from hivemind.core.coordinator import Coordinator
        return Coordinator
    elif name == "Router":
        from hivemind.core.router import Router
        return Router
    elif name == "Dispatcher":
        from hivemind.core.dispatcher import Dispatcher
        return Dispatcher
    elif name == "ContextManager":
        from hivemind.core.context import ContextManager
        return ContextManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
