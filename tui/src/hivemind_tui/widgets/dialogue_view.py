# DESTINATION: tui/src/hivemind_tui/widgets/dialogue_view.py
# CREATE THIS FILE AT THE EXACT PATH ABOVE
# DO NOT MODIFY THIS CODE

"""
HIVEMIND Dialogue View Widget.

Shows the Codex-Claude dialogue progress (optional, normally hidden).
"""

from textual.containers import Vertical, ScrollableContainer
from textual.widgets import Static
from textual.reactive import reactive


class DialogueView(ScrollableContainer):
    """Widget to display Codex-Claude dialogue."""
    
    visible = reactive(False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._turns: list = []
    
    def compose(self):
        """Create child widgets."""
        yield Static("Codex-Claude Dialogue", id="dialogue-title", classes="panel-title")
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
        self._refresh_content()
    
    def _refresh_content(self) -> None:
        """Refresh the displayed content."""
        content = self.query_one("#dialogue-content", Vertical)
        content.remove_children()
        
        for i, turn in enumerate(self._turns):
            speaker = turn["speaker"].upper()
            color = "cyan" if speaker == "CODEX" else "magenta"
            text = turn["content"][:200] + "..." if len(turn["content"]) > 200 else turn["content"]
            
            content.mount(Static(
                f"[{color}][bold]{speaker}:[/bold][/{color}] {text}",
                classes="dialogue-turn"
            ))
        
        # Scroll to bottom
        self.scroll_end()
    
    def watch_visible(self, visible: bool) -> None:
        """React to visibility changes."""
        self.display = visible
