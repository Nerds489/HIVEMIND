"""Main Screen - Three-panel layout for HIVEMIND with intelligent routing."""

import asyncio
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
from ..engine.coordinator import Coordinator, RouteType, AGENTS, GATES


class MainScreen(Screen):
    """Main screen with three-panel layout: agents, chat, and status."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=False),
        Binding("enter", "focus_chat_input", "Quick Chat", show=True),
        Binding("c", "open_full_chat", "Full Chat", show=True),
        Binding("slash", "focus_chat_input", "/", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._processing = False
        self._hivemind_dir = Path(__file__).parent.parent.parent.parent.parent.parent
        self._coordinator = Coordinator(
            working_dir=self._hivemind_dir,
            on_status_update=self._on_coordinator_status,
            on_agent_update=self._on_agent_update,
        )

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            # Quick chat bar at top
            with Horizontal(id="quick-chat-bar"):
                yield Input(
                    placeholder="Type here and press Enter to chat with HIVEMIND...",
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
        return """[bold cyan]HIVEMIND Commands[/bold cyan]

[yellow]Enter[/yellow] - Focus chat input
[yellow]C[/yellow] - Open full chat screen
[yellow]Q[/yellow] - Quit
[yellow]D[/yellow] - Toggle dark mode
[yellow]?[/yellow] - Help

[dim]Type your message in the
input bar above and press
Enter to send.

Simple questions get direct
answers. Work tasks route
to specialized agents.[/dim]"""

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the quick chat input for immediate use
        self.query_one("#quick-chat-input", Input).focus()

        # Add welcome message
        message_view = self.query_one("#message-view", MessageView)
        message_view.add_message(
            role="assistant",
            content="""Welcome to HIVEMIND v2.0!

I'm HEAD_CODEX, the master coordinator. I can:
- **Answer questions directly** for simple queries
- **Route to specialized agents** for technical work

Just type your message above. Try "who are you" or ask me to design something!""",
            agent_name="HEAD_CODEX"
        )

        # Update status bar
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.set_connection_status("connected")

    def _on_coordinator_status(self, status: str, message: str) -> None:
        """Handle coordinator status updates."""
        # Update status bar
        try:
            status_bar = self.query_one("#status-bar", StatusBar)
            if status == "analyzing":
                status_bar.set_connection_status("connecting")
            elif status == "workflow":
                status_bar.set_connection_status("connected")
        except Exception:
            pass

    def _on_agent_update(self, agent_id: str, status: str, message: str) -> None:
        """Handle agent status updates."""
        try:
            # Update orchestration panel
            orch_panel = self.query_one("#orchestration-panel", OrchestrationPanel)
            orch_panel.update_agent_status(agent_id, status, message)

            # Update agent list widget
            agent_list = self.query_one("#agent-list", AgentListWidget)
            agent_list.update_agent_status(agent_id, status, message)
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
            await self._send_quick_message()
        elif event.button.id == "full-chat-btn":
            self.app.action_show_chat()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in quick chat input."""
        if event.input.id == "quick-chat-input":
            await self._send_quick_message()

    async def _send_quick_message(self) -> None:
        """Send message from quick chat input using coordinator."""
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

        # Process through coordinator
        try:
            await self._process_with_coordinator(message, message_view, orch_panel, status_bar)
        except Exception as e:
            message_view.add_message(
                role="assistant",
                content=f"[red]Error: {str(e)}[/red]",
                agent_name="HEAD_CODEX"
            )
        finally:
            self._processing = False

    async def _process_with_coordinator(
        self,
        message: str,
        message_view: MessageView,
        orch_panel: OrchestrationPanel,
        status_bar: StatusBar,
    ) -> None:
        """Process message through coordinator with proper UI updates."""

        # Show thinking indicator
        message_view.add_message(
            role="assistant",
            content="[dim italic]Analyzing...[/dim italic]",
            agent_name="HEAD_CODEX"
        )

        # Get routing decision
        result = await self._coordinator.process_input(message)

        # Remove thinking message
        message_view.remove_last_message()

        # Handle based on route type
        if result.route_decision.route_type == RouteType.DIRECT:
            # Direct response - no orchestration UI needed
            orch_panel.clear()
            status_bar.set_active_agent(None)

            if result.success:
                message_view.add_message(
                    role="assistant",
                    content=result.response,
                    agent_name="HEAD_CODEX"
                )
            else:
                message_view.add_message(
                    role="assistant",
                    content=f"[red]{result.error or 'Unknown error'}[/red]",
                    agent_name="HEAD_CODEX"
                )

        else:
            # Agent or workflow execution - show orchestration UI
            orch_panel.start_orchestration(
                result.route_decision.task or message[:50]
            )

            # Add engaged agents to orchestration panel
            for agent_result in result.agent_results:
                agent_info = AGENTS.get(agent_result.agent_id, {})
                orch_panel.add_agent(
                    agent_result.agent_id,
                    agent_info.get("name", agent_result.agent_name)
                )
                status_bar.set_active_agent(agent_result.agent_id)

            # Update gates
            for gate_id in result.gates_passed:
                gate_info = GATES.get(gate_id, {})
                orch_panel.set_gate_status(
                    gate_id,
                    gate_info.get("name", gate_id),
                    "PASSED"
                )

            for gate_id in result.gates_blocked:
                gate_info = GATES.get(gate_id, {})
                orch_panel.set_gate_status(
                    gate_id,
                    gate_info.get("name", gate_id),
                    "BLOCKED"
                )

            # Show the response
            if result.success:
                agent_name = "HEAD_CODEX"
                if result.agent_results:
                    agent_info = AGENTS.get(result.agent_results[0].agent_id, {})
                    agent_name = agent_info.get("name", result.agent_results[0].agent_name)

                message_view.add_message(
                    role="assistant",
                    content=result.response,
                    agent_name=agent_name
                )
            else:
                message_view.add_message(
                    role="assistant",
                    content=f"[red]{result.error or 'Agent execution failed'}[/red]",
                    agent_name="HEAD_CODEX"
                )

            # Update status
            status_bar.set_task_progress(
                len([r for r in result.agent_results if r.status == "complete"]),
                len(result.agent_results)
            )

        # Reset status
        status_bar.set_connection_status("connected")
        message_view.refresh()
