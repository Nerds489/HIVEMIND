"""Main Screen - Three-panel layout for HIVEMIND v2.0."""

import os
from pathlib import Path
from typing import Optional, List

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

        self._active_agents: List[str] = []
        self._completed_agents: set[str] = set()

        # Create CodexHead
        self._codex = CodexHead(
            auth_manager=self.auth_manager,
            working_dir=self._launch_dir,
            on_status=self._on_codex_status,
            on_agent_update=self._on_agent_update,
            on_gate_update=self._on_gate_update,
            on_orchestration_start=self._on_orchestration_start,
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
        return """[bold cyan]HIVEMIND v2.0[/bold cyan]

[yellow]Enter[/yellow] - Send message
[yellow]C[/yellow] - Full chat screen
[yellow]Q[/yellow] - Quit
[yellow]D[/yellow] - Toggle dark mode
[yellow]Ctrl+O[/yellow] - Status log
[yellow]Ctrl+C[/yellow] - Cancel task
[yellow]?[/yellow] - Help

[dim]Commands:
/hivemind, /dev, /sec, /infra, /qa
/architect, /pentest, /sre, /reviewer
/status, /recall, /debug
/note <message> (live input during planning/review)[/dim]"""

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the quick chat input
        self.query_one("#quick-chat-input", Input).focus()

        # Add welcome message
        message_view = self.query_one("#message-view", MessageView)
        message_view.add_message(
            role="assistant",
            content="""Welcome to HIVEMIND v2.0 (Minimal Output).

I am HEAD_CODEX. Provide a task and I will route it to agents, show
minimal status updates, enforce quality gates, and generate a final report.

Use /help to see commands.""",
            agent_name="HEAD_CODEX",
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
            self._update_status_display(message)

    def _on_orchestration_start(self, task: str, agents: List[str]) -> None:
        """Handle orchestration start - called from worker thread."""
        try:
            self.app.call_from_thread(self._start_orchestration_ui, task, agents)
        except Exception:
            pass

    def _on_agent_update(self, agent_id: str, status: str, message: str) -> None:
        """Handle agent status updates - called from worker thread."""
        try:
            self.app.call_from_thread(self._update_agent_ui, agent_id, status, message)
        except Exception:
            pass

    def _on_gate_update(self, gate_id: str, status: str) -> None:
        """Handle gate updates - called from worker thread."""
        try:
            self.app.call_from_thread(self._update_gate_ui, gate_id, status)
        except Exception:
            pass

    def _update_status_display(self, message: str) -> None:
        """Update status display on main thread."""
        try:
            status_bar = self.query_one("#status-bar", StatusBar)
            status_bar.set_connection_status("connecting")
            status_bar.set_status_message(message)
            if hasattr(self.app, "log_status"):
                self.app.log_status(message)
            message_view = self.query_one("#message-view", MessageView)
            if self._processing and message:
                message_view.update_last_message(f"[dim italic]{message}[/dim italic]")
        except Exception:
            pass

    def _start_orchestration_ui(self, task: str, agents: List[str]) -> None:
        """Initialize orchestration UI state."""
        orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
        agent_list = self.query_one("#agent-list", AgentListWidget)
        status_bar = self.query_one("#status-bar", StatusBar)

        orch_panel.start_orchestration(task)
        agent_list.reset_all_agents()
        self._active_agents = list(agents)
        self._completed_agents = set()
        status_bar.set_task_progress(0, len(agents))

        for agent_id in agents:
            agent_info = AGENTS.get(agent_id, {})
            orch_panel.add_agent(agent_id, agent_info.get("name", agent_id))

    def _update_agent_ui(self, agent_id: str, status: str, message: str) -> None:
        """Update agent status in UI."""
        agent_list = self.query_one("#agent-list", AgentListWidget)
        orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
        status_bar = self.query_one("#status-bar", StatusBar)

        agent_list.update_agent_status(agent_id, status, message)
        orch_panel.update_agent_status(agent_id, status, message)
        status_bar.set_active_agent(agent_id if status == "working" else None)

        if status in ("complete", "error") and agent_id not in self._completed_agents:
            self._completed_agents.add(agent_id)
            status_bar.set_task_progress(len(self._completed_agents), len(self._active_agents))

    def _update_gate_ui(self, gate_id: str, status: str) -> None:
        """Update gate status in UI."""
        gate_names = {
            "G1-DESIGN": "Design Gate",
            "G2-SECURITY": "Security Gate",
            "G3-CODE": "Code Gate",
            "G4-TEST": "Test Gate",
            "G5-DEPLOY": "Deploy Gate",
        }
        orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
        orch_panel.set_gate_status(gate_id, gate_names.get(gate_id, gate_id), status)

    def action_focus_chat_input(self) -> None:
        """Focus the quick chat input."""
        self.query_one("#quick-chat-input", Input).focus()

    def action_cancel_task(self) -> None:
        """Cancel the current processing task."""
        if self._current_worker and self._processing:
            self._current_worker.cancel()
            self.run_worker(self._codex.cancel_pending(), name="codex_cancel", exclusive=False)
            self._current_worker = None
            message_view = self.query_one("#message-view", MessageView)
            orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
            agent_list = self.query_one("#agent-list", AgentListWidget)
            status_bar = self.query_one("#status-bar", StatusBar)
            message_view.remove_last_message()
            message_view.add_message(
                role="assistant",
                content="[yellow]Task cancelled.[/yellow]",
                agent_name="HEAD_CODEX"
            )
            orch_panel.clear()
            agent_list.reset_all_agents()
            self._processing = False
            status_bar.set_connection_status("connected")
            status_bar.set_status_message("Cancelled")
            if hasattr(self.app, "log_status"):
                self.app.log_status("Cancelled")
            status_bar.set_task_progress(0, 0)
            self._active_agents = []
            self._completed_agents = set()

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

        if not message:
            return
        if message.startswith("/note") or message.startswith("/live") or message.startswith("/feedback"):
            note = message.split(maxsplit=1)[1].strip() if len(message.split()) > 1 else ""
            chat_input.clear()
            self._queue_live_note(note)
            return
        if self._processing:
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
            agent_name="HEAD_CODEX"
        )
        status_bar.set_connection_status("connecting")

        # Run processing in background worker
        self._process_message_async(message)

    def _queue_live_note(self, note: str) -> None:
        """Queue live input for the current operation."""
        message_view = self.query_one("#message-view", MessageView)
        status_bar = self.query_one("#status-bar", StatusBar)

        if not note:
            message_view.add_message(
                role="assistant",
                content="[yellow]Live note requires a message.[/yellow]",
                agent_name="HEAD_CODEX",
            )
            return

        self._codex.add_live_input(note)
        status_text = "Live note queued" if self._processing else "Live note queued (next task)"
        status_bar.set_status_message(status_text)
        if hasattr(self.app, "log_status"):
            self.app.log_status(f"Live input: {note}")
        message_view.add_message(
            role="assistant",
            content=f"[dim]{status_text}: {note}[/dim]",
            agent_name="HEAD_CODEX",
        )

    @work(exclusive=True, thread=False)
    async def _process_message_async(self, message: str) -> None:
        """Process message in background worker (async, non-blocking)."""
        worker = get_current_worker()
        self._current_worker = worker

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
        agent_list = self.query_one("#agent-list", AgentListWidget)
        status_bar = self.query_one("#status-bar", StatusBar)

        # Remove thinking message
        message_view.remove_last_message()

        # Handle response based on source
        if response.source == ResponseSource.CODEX_DIRECT:
            orch_panel.clear()
            agent_list.reset_all_agents()
            status_bar.set_task_progress(0, 0)
            status_bar.set_active_agent(None)
            self._active_agents = []
            self._completed_agents = set()

        # Show response
        if response.success:
            message_view.add_message(
                role="assistant",
                content=response.content,
                agent_name="HEAD_CODEX"
            )
        else:
            message_view.add_message(
                role="assistant",
                content=f"[red]{response.error or 'An error occurred'}[/red]",
                agent_name="HEAD_CODEX"
            )

        status_bar.set_connection_status("connected")
        status_bar.set_status_message("")
        if hasattr(self.app, "log_status"):
            self.app.log_status("Complete")
        message_view.refresh()

    def _handle_error(self, error: str) -> None:
        """Handle processing error."""
        message_view = self.query_one("#message-view", MessageView)
        status_bar = self.query_one("#status-bar", StatusBar)
        orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
        agent_list = self.query_one("#agent-list", AgentListWidget)

        message_view.remove_last_message()
        message_view.add_message(
            role="assistant",
            content=f"[red]Error: {error}[/red]",
            agent_name="HEAD_CODEX"
        )

        orch_panel.clear()
        agent_list.reset_all_agents()
        self._active_agents = []
        self._completed_agents = set()
        status_bar.set_connection_status("connected")
        status_bar.set_status_message("")
        if hasattr(self.app, "log_status"):
            self.app.log_status("Error")
        status_bar.set_task_progress(0, 0)
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
