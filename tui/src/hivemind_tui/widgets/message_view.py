"""Message View Widget - Scrollable message history with rich formatting."""

from datetime import datetime
from typing import Optional

from rich.markdown import Markdown
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


class MessageView(Widget):
    """Widget to display scrollable message history."""

    message_count: reactive[int] = reactive(0)

    def __init__(
        self,
        *args,
        show_timestamps: bool = True,
        **kwargs
    ) -> None:
        """Initialize message view.

        Args:
            show_timestamps: Whether to show timestamps on messages
        """
        super().__init__(*args, **kwargs)
        self.show_timestamps = show_timestamps

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield VerticalScroll(id="message-scroll")

    def add_message(
        self,
        role: str,
        content: str,
        agent_name: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        use_markdown: bool = True,
    ) -> None:
        """Add a message to the view.

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            agent_name: Optional agent name for assistant messages
            timestamp: Optional timestamp (defaults to now)
            use_markdown: Whether to render content as markdown
        """
        if timestamp is None:
            timestamp = datetime.now()

        scroll = self.query_one("#message-scroll", VerticalScroll)

        message = MessageItem(
            role=role,
            content=content,
            agent_name=agent_name,
            timestamp=timestamp,
            show_timestamp=self.show_timestamps,
            use_markdown=use_markdown,
        )

        scroll.mount(message)
        self.message_count += 1

        # Auto-scroll to bottom
        self.call_after_refresh(self._scroll_to_bottom)

    def add_streaming_message(
        self,
        role: str,
        agent_name: Optional[str] = None,
    ) -> "StreamingMessageItem":
        """Add a streaming message that can be updated in real-time.

        Args:
            role: Message role (typically 'assistant')
            agent_name: Optional agent name

        Returns:
            StreamingMessageItem that can be updated
        """
        scroll = self.query_one("#message-scroll", VerticalScroll)

        message = StreamingMessageItem(
            role=role,
            agent_name=agent_name,
            timestamp=datetime.now(),
            show_timestamp=self.show_timestamps,
        )

        scroll.mount(message)
        self.message_count += 1

        return message

    def clear_messages(self) -> None:
        """Clear all messages from the view."""
        scroll = self.query_one("#message-scroll", VerticalScroll)
        scroll.remove_children()
        self.message_count = 0

    def _scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the message view."""
        scroll = self.query_one("#message-scroll", VerticalScroll)
        scroll.scroll_end(animate=False)


class MessageItem(Static):
    """Individual message item."""

    def __init__(
        self,
        role: str,
        content: str,
        agent_name: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        show_timestamp: bool = True,
        use_markdown: bool = True,
        **kwargs
    ) -> None:
        """Initialize message item.

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            agent_name: Optional agent name
            timestamp: Message timestamp
            show_timestamp: Whether to show timestamp
            use_markdown: Whether to render as markdown
        """
        super().__init__(**kwargs)
        self.role = role
        self.content = content
        self.agent_name = agent_name
        self.timestamp = timestamp or datetime.now()
        self.show_timestamp = show_timestamp
        self.use_markdown = use_markdown

        self.add_class(f"message-{role}")
        self.update(self._render_message())

    def _render_message(self) -> Text | Markdown:
        """Render the message content."""
        # Build header
        header_parts = []

        if self.role == "user":
            header_parts.append("[bold cyan]You[/bold cyan]")
        elif self.role == "assistant":
            agent = self.agent_name or "Assistant"
            header_parts.append(f"[bold green]{agent}[/bold green]")
        elif self.role == "system":
            header_parts.append("[bold yellow]System[/bold yellow]")

        if self.show_timestamp:
            time_str = self.timestamp.strftime("%H:%M:%S")
            header_parts.append(f"[dim]{time_str}[/dim]")

        header = " • ".join(header_parts)

        # Combine header and content
        full_content = f"{header}\n{self.content}\n"

        if self.use_markdown:
            return Markdown(full_content)
        else:
            return Text.from_markup(full_content)


class StreamingMessageItem(Static):
    """Message item that can be updated in real-time for streaming responses."""

    def __init__(
        self,
        role: str,
        agent_name: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        show_timestamp: bool = True,
        **kwargs
    ) -> None:
        """Initialize streaming message item.

        Args:
            role: Message role
            agent_name: Optional agent name
            timestamp: Message timestamp
            show_timestamp: Whether to show timestamp
        """
        super().__init__(**kwargs)
        self.role = role
        self.agent_name = agent_name
        self.timestamp = timestamp or datetime.now()
        self.show_timestamp = show_timestamp
        self.content_buffer = ""

        self.add_class(f"message-{role}")
        self.add_class("streaming")

    def append_content(self, chunk: str) -> None:
        """Append content chunk to the streaming message.

        Args:
            chunk: Content chunk to append
        """
        self.content_buffer += chunk
        self.update(self._render_message())

    def finalize(self) -> None:
        """Finalize the streaming message."""
        self.remove_class("streaming")
        self.update(self._render_message())

    def _render_message(self) -> Markdown:
        """Render the current message state."""
        # Build header
        header_parts = []

        if self.role == "assistant":
            agent = self.agent_name or "Assistant"
            header_parts.append(f"[bold green]{agent}[/bold green]")

        if self.show_timestamp:
            time_str = self.timestamp.strftime("%H:%M:%S")
            header_parts.append(f"[dim]{time_str}[/dim]")

        header = " • ".join(header_parts)

        # Add streaming indicator if still streaming
        content = self.content_buffer
        if "streaming" in self.classes:
            content += " ▌"

        full_content = f"{header}\n{content}\n"
        return Markdown(full_content)
