"""Chat Screen - Interactive chat interface with intelligent routing via Coordinator."""

import asyncio
from pathlib import Path
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from ..widgets.message_view import MessageView
from ..widgets.input_box import InputBox
from ..widgets.orchestration_panel import OrchestrationPanel
from ..engine.coordinator import Coordinator, RouteType, AGENTS, GATES


class ChatScreen(Screen):
    """Chat screen with message history and intelligent input routing."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+l", "clear_messages", "Clear"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conversation_history: list[dict] = []
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

        with Container(id="chat-container"):
            with Horizontal(id="chat-layout"):
                # Main chat area
                with Vertical(id="chat-area"):
                    yield Static("HIVEMIND CHAT", classes="panel-title")
                    yield MessageView(id="chat-messages", show_timestamps=True)

                    # Input area
                    yield Static("YOUR MESSAGE (Ctrl+Enter to send)", classes="input-label")
                    yield InputBox(id="chat-input")

                # Side panel for orchestration (only visible when agents are engaged)
                with Vertical(id="chat-side-panel"):
                    yield Static("ORCHESTRATION", classes="panel-title")
                    yield OrchestrationPanel(id="chat-orchestration")

        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the input box
        self.query_one("#chat-input", InputBox).focus()

        # Load initial welcome message
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.add_message(
            role="assistant",
            content="""HIVEMIND Full Chat Mode active.

I'm HEAD_CODEX, your intelligent coordinator. I'll answer simple questions directly,
and route complex technical tasks to specialized agents.

**Try these examples:**
- "Who are you?" (direct response)
- "Design a REST API for a todo app" (routes to DEV-001 Architect)
- "Run a security audit on my code" (routes to SEC-002 Pentester)

What would you like help with?""",
            agent_name="HEAD_CODEX"
        )

    def _on_coordinator_status(self, status: str, message: str) -> None:
        """Handle coordinator status updates."""
        pass  # Could update a status indicator

    def _on_agent_update(self, agent_id: str, status: str, message: str) -> None:
        """Handle agent status updates."""
        try:
            orch_panel = self.query_one("#chat-orchestration", OrchestrationPanel)
            orch_panel.update_agent_status(agent_id, status, message)
        except Exception:
            pass

    def action_clear_messages(self) -> None:
        """Clear all messages from the chat."""
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.clear_messages()
        self._conversation_history.clear()

        orch_panel = self.query_one("#chat-orchestration", OrchestrationPanel)
        orch_panel.clear()

        self.notify("Messages cleared", title="Chat")

    async def on_input_box_submitted(self, event: InputBox.Submitted) -> None:
        """Handle message submission from input box."""
        message = event.message.strip()
        if not message or self._processing:
            return

        self._processing = True

        # Add user message to view
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.add_message(role="user", content=message)

        # Store in history
        self._conversation_history.append({"role": "user", "content": message})

        # Process through coordinator
        try:
            await self._process_with_coordinator(message)
        except Exception as e:
            message_view.add_message(
                role="assistant",
                content=f"[red]Error: {str(e)}[/red]",
                agent_name="HEAD_CODEX"
            )
        finally:
            self._processing = False

    async def _process_with_coordinator(self, message: str) -> None:
        """Process message through coordinator."""
        message_view = self.query_one("#chat-messages", MessageView)
        orch_panel = self.query_one("#chat-orchestration", OrchestrationPanel)

        # Show thinking indicator
        message_view.add_message(
            role="assistant",
            content="[dim italic]Analyzing...[/dim italic]",
            agent_name="HEAD_CODEX"
        )

        # Get response from coordinator
        result = await self._coordinator.process_input(message)

        # Remove thinking message
        message_view.remove_last_message()

        # Handle based on route type
        if result.route_decision.route_type == RouteType.DIRECT:
            # Direct response - no orchestration
            orch_panel.clear()

            if result.success:
                message_view.add_message(
                    role="assistant",
                    content=result.response,
                    agent_name="HEAD_CODEX"
                )
                self._conversation_history.append({
                    "role": "assistant",
                    "content": result.response
                })
            else:
                message_view.add_message(
                    role="assistant",
                    content=f"[red]{result.error or 'Unknown error'}[/red]",
                    agent_name="HEAD_CODEX"
                )

        else:
            # Agent execution - show orchestration
            orch_panel.start_orchestration(
                result.route_decision.task or message[:50]
            )

            # Add engaged agents
            for agent_result in result.agent_results:
                agent_info = AGENTS.get(agent_result.agent_id, {})
                orch_panel.add_agent(
                    agent_result.agent_id,
                    agent_info.get("name", agent_result.agent_name)
                )

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
                self._conversation_history.append({
                    "role": "assistant",
                    "content": result.response
                })
            else:
                message_view.add_message(
                    role="assistant",
                    content=f"[red]{result.error or 'Agent execution failed'}[/red]",
                    agent_name="HEAD_CODEX"
                )

        message_view.refresh()
