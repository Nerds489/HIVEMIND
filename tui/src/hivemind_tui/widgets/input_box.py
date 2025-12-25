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
        self._input_history: list[str] = []
        self._history_index: int = -1
        self._current_draft: str = ""

    def action_submit(self) -> None:
        """Submit the current text."""
        message = self.text.strip()

        if not message:
            return

        # Add to history
        if message and (not self._input_history or self._input_history[-1] != message):
            self._input_history.append(message)

        # Reset history navigation
        self._history_index = -1
        self._current_draft = ""

        # Post message and clear input
        self.post_message(self.Submitted(message))
        self.clear()

    def action_history_prev(self) -> None:
        """Navigate to previous history item."""
        if not self._input_history:
            return

        # Save current draft if starting navigation
        if self._history_index == -1:
            self._current_draft = self.text

        # Move to previous item
        if self._history_index < len(self._input_history) - 1:
            self._history_index += 1
            self.text = self._input_history[-(self._history_index + 1)]

    def action_history_next(self) -> None:
        """Navigate to next history item."""
        if not self._input_history or self._history_index == -1:
            return

        # Move to next item
        if self._history_index > 0:
            self._history_index -= 1
            self.text = self._input_history[-(self._history_index + 1)]
        else:
            # Return to draft
            self._history_index = -1
            self.text = self._current_draft
            self._current_draft = ""

    def clear(self) -> None:
        """Clear the input text."""
        self.text = ""
