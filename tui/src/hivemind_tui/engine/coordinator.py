"""
HIVEMIND Coordinator - Wrapper for backward compatibility.

This module now wraps CodexHead for backward compatibility with existing code.
All actual logic is in codex_head.py, claude_agent.py, and dialogue.py.
"""

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Callable

from .auth import AuthManager
from .codex_head import CodexHead, ResponseSource
from .claude_agent import AGENTS, AgentResult


class RouteType(str, Enum):
    """Type of route decision - for backward compatibility."""
    DIRECT = "direct"
    AGENT = "agent"
    WORKFLOW = "workflow"


@dataclass
class RouteDecision:
    """Route decision - for backward compatibility."""
    route_type: RouteType
    response: Optional[str] = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    workflow: Optional[str] = None
    task: Optional[str] = None
    error: Optional[str] = None
    raw_response: Optional[str] = None


@dataclass
class ExecutionResult:
    """Execution result - for backward compatibility."""
    success: bool
    response: str
    route_decision: RouteDecision
    agent_results: List[AgentResult] = field(default_factory=list)
    gates_passed: List[str] = field(default_factory=list)
    gates_blocked: List[str] = field(default_factory=list)
    error: Optional[str] = None


# Re-export for backward compatibility
GATES = {
    "G1-DESIGN": {"name": "Design Gate", "required_agents": ["DEV-001"]},
    "G2-SECURITY": {"name": "Security Gate", "required_agents": ["SEC-001", "SEC-002"]},
    "G3-CODE": {"name": "Code Gate", "required_agents": ["DEV-004"]},
    "G4-TEST": {"name": "Test Gate", "required_agents": ["QA-001", "QA-002"]},
    "G5-DEPLOY": {"name": "Deploy Gate", "required_agents": ["INF-005"]},
}


class Coordinator:
    """
    HIVEMIND Coordinator - Wrapper around CodexHead.

    This class maintains backward compatibility with existing TUI code
    while delegating to the new CodexHead architecture.
    """

    def __init__(
        self,
        working_dir: Optional[Path] = None,
        on_status_update: Optional[Callable[[str, str], None]] = None,
        on_agent_update: Optional[Callable[[str, str, str], None]] = None,
    ):
        """Initialize coordinator.

        Args:
            working_dir: Working directory
            on_status_update: Callback for status updates
            on_agent_update: Callback for agent updates
        """
        self.working_dir = working_dir or Path.cwd()
        self.on_status_update = on_status_update
        self.on_agent_update = on_agent_update

        # Create auth manager and Codex head
        self._auth = AuthManager()
        self._codex = CodexHead(
            self._auth,
            working_dir=self.working_dir,
            on_status=self._handle_status,
        )

    def _handle_status(self, message: str) -> None:
        """Handle status updates from Codex."""
        if self.on_status_update:
            self.on_status_update("processing", message)

    def _emit_status(self, status: str, message: str) -> None:
        """Emit status update."""
        if self.on_status_update:
            self.on_status_update(status, message)

    def _emit_agent(self, agent_id: str, status: str, message: str) -> None:
        """Emit agent update."""
        if self.on_agent_update:
            self.on_agent_update(agent_id, status, message)

    async def process_input(self, user_input: str) -> ExecutionResult:
        """Process user input.

        This is the main entry point - delegates to CodexHead.

        Args:
            user_input: User's input text

        Returns:
            ExecutionResult
        """
        self._emit_status("analyzing", "Processing...")

        # Process through CodexHead
        response = await self._codex.process(user_input)

        # Convert to ExecutionResult for backward compatibility
        if response.source == ResponseSource.CODEX_DIRECT:
            route_type = RouteType.DIRECT
        elif response.source == ResponseSource.AGENTS:
            route_type = RouteType.AGENT if len(response.agents_used) == 1 else RouteType.WORKFLOW
        else:
            route_type = RouteType.DIRECT

        # Build agent results
        agent_results = []
        for agent_id in response.agents_used:
            agent_info = AGENTS.get(agent_id, {"name": "Unknown"})
            agent_results.append(AgentResult(
                agent_id=agent_id,
                agent_name=agent_info.get("name", "Unknown"),
                status="complete",
                output="Agent executed as part of workflow",
            ))
            self._emit_agent(agent_id, "complete", f"{agent_info.get('name', 'Unknown')} complete")

        return ExecutionResult(
            success=response.success,
            response=response.content,
            route_decision=RouteDecision(
                route_type=route_type,
                response=response.content if route_type == RouteType.DIRECT else None,
                agent_id=response.agents_used[0] if response.agents_used else None,
            ),
            agent_results=agent_results,
            error=response.error,
        )

    async def classify_input(self, user_input: str) -> RouteDecision:
        """Classify input - for backward compatibility.

        Note: This is no longer used by the new architecture.
        Kept for any code that might call it directly.
        """
        # Just check if Codex would handle alone
        if self._codex._can_handle_alone(user_input):
            return RouteDecision(
                route_type=RouteType.DIRECT,
                response="Will handle directly",
            )
        else:
            return RouteDecision(
                route_type=RouteType.AGENT,
                task=user_input,
            )


# Convenience function
async def process_message(
    message: str,
    working_dir: Optional[Path] = None,
) -> tuple[bool, str, Optional[str]]:
    """Simple interface to process a message.

    Args:
        message: User message
        working_dir: Optional working directory

    Returns:
        Tuple of (success, response, agent_id or None)
    """
    coordinator = Coordinator(working_dir=working_dir)
    result = await coordinator.process_input(message)

    agent_id = None
    if result.agent_results:
        agent_id = result.agent_results[0].agent_id

    return result.success, result.response, agent_id
