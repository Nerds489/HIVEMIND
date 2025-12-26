"""Chat Screen - Full chat interface for HIVEMIND v3.0."""

import asyncio
import os
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Input, TextArea
from textual.binding import Binding

from ..widgets.message_view import MessageView
from ..widgets.status_bar import StatusBar
from ..engine.auth import AuthManager
from ..engine.codex_head import CodexHead, ResponseSource
from ..engine.claude_agent import AGENTS


class ChatScreen(Screen):
    """Full-screen chat interface."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("ctrl+l", "clear_chat", "Clear", show=True),
        Binding("ctrl+enter", "send_message", "Send", show=True),
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
        """Create child widgets."""
        yield Header(show_clock=True)

        with Container(id="chat-container"):
            with Vertical(id="chat-main"):
                yield Static("HIVEMIND Chat", id="chat-title", classes="panel-title")
                yield MessageView(id="chat-messages")

                with Container(id="chat-input-area"):
                    yield TextArea(id="chat-input", classes="chat-input")
                    yield StatusBar(id="chat-status")

        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        # Focus input
        self.query_one("#chat-input", TextArea).focus()

        # Add welcome message
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.add_message(
            role="assistant",
            content="Full chat mode. Type your message and press Ctrl+Enter to send.",
            agent_name="Codex"
        )

        # Update status
        status_bar = self.query_one("#chat-status", StatusBar)
        status_bar.set_connection_status("connected")

    def _on_codex_status(self, message: str) -> None:
        """Handle status updates from Codex."""
        try:
            status_bar = self.query_one("#chat-status", StatusBar)
            status_bar.set_connection_status("connecting")
        except Exception:
            pass

    def action_go_back(self) -> None:
        """Go back to main screen."""
        self.app.pop_screen()

    def action_clear_chat(self) -> None:
        """Clear chat messages."""
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.clear()
        self._codex.clear_history()

    async def action_send_message(self) -> None:
        """Send the current message."""
        await self._send_message()

    async def on_text_area_submitted(self, event) -> None:
        """Handle TextArea submission."""
        await self._send_message()

    async def _send_message(self) -> None:
        """Send message using CodexHead."""
        chat_input = self.query_one("#chat-input", TextArea)
        message = chat_input.text.strip()

        if not message or self._processing:
            return

        self._processing = True
        message_view = self.query_one("#chat-messages", MessageView)
        status_bar = self.query_one("#chat-status", StatusBar)

        # Show user message
        message_view.add_message(role="user", content=message)
        chat_input.clear()

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

            # Show response
            if response.success:
                # Add agent info if agents were used
                agent_info = ""
                if response.agents_used:
                    agent_names = [AGENTS.get(a, {}).get("name", a) for a in response.agents_used]
                    agent_info = f"\n\n[dim](Assisted by: {', '.join(agent_names)})[/dim]"

                message_view.add_message(
                    role="assistant",
                    content=response.content + agent_info,
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
