"""Main Screen - Three-panel layout for HIVEMIND."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from ..widgets.agent_list import AgentListWidget
from ..widgets.message_view import MessageView
from ..widgets.status_bar import StatusBar


class MainScreen(Screen):
    """Main screen with three-panel layout: agents, chat, and status."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            with Horizontal(id="content-area"):
                # Left panel: Agent list
                with Vertical(id="agent-panel", classes="panel"):
                    yield Static("AGENT TEAMS", classes="panel-title")
                    yield AgentListWidget(id="agent-list")

                # Center panel: Message view
                with Vertical(id="chat-panel", classes="panel"):
                    yield Static("MESSAGE HISTORY", classes="panel-title")
                    yield MessageView(id="message-view")

                # Right panel: Status and info
                with Vertical(id="status-panel", classes="panel"):
                    yield Static("SYSTEM STATUS", classes="panel-title")
                    yield StatusBar(id="status-bar")

        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount event."""
        self.query_one("#agent-list", AgentListWidget).focus()


class WelcomeMessage(Static):
    """Welcome message widget for the main screen."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(self._get_welcome_text())

    def _get_welcome_text(self) -> str:
        """Generate welcome text."""
        return """
[bold cyan]Welcome to HIVEMIND Command Center[/bold cyan]

[yellow]24 AI Agents Ready[/yellow]
[green]6 Specialized Teams Active[/green]

[dim]Use the controls below to:[/dim]
- Select an agent from the left panel
- View messages in the center panel
- Monitor status in the right panel

[dim]Press '?' for help, 'c' for chat mode, 'q' to quit[/dim]
"""
