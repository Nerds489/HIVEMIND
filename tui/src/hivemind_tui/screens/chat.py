"""Chat Screen - Full chat interface for HIVEMIND v3.0."""

import asyncio
import os
from pathlib import Path
from typing import Optional

from textual import work
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.worker import Worker, WorkerState, get_current_worker

from ..widgets.message_view import MessageView
from ..widgets.status_bar import StatusBar
from ..widgets.input_box import InputBox
from ..engine.auth import AuthManager
from ..engine.codex_head import CodexHead, ResponseSource, CodexResponse
from ..engine.claude_agent import AGENTS


class ChatScreen(Screen):
    """Full-screen chat interface."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True, priority=True),
        Binding("ctrl+l", "clear_chat", "Clear", show=True),
        Binding("ctrl+c", "cancel_task", "Cancel", show=True),
    ]

    def __init__(self, auth_manager: AuthManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_manager = auth_manager
        self._processing = False
        self._current_worker: Optional[Worker] = None

        # Get launch directory for context
        self._launch_dir = Path(os.environ.get("HIVEMIND_LAUNCH_DIR", os.getcwd()))

        # Create CodexHead with thread-safe status callback
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
                    yield InputBox(id="chat-input", classes="chat-input")
                    yield StatusBar(id="chat-status")

        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        # Focus input
        input_box = self.query_one("#chat-input", InputBox)
        input_box.focus()

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
        """Handle status updates from Codex - called from worker thread."""
        # Use call_from_thread to safely post message to UI
        try:
            self.app.call_from_thread(self._update_status_display, message)
        except Exception:
            pass

    def _update_status_display(self, message: str) -> None:
        """Update status display on main thread."""
        try:
            status_bar = self.query_one("#chat-status", StatusBar)
            status_bar.set_connection_status("connecting")
            # Also update the thinking message if it exists
            message_view = self.query_one("#chat-messages", MessageView)
            if self._processing and message:
                # Update the last message to show current status
                message_view.update_last_message(f"[dim italic]{message}[/dim italic]")
        except Exception:
            pass

    def action_go_back(self) -> None:
        """Go back to main screen."""
        self._cancel_current_task()
        self.app.pop_screen()

    def action_cancel_task(self) -> None:
        """Cancel the current processing task."""
        if self._current_worker and self._processing:
            self._cancel_current_task()
            try:
                message_view = self.query_one("#chat-messages", MessageView)
                message_view.remove_last_message()
                message_view.add_message(
                    role="assistant",
                    content="[yellow]Task cancelled.[/yellow]",
                    agent_name="Codex"
                )
                self.query_one("#chat-status", StatusBar).set_connection_status("connected")
            except Exception:
                pass
            self._processing = False

    def _cancel_current_task(self) -> None:
        """Cancel the current worker if running."""
        if self._current_worker:
            self._current_worker.cancel()
            self._current_worker = None

    def action_clear_chat(self) -> None:
        """Clear chat messages."""
        self._cancel_current_task()
        try:
            message_view = self.query_one("#chat-messages", MessageView)
            message_view.clear()
            self._codex.clear_history()
        except Exception:
            pass

    def on_input_box_submitted(self, event: InputBox.Submitted) -> None:
        """Handle InputBox submission (Ctrl+Enter)."""
        # Don't await - call the worker method directly
        self._send_message(event.message)

    @work(exclusive=True)
    async def _send_message(self, message: str) -> None:
        """Send message using CodexHead via background worker."""
        if not message or self._processing:
            return

        self._processing = True
        worker = get_current_worker()
        self._current_worker = worker

        try:
            message_view = self.query_one("#chat-messages", MessageView)
            status_bar = self.query_one("#chat-status", StatusBar)

            # Show user message
            message_view.add_message(role="user", content=message)

            # Show thinking indicator
            message_view.add_message(
                role="assistant",
                content="[dim italic]Thinking... (Ctrl+C to cancel)[/dim italic]",
                agent_name="Codex"
            )
            status_bar.set_connection_status("connecting")

            # Check for cancellation before processing
            if worker.is_cancelled:
                return

            # Process the message
            response = await self._codex.process(message)

            # Check for cancellation after processing
            if worker.is_cancelled:
                return

            # Handle the response
            self._handle_response(response)

        except asyncio.CancelledError:
            # Worker was cancelled - handled by action_cancel_task
            pass
        except Exception as e:
            self._handle_error(str(e))
        finally:
            self._processing = False
            self._current_worker = None

    def _handle_response(self, response: CodexResponse) -> None:
        """Handle successful response from Codex."""
        try:
            message_view = self.query_one("#chat-messages", MessageView)
            status_bar = self.query_one("#chat-status", StatusBar)

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

            status_bar.set_connection_status("connected")
            message_view.refresh()
        except Exception:
            pass

    def _handle_error(self, error: str) -> None:
        """Handle processing error."""
        try:
            message_view = self.query_one("#chat-messages", MessageView)
            status_bar = self.query_one("#chat-status", StatusBar)

            message_view.remove_last_message()
            message_view.add_message(
                role="assistant",
                content=f"[red]Error: {error}[/red]",
                agent_name="Codex"
            )

            status_bar.set_connection_status("connected")
            message_view.refresh()
        except Exception:
            pass
