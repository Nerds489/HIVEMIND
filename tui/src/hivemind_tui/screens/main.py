"""Main Screen - Three-panel layout for HIVEMIND with quick chat."""

import asyncio
import shutil
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from textual.binding import Binding

from ..widgets.agent_list import AgentListWidget
from ..widgets.message_view import MessageView
from ..widgets.status_bar import StatusBar


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

                # Center panel: Quick response view
                with Vertical(id="chat-panel", classes="panel"):
                    yield Static("RESPONSE", classes="panel-title")
                    yield MessageView(id="message-view")

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
Enter to send.[/dim]"""

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the quick chat input for immediate use
        self.query_one("#quick-chat-input", Input).focus()

        # Add welcome message
        message_view = self.query_one("#message-view", MessageView)
        message_view.add_message(
            role="assistant",
            content="HIVEMIND ready. Type above to chat, or press [C] for full chat mode.",
            agent_name="HIVEMIND"
        )

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
        """Send message from quick chat input."""
        chat_input = self.query_one("#quick-chat-input", Input)
        message = chat_input.value.strip()

        if not message or self._processing:
            return

        self._processing = True
        message_view = self.query_one("#message-view", MessageView)

        # Show user message
        message_view.add_message(role="user", content=message)
        chat_input.value = ""

        # Call Claude
        await self._call_claude(message, message_view)

    async def _call_claude(self, message: str, message_view: MessageView) -> None:
        """Call Claude Code CLI."""
        claude_path = shutil.which("claude")
        if not claude_path:
            for path in [Path.home() / ".local/bin/claude", Path("/usr/local/bin/claude")]:
                if path.exists():
                    claude_path = str(path)
                    break

        if not claude_path:
            message_view.add_message(
                role="assistant",
                content="[red]Claude Code CLI not found![/red]",
                agent_name="HIVEMIND"
            )
            self._processing = False
            return

        cmd = [claude_path, "--dangerously-skip-permissions", "--print", message]

        try:
            message_view.add_message(
                role="assistant",
                content="[dim italic]Thinking...[/dim italic]",
                agent_name="HIVEMIND"
            )

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self._hivemind_dir),
            )

            stdout, stderr = await process.communicate()

            # Remove thinking message
            message_view.remove_last_message()

            if process.returncode == 0:
                response = stdout.decode("utf-8", errors="replace").strip()
                message_view.add_message(
                    role="assistant",
                    content=response or "[dim]No response[/dim]",
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
                content=f"[red]Error: {str(e)}[/red]",
                agent_name="HIVEMIND"
            )
        finally:
            self._processing = False
            message_view.refresh()
