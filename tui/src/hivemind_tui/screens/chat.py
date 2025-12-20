"""Chat Screen - Interactive chat interface."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from ..widgets.message_view import MessageView
from ..widgets.input_box import InputBox


class ChatScreen(Screen):
    """Chat screen with message history and input."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+l", "clear_messages", "Clear"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)

        with Container(id="chat-container"):
            with Vertical(id="chat-area"):
                # Message history
                yield Static("CONVERSATION", classes="panel-title")
                yield MessageView(id="chat-messages", show_timestamps=True)

                # Input area
                yield Static("YOUR MESSAGE (Ctrl+Enter to send)", classes="input-label")
                yield InputBox(id="chat-input")

        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the input box
        self.query_one("#chat-input", InputBox).focus()

        # Load initial welcome message
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.add_message(
            role="assistant",
            content="Hello! I'm HIVEMIND. How can I help you today?",
            agent_name="System"
        )

    def action_clear_messages(self) -> None:
        """Clear all messages from the chat."""
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.clear_messages()
        self.notify("Messages cleared", title="Chat")

    async def on_input_box_submitted(self, event: InputBox.Submitted) -> None:
        """Handle message submission from input box."""
        message = event.message.strip()
        if not message:
            return

        # Add user message to view
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.add_message(role="user", content=message)

        # TODO: Send message to API and handle streaming response
        # For now, just echo back
        await self._send_message(message)

    async def _send_message(self, message: str) -> None:
        """Send message to HIVEMIND API and handle response.

        Args:
            message: User message to send
        """
        message_view = self.query_one("#chat-messages", MessageView)

        # TODO: Implement actual API call with streaming
        # For now, show a placeholder response
        import asyncio
        await asyncio.sleep(0.5)

        message_view.add_message(
            role="assistant",
            content=f"You said: {message}\n\n[dim]API integration pending...[/dim]",
            agent_name="HIVEMIND"
        )
