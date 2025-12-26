"""Main Screen - Three-panel layout for HIVEMIND v3.0."""

import asyncio
import os
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from textual.binding import Binding

from ..widgets.agent_list import AgentListWidget
from ..widgets.message_view import MessageView
from ..widgets.status_bar import StatusBar
from ..widgets.orchestration_panel import OrchestrationPanel
from ..engine.auth import AuthManager
from ..engine.codex_head import CodexHead, ResponseSource
from ..engine.claude_agent import AGENTS


class MainScreen(Screen):
    """Main screen with three-panel layout."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=False),
        Binding("enter", "focus_chat_input", "Quick Chat", show=True),
        Binding("c", "open_full_chat", "Full Chat", show=True),
        Binding("slash", "focus_chat_input", "/", show=False),
    ]

    def __init__(self, auth_manager: AuthManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_manager = auth_manager
        self._processing = False

        # Get launch directory for context
        self._launch_dir = Path(os.environ.get("HIVEMIND_LAUNCH_DIR", os.getcwd()))

        # Create CodexHead
        self._codex = CodexHead(
            auth_manager=self.auth_manager,
            working_dir=self._launch_dir,
            on_status=self._on_codex_status,
        )

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            # Quick chat bar at top
            with Horizontal(id="quick-chat-bar"):
                yield Input(
                    placeholder="Talk to HIVEMIND... (Enter to send)",
                    id="quick-chat-input"
                )
                yield Button("Send", id="send-btn", variant="primary")
                yield Button("Full Chat [C]", id="full-chat-btn", variant="default")

            with Horizontal(id="content-area"):
                # Left panel: Agent list
                with Vertical(id="agent-panel", classes="panel"):
                    yield Static("AGENTS", classes="panel-title")
                    yield AgentListWidget(id="agent-list")

                # Center panel: Chat and orchestration
                with Vertical(id="chat-panel", classes="panel"):
                    yield Static("RESPONSE", classes="panel-title")
                    yield MessageView(id="message-view")
                    yield OrchestrationPanel(id="orchestration-panel")

                # Right panel: Status and help
                with Vertical(id="status-panel", classes="panel"):
                    yield Static("QUICK HELP", classes="panel-title")
                    yield Static(self._get_help_text(), id="help-text")
                    yield Static("STATUS", classes="panel-title")
                    yield StatusBar(id="status-bar")

        yield Footer()

    def _get_help_text(self) -> str:
        return """[bold cyan]HIVEMIND v3.0[/bold cyan]

[yellow]Enter[/yellow] - Send message
[yellow]C[/yellow] - Full chat screen
[yellow]Q[/yellow] - Quit
[yellow]D[/yellow] - Toggle dark mode
[yellow]?[/yellow] - Help

[dim]I'm your AI assistant.

Simple questions get
direct answers.

Complex work involves
Claude and agents.[/dim]"""

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the quick chat input
        self.query_one("#quick-chat-input", Input).focus()

        # Add welcome message
        message_view = self.query_one("#message-view", MessageView)
        message_view.add_message(
            role="assistant",
            content="""Welcome to HIVEMIND v3.0!

I'm Codex, your AI assistant. You can:
- **Ask me anything** - I'll answer directly
- **Request complex work** - I'll coordinate with Claude and specialist agents

Just type your message above. What can I help you with?""",
            agent_name="Codex"
        )

        # Check for initial prompt
        initial_prompt = os.environ.get("HIVEMIND_INITIAL_PROMPT")
        if initial_prompt:
            os.environ.pop("HIVEMIND_INITIAL_PROMPT", None)
            self.query_one("#quick-chat-input", Input).value = initial_prompt

        # Update status bar
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.set_connection_status("connected")

    def _on_codex_status(self, message: str) -> None:
        """Handle status updates from Codex."""
        try:
            status_bar = self.query_one("#status-bar", StatusBar)
            status_bar.set_connection_status("connecting")
            # Could add status message display here
        except Exception:
            pass

    def action_focus_chat_input(self) -> None:
        """Focus the quick chat input."""
        self.query_one("#quick-chat-input", Input).focus()

    def action_open_full_chat(self) -> None:
        """Open the full chat screen."""
        self.app.action_show_chat()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "send-btn":
            await self._send_message()
        elif event.button.id == "full-chat-btn":
            self.app.action_show_chat()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in quick chat input."""
        if event.input.id == "quick-chat-input":
            await self._send_message()

    async def _send_message(self) -> None:
        """Send message using CodexHead."""
        chat_input = self.query_one("#quick-chat-input", Input)
        message = chat_input.value.strip()

        if not message or self._processing:
            return

        self._processing = True
        message_view = self.query_one("#message-view", MessageView)
        orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
        status_bar = self.query_one("#status-bar", StatusBar)

        # Show user message
        message_view.add_message(role="user", content=message)
        chat_input.value = ""

        # Show thinking indicator
        message_view.add_message(
            role="assistant",
            content="[dim italic]Thinking...[/dim italic]",
            agent_name="Codex"
        )

        try:
            # Process through CodexHead
            response = await self._codex.process(message)

            # Remove thinking message
            message_view.remove_last_message()

            # Handle response based on source
            if response.source == ResponseSource.CODEX_DIRECT:
                # Direct response - clear orchestration
                orch_panel.clear()
                status_bar.set_active_agent(None)
            else:
                # Agents were involved - show orchestration
                if response.agents_used:
                    orch_panel.start_orchestration(message[:50])
                    for agent_id in response.agents_used:
                        agent_info = AGENTS.get(agent_id, {})
                        orch_panel.add_agent(agent_id, agent_info.get("name", agent_id))
                        orch_panel.update_agent_status(agent_id, "complete", "Done")
                        status_bar.set_active_agent(agent_id)

            # Show response
            if response.success:
                message_view.add_message(
                    role="assistant",
                    content=response.content,
                    agent_name="Codex"
                )
            else:
                message_view.add_message(
                    role="assistant",
                    content=f"[red]{response.error or 'An error occurred'}[/red]",
                    agent_name="Codex"
                )

        except Exception as e:
            message_view.remove_last_message()
            message_view.add_message(
                role="assistant",
                content=f"[red]Error: {str(e)}[/red]",
                agent_name="Codex"
            )
        finally:
            self._processing = False
            status_bar.set_connection_status("connected")
            message_view.refresh()
