"""HIVEMIND Engine Module - v3.0."""

from .auth import AuthManager, AuthStatus, AuthMethod, AuthState
from .codex_head import CodexHead, CodexResponse, ResponseSource
from .claude_agent import ClaudeAgent, AgentResult, AGENTS
from .dialogue import CodexClaudeDialogue, DialogueResult
from .coordinator import Coordinator, RouteType, RouteDecision, ExecutionResult

__all__ = [
    # Auth
    "AuthManager",
    "AuthStatus",
    "AuthMethod",
    "AuthState",

    # Codex Head
    "CodexHead",
    "CodexResponse",
    "ResponseSource",

    # Claude Agent
    "ClaudeAgent",
    "AgentResult",
    "AGENTS",

    # Dialogue
    "CodexClaudeDialogue",
    "DialogueResult",

    # Coordinator (backward compatibility)
    "Coordinator",
    "RouteType",
    "RouteDecision",
    "ExecutionResult",
]
