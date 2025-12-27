"""
HIVEMIND Dialogue View Widget.

Shows the Codex-Claude dialogue progress in real-time.
"""

from textual.containers import Vertical, ScrollableContainer
from textual.widgets import Static
from textual.reactive import reactive


class DialogueView(ScrollableContainer):
    """Widget to display Codex-Claude dialogue."""

    DEFAULT_CSS = """
    DialogueView {
        height: auto;
        max-height: 12;
        border: solid $primary;
        background: $surface;
        margin-bottom: 1;
        display: none;
    }

    DialogueView.visible {
        display: block;
    }

    #dialogue-title {
        text-style: bold;
        color: $primary;
        padding: 0 1;
    }

    #dialogue-content {
        padding: 0 1;
    }

    .dialogue-turn {
        margin: 0;
        padding: 0;
    }
    """

    visible = reactive(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._turns: list = []

    def compose(self):
        """Create child widgets."""
        yield Static("CODEX-CLAUDE DIALOGUE", id="dialogue-title")
        yield Vertical(id="dialogue-content")

    def add_turn(self, speaker: str, content: str) -> None:
        """Add a dialogue turn.

        Args:
            speaker: "codex" or "claude"
            content: Turn content
        """
        self._turns.append({"speaker": speaker, "content": content})
        self._refresh_content()

    def clear(self) -> None:
        """Clear all turns."""
        self._turns = []
        try:
            content = self.query_one("#dialogue-content", Vertical)
            content.remove_children()
        except Exception:
            pass

    def _refresh_content(self) -> None:
        """Refresh the displayed content."""
        try:
            content = self.query_one("#dialogue-content", Vertical)
            content.remove_children()

            for turn in self._turns:
                speaker = turn["speaker"].upper()
                color = "cyan" if speaker == "CODEX" else "magenta"
                # Show more content for better visibility
                text = turn["content"][:300] + "..." if len(turn["content"]) > 300 else turn["content"]
                # Clean up for display
                text = text.replace("\n", " ").strip()

                content.mount(Static(
                    f"[{color}][bold]{speaker}:[/bold][/{color}] {text}",
                    classes="dialogue-turn"
                ))

            # Scroll to bottom
            self.scroll_end()
        except Exception:
            pass

    def watch_visible(self, visible: bool) -> None:
        """React to visibility changes."""
        if visible:
            self.add_class("visible")
        else:
            self.remove_class("visible")
