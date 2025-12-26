"""Main Screen - Three-panel layout for HIVEMIND v3.0."""

import os
from pathlib import Path
from typing import Optional

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from textual.binding import Binding
from textual.worker import Worker, WorkerState, get_current_worker

from ..widgets.agent_list import AgentListWidget
from ..widgets.message_view import MessageView
from ..widgets.status_bar import StatusBar
from ..widgets.orchestration_panel import OrchestrationPanel
from ..engine.auth import AuthManager
from ..engine.codex_head import CodexHead, ResponseSource, CodexResponse
from ..engine.claude_agent import AGENTS


class MainScreen(Screen):
    """Main screen with three-panel layout."""

    # Do NOT bind Enter key at screen level - let Input widget handle it
    BINDINGS = [
        Binding("escape", "focus_chat_input", "Focus Input", show=False),
        Binding("c", "open_full_chat", "Full Chat", show=True),
        Binding("ctrl+c", "cancel_task", "Cancel", show=True),
    ]

    def __init__(self, auth_manager: AuthManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_manager = auth_manager
        self._processing = False
        self._current_worker: Optional[Worker] = None

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
[yellow]Ctrl+C[/yellow] - Cancel task
[yellow]?[/yellow] - Help

[dim]Type in the input box
and press Enter to send.

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
        """Handle status updates from Codex - called from worker thread."""
        try:
            self.app.call_from_thread(self._update_status_display, message)
        except Exception:
            pass

    def _update_status_display(self, message: str) -> None:
        """Update status display on main thread."""
        try:
            status_bar = self.query_one("#status-bar", StatusBar)
            status_bar.set_connection_status("connecting")
            message_view = self.query_one("#message-view", MessageView)
            if self._processing and message:
                message_view.update_last_message(f"[dim italic]{message}[/dim italic]")
        except Exception:
            pass

    def action_focus_chat_input(self) -> None:
        """Focus the quick chat input."""
        self.query_one("#quick-chat-input", Input).focus()

    def action_cancel_task(self) -> None:
        """Cancel the current processing task."""
        if self._current_worker and self._processing:
            self._current_worker.cancel()
            self._current_worker = None
            message_view = self.query_one("#message-view", MessageView)
            message_view.remove_last_message()
            message_view.add_message(
                role="assistant",
                content="[yellow]Task cancelled.[/yellow]",
                agent_name="Codex"
            )
            self._processing = False
            self.query_one("#status-bar", StatusBar).set_connection_status("connected")

    def action_open_full_chat(self) -> None:
        """Open the full chat screen."""
        self.app.action_show_chat()

    # Handle button presses with @on decorator
    @on(Button.Pressed, "#send-btn")
    def handle_send_button(self, event: Button.Pressed) -> None:
        """Handle send button press."""
        self._trigger_send_message()

    @on(Button.Pressed, "#full-chat-btn")
    def handle_full_chat_button(self, event: Button.Pressed) -> None:
        """Handle full chat button press."""
        self.app.action_show_chat()

    # Handle Input submission - this captures Enter key in the Input widget
    @on(Input.Submitted, "#quick-chat-input")
    def handle_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in quick chat input."""
        self._trigger_send_message()

    def _trigger_send_message(self) -> None:
        """Trigger sending a message - starts the background worker."""
        chat_input = self.query_one("#quick-chat-input", Input)
        message = chat_input.value.strip()

        if not message or self._processing:
            return

        self._processing = True
        message_view = self.query_one("#message-view", MessageView)
        status_bar = self.query_one("#status-bar", StatusBar)

        # Show user message
        message_view.add_message(role="user", content=message)
        chat_input.clear()

        # Show thinking indicator
        message_view.add_message(
            role="assistant",
            content="[dim italic]Thinking... (Ctrl+C to cancel)[/dim italic]",
            agent_name="Codex"
        )
        status_bar.set_connection_status("connecting")

        # Run processing in background worker
        self._process_message_async(message)

    @work(exclusive=True, thread=False)
    async def _process_message_async(self, message: str) -> None:
        """Process message in background worker (async, non-blocking)."""
        worker = get_current_worker()

        try:
            # Check for cancellation before starting
            if worker.is_cancelled:
                return

            # Process through Codex
            response = await self._codex.process(message)

            # Check for cancellation after processing
            if worker.is_cancelled:
                return

            # Handle response on main thread
            self._handle_response(response)

        except Exception as e:
            if not worker.is_cancelled:
                self._handle_error(str(e))

        finally:
            self._processing = False
            self._current_worker = None

    def _handle_response(self, response: CodexResponse) -> None:
        """Handle successful response from Codex."""
        message_view = self.query_one("#message-view", MessageView)
        orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
        status_bar = self.query_one("#status-bar", StatusBar)

        # Remove thinking message
        message_view.remove_last_message()

        # Handle response based on source
        if response.source == ResponseSource.CODEX_DIRECT:
            orch_panel.clear()
            status_bar.set_active_agent(None)
        else:
            if response.agents_used:
                orch_panel.start_orchestration("Task")
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

        status_bar.set_connection_status("connected")
        message_view.refresh()

    def _handle_error(self, error: str) -> None:
        """Handle processing error."""
        message_view = self.query_one("#message-view", MessageView)
        status_bar = self.query_one("#status-bar", StatusBar)

        message_view.remove_last_message()
        message_view.add_message(
            role="assistant",
            content=f"[red]Error: {error}[/red]",
            agent_name="Codex"
        )

        status_bar.set_connection_status("connected")
        message_view.refresh()

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle worker state changes for cleanup."""
        if event.state == WorkerState.CANCELLED:
            self._processing = False
            self._current_worker = None
        elif event.state == WorkerState.ERROR:
            self._processing = False
            self._current_worker = None
            # Error already handled in the worker
