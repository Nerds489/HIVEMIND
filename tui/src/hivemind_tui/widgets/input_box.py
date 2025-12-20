"""Input Box Widget - Multi-line text input with history navigation."""

from textual.message import Message
from textual.widgets import TextArea


class InputBox(TextArea):
    """Multi-line text input widget with submission and history support."""

    BINDINGS = [
        ("ctrl+enter", "submit", "Send"),
        ("ctrl+up", "history_prev", "Previous"),
        ("ctrl+down", "history_next", "Next"),
    ]

    class Submitted(Message):
        """Message sent when text is submitted."""

        def __init__(self, message: str) -> None:
            super().__init__()
            self.message = message

    def __init__(self, *args, **kwargs) -> None:
        """Initialize input box."""
        super().__init__(*args, **kwargs)
        self.history: list[str] = []
        self.history_index: int = -1
        self.current_draft: str = ""

    def action_submit(self) -> None:
        """Submit the current text."""
        message = self.text.strip()

        if not message:
            return

        # Add to history
        if message and (not self.history or self.history[-1] != message):
            self.history.append(message)

        # Reset history navigation
        self.history_index = -1
        self.current_draft = ""

        # Post message and clear input
        self.post_message(self.Submitted(message))
        self.clear()

    def action_history_prev(self) -> None:
        """Navigate to previous history item."""
        if not self.history:
            return

        # Save current draft if starting navigation
        if self.history_index == -1:
            self.current_draft = self.text

        # Move to previous item
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.text = self.history[-(self.history_index + 1)]

    def action_history_next(self) -> None:
        """Navigate to next history item."""
        if not self.history or self.history_index == -1:
            return

        # Move to next item
        if self.history_index > 0:
            self.history_index -= 1
            self.text = self.history[-(self.history_index + 1)]
        else:
            # Return to draft
            self.history_index = -1
            self.text = self.current_draft
            self.current_draft = ""

    def clear(self) -> None:
        """Clear the input text."""
        self.text = ""
