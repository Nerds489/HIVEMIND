"""Status Bar Widget - Display connection status and system information."""

from datetime import datetime
from typing import Optional

from rich.table import Table
from rich.text import Text
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


class StatusBar(Widget):
    """Widget to display system status and information."""

    can_focus = False  # Prevent focus stealing from input widgets

    connection_status: reactive[str] = reactive("disconnected")
    active_agent: reactive[Optional[str]] = reactive(None)
    task_progress: reactive[int] = reactive(0)
    total_tasks: reactive[int] = reactive(0)

    def compose(self):
        """Create child widgets."""
        yield Static("", id="status-display")

    def watch_connection_status(self, status: str) -> None:
        """React to connection status changes."""
        self._update_display()

    def watch_active_agent(self, agent: Optional[str]) -> None:
        """React to active agent changes."""
        self._update_display()

    def watch_task_progress(self, progress: int) -> None:
        """React to task progress changes."""
        self._update_display()

    def watch_total_tasks(self, total: int) -> None:
        """React to total tasks changes."""
        self._update_display()

    def _update_display(self) -> None:
        """Update the status display."""
        status_display = self.query_one("#status-display", Static)

        # Build status table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", style="bold")
        table.add_column("Value")

        # Connection status
        status_color = {
            "connected": "green",
            "connecting": "yellow",
            "disconnected": "red",
            "error": "red bold"
        }.get(self.connection_status, "white")

        status_icon = {
            "connected": "✓",
            "connecting": "◐",
            "disconnected": "✗",
            "error": "⚠"
        }.get(self.connection_status, "○")

        table.add_row(
            "Connection:",
            f"[{status_color}]{status_icon} {self.connection_status.title()}[/{status_color}]"
        )

        # Active agent
        agent_display = self.active_agent or "[dim]None[/dim]"
        table.add_row("Active Agent:", agent_display)

        # Task progress
        if self.total_tasks > 0:
            progress_pct = int((self.task_progress / self.total_tasks) * 100)
            progress_bar = self._create_progress_bar(progress_pct)
            table.add_row(
                "Tasks:",
                f"{self.task_progress}/{self.total_tasks} {progress_bar}"
            )
        else:
            table.add_row("Tasks:", "[dim]No active tasks[/dim]")

        # System info
        table.add_row("", "")  # Spacer
        table.add_row("[bold cyan]SYSTEM INFO[/bold cyan]", "")

        # Current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table.add_row("Time:", current_time)

        # API endpoint
        app = self.app
        if hasattr(app, 'api_base_url'):
            table.add_row("API:", f"[dim]{app.api_base_url}[/dim]")

        status_display.update(table)

    def _create_progress_bar(self, percentage: int, width: int = 10) -> str:
        """Create a simple text progress bar.

        Args:
            percentage: Progress percentage (0-100)
            width: Width of the progress bar in characters

        Returns:
            Formatted progress bar string
        """
        filled = int((percentage / 100) * width)
        empty = width - filled

        bar = "█" * filled + "░" * empty
        color = "green" if percentage == 100 else "yellow" if percentage > 50 else "red"

        return f"[{color}]{bar}[/{color}] {percentage}%"

    def set_connection_status(self, status: str) -> None:
        """Set the connection status.

        Args:
            status: Status string (connected, connecting, disconnected, error)
        """
        self.connection_status = status

    def set_active_agent(self, agent_name: Optional[str]) -> None:
        """Set the active agent.

        Args:
            agent_name: Name of the active agent or None
        """
        self.active_agent = agent_name

    def set_task_progress(self, completed: int, total: int) -> None:
        """Set task progress.

        Args:
            completed: Number of completed tasks
            total: Total number of tasks
        """
        self.task_progress = completed
        self.total_tasks = total

    def on_mount(self) -> None:
        """Handle widget mount."""
        self._update_display()
        # Update display every second
        self.set_interval(1.0, self._update_display)
