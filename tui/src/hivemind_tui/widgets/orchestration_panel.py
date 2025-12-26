"""
Orchestration Panel Widget - Shows agent status and quality gates.

This panel ONLY appears when agents are actually engaged in work.
It provides real-time status updates during agent execution.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


@dataclass
class AgentStatus:
    """Status of an agent."""
    agent_id: str
    agent_name: str
    status: str  # idle, working, complete, error
    message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class GateStatus:
    """Status of a quality gate."""
    gate_id: str
    gate_name: str
    status: str  # PASSED, BLOCKED, PENDING, SKIPPED


class OrchestrationPanel(Widget):
    """Panel showing active agent orchestration status."""

    can_focus = False  # Prevent focus stealing

    is_active: reactive[bool] = reactive(False)
    current_task: reactive[str] = reactive("")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._agents: Dict[str, AgentStatus] = {}
        self._gates: Dict[str, GateStatus] = {}
        self._started_at: Optional[datetime] = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("", id="orchestration-display")

    def on_mount(self) -> None:
        """Handle mount."""
        self._update_display()

    def start_orchestration(self, task: str) -> None:
        """Start a new orchestration session.

        Args:
            task: Task description
        """
        self.current_task = task
        self.is_active = True
        self._started_at = datetime.now()
        self._agents.clear()
        self._gates.clear()
        self._update_display()

    def stop_orchestration(self) -> None:
        """Stop orchestration session."""
        self.is_active = False
        self._update_display()

    def add_agent(self, agent_id: str, agent_name: str) -> None:
        """Add an agent to the orchestration.

        Args:
            agent_id: Agent ID (e.g., "DEV-001")
            agent_name: Human-readable agent name
        """
        self._agents[agent_id] = AgentStatus(
            agent_id=agent_id,
            agent_name=agent_name,
            status="idle",
            started_at=datetime.now(),
        )
        self._update_display()

    def update_agent_status(
        self,
        agent_id: str,
        status: str,
        message: Optional[str] = None,
    ) -> None:
        """Update agent status.

        Args:
            agent_id: Agent ID
            status: New status (idle, working, complete, error)
            message: Optional status message
        """
        if agent_id in self._agents:
            agent = self._agents[agent_id]
            agent.status = status
            agent.message = message
            if status in ("complete", "error"):
                agent.completed_at = datetime.now()
        else:
            # Agent not yet added, create it
            self._agents[agent_id] = AgentStatus(
                agent_id=agent_id,
                agent_name=agent_id,  # Use ID as name if not known
                status=status,
                message=message,
                started_at=datetime.now(),
            )

        self._update_display()

    def set_gate_status(
        self,
        gate_id: str,
        gate_name: str,
        status: str,
    ) -> None:
        """Set quality gate status.

        Args:
            gate_id: Gate ID (e.g., "G1-DESIGN")
            gate_name: Human-readable gate name
            status: Gate status (PASSED, BLOCKED, PENDING, SKIPPED)
        """
        self._gates[gate_id] = GateStatus(
            gate_id=gate_id,
            gate_name=gate_name,
            status=status,
        )
        self._update_display()

    def clear(self) -> None:
        """Clear all orchestration state."""
        self._agents.clear()
        self._gates.clear()
        self.is_active = False
        self.current_task = ""
        self._started_at = None
        self._update_display()

    def _update_display(self) -> None:
        """Update the display."""
        display = self.query_one("#orchestration-display", Static)

        if not self.is_active and not self._agents:
            display.update("")
            # Use visibility instead of display to avoid layout/event issues
            self.styles.height = 0
            self.styles.min_height = 0
            return

        # Restore height when active
        self.styles.height = "auto"
        self.styles.min_height = 3

        # Build display content
        content = []

        # Header
        if self.current_task:
            content.append(Text(f"TASK: {self.current_task[:50]}...", style="bold cyan"))
            content.append(Text())

        # Agent status table
        if self._agents:
            agent_table = Table(
                show_header=True,
                header_style="bold",
                box=None,
                padding=(0, 1),
            )
            agent_table.add_column("Agent", style="cyan", width=12)
            agent_table.add_column("Status", width=10)
            agent_table.add_column("Info", style="dim")

            for agent_id, agent in self._agents.items():
                status_icon, status_color = self._get_status_display(agent.status)
                status_text = Text(f"{status_icon} {agent.status}", style=status_color)

                agent_table.add_row(
                    f"[{agent_id}]",
                    status_text,
                    agent.message or agent.agent_name,
                )

            content.append(agent_table)

        # Gates
        if self._gates:
            content.append(Text())
            content.append(Text("QUALITY GATES", style="bold yellow"))

            for gate_id, gate in self._gates.items():
                gate_icon, gate_color = self._get_gate_display(gate.status)
                gate_text = Text()
                gate_text.append(f"[GATE] {gate_id}: ", style="dim")
                gate_text.append(f"{gate_icon} {gate.status}", style=gate_color)
                content.append(gate_text)

        display.update(Group(*content))

    def _get_status_display(self, status: str) -> tuple[str, str]:
        """Get status icon and color.

        Args:
            status: Status string

        Returns:
            Tuple of (icon, color)
        """
        status_map = {
            "idle": ("○", "dim"),
            "working": ("◐", "yellow"),
            "complete": ("✓", "green"),
            "error": ("✗", "red"),
        }
        return status_map.get(status, ("○", "white"))

    def _get_gate_display(self, status: str) -> tuple[str, str]:
        """Get gate status icon and color.

        Args:
            status: Gate status string

        Returns:
            Tuple of (icon, color)
        """
        gate_map = {
            "PASSED": ("✓", "green"),
            "BLOCKED": ("✗", "red"),
            "PENDING": ("◐", "yellow"),
            "SKIPPED": ("○", "dim"),
        }
        return gate_map.get(status, ("○", "white"))

    def get_summary(self) -> Dict:
        """Get orchestration summary.

        Returns:
            Dictionary with summary info
        """
        agents_complete = sum(1 for a in self._agents.values() if a.status == "complete")
        agents_error = sum(1 for a in self._agents.values() if a.status == "error")
        gates_passed = sum(1 for g in self._gates.values() if g.status == "PASSED")
        gates_blocked = sum(1 for g in self._gates.values() if g.status == "BLOCKED")

        return {
            "total_agents": len(self._agents),
            "agents_complete": agents_complete,
            "agents_error": agents_error,
            "gates_passed": gates_passed,
            "gates_blocked": gates_blocked,
            "task": self.current_task,
            "started_at": self._started_at,
        }
