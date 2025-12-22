"""Chat Screen - Interactive chat interface with Claude Code integration."""

import asyncio
import os
import shutil
from pathlib import Path
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.worker import Worker, get_current_worker

from ..widgets.message_view import MessageView
from ..widgets.input_box import InputBox


class ChatScreen(Screen):
    """Chat screen with message history and input."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+l", "clear_messages", "Clear"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conversation_history: list[dict] = []
        self._processing = False
        self._hivemind_dir = Path(__file__).parent.parent.parent.parent.parent.parent

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)

        with Container(id="chat-container"):
            with Vertical(id="chat-area"):
                # Message history
                yield Static("HIVEMIND CHAT (Claude Code)", classes="panel-title")
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
            content="HIVEMIND active. I'm connected to Claude Code. How can I help?",
            agent_name="HIVEMIND"
        )

    def action_clear_messages(self) -> None:
        """Clear all messages from the chat."""
        message_view = self.query_one("#chat-messages", MessageView)
        message_view.clear_messages()
        self._conversation_history.clear()
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

        # Send to Claude Code
        self.run_worker(self._call_claude(message), exclusive=True)

    async def _call_claude(self, message: str) -> None:
        """Call Claude Code CLI and stream the response."""
        message_view = self.query_one("#chat-messages", MessageView)

        # Find claude executable
        claude_path = shutil.which("claude")
        if not claude_path:
            # Try common locations
            for path in [
                Path.home() / ".local/bin/claude",
                Path("/usr/local/bin/claude"),
            ]:
                if path.exists():
                    claude_path = str(path)
                    break

        if not claude_path:
            message_view.add_message(
                role="assistant",
                content="[red]Error: Claude Code CLI not found. Install it with: npm install -g @anthropic-ai/claude-code[/red]",
                agent_name="HIVEMIND"
            )
            self._processing = False
            return

        # Prepare the command - use print mode for streaming
        cmd = [
            claude_path,
            "--dangerously-skip-permissions",
            "--print",
            message
        ]

        try:
            # Show thinking indicator
            message_view.add_message(
                role="assistant",
                content="[dim italic]Processing...[/dim italic]",
                agent_name="HIVEMIND"
            )

            # Run claude with streaming output
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self._hivemind_dir),
            )

            stdout, stderr = await process.communicate()

            # Remove the "Processing..." message
            message_view.remove_last_message()

            if process.returncode == 0:
                response = stdout.decode("utf-8", errors="replace").strip()
                if response:
                    message_view.add_message(
                        role="assistant",
                        content=response,
                        agent_name="HIVEMIND"
                    )
                    self._conversation_history.append({"role": "assistant", "content": response})
                else:
                    message_view.add_message(
                        role="assistant",
                        content="[dim]No response received.[/dim]",
                        agent_name="HIVEMIND"
                    )
            else:
                error = stderr.decode("utf-8", errors="replace").strip()
                message_view.add_message(
                    role="assistant",
                    content=f"[red]Error: {error or 'Unknown error'}[/red]",
                    agent_name="HIVEMIND"
                )

        except Exception as e:
            message_view.add_message(
                role="assistant",
                content=f"[red]Error calling Claude: {str(e)}[/red]",
                agent_name="HIVEMIND"
            )
        finally:
            self._processing = False
            message_view.refresh()
