"""Input Box Widget - Multi-line text input with history navigation."""

from textual.binding import Binding
from textual.events import Key
from textual.message import Message
from textual.widgets import TextArea


class InputBox(TextArea):
    """Multi-line text input widget with submission and history support.

    This widget extends TextArea to provide:
    - Ctrl+Enter to submit the message
    - Ctrl+Up/Down for history navigation
    - Full text selection and editing capabilities
    """

    # Set can_focus to True to ensure proper focus handling
    can_focus = True

    # Define bindings for history navigation (Ctrl+Enter handled in _on_key)
    BINDINGS = [
        Binding("ctrl+up", "history_prev", "Previous", show=False),
        Binding("ctrl+down", "history_next", "Next", show=False),
    ]

    class Submitted(Message):
        """Message sent when text is submitted via Ctrl+Enter.

        Attributes:
            message: The submitted text content.
        """
        # Ensure message bubbles up to parent widgets/screens
        bubble = True

        def __init__(self, message: str) -> None:
            super().__init__()
            self.message = message

    def __init__(
        self,
        text: str = "",
        *,
        language: str | None = None,
        theme: str = "css",
        soft_wrap: bool = True,
        tab_behavior: str = "indent",
        show_line_numbers: bool = False,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialize input box.

        Args:
            text: Initial text content.
            language: Language for syntax highlighting (None for plain text).
            theme: Color theme for the text area.
            soft_wrap: Whether to wrap long lines.
            tab_behavior: How tabs are handled ("indent" or "focus").
            show_line_numbers: Whether to show line numbers.
            id: Widget ID.
            classes: CSS classes.
            disabled: Whether the widget is disabled.
        """
        super().__init__(
            text,
            language=language,
            theme=theme,
            soft_wrap=soft_wrap,
            tab_behavior=tab_behavior,
            show_line_numbers=show_line_numbers,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._input_history: list[str] = []
        self._history_index: int = -1
        self._current_draft: str = ""

    def _on_key(self, event: Key) -> None:
        """Handle key presses, intercepting Ctrl+Enter for submission.

        This method intercepts key events before they reach TextArea's
        default handling, allowing us to properly capture Ctrl+Enter
        for message submission.
        """
        # Handle Ctrl+Enter for submission
        if event.key == "ctrl+enter":
            self._submit()
            event.prevent_default()
            event.stop()
            return

        # Let TextArea handle all other keys normally
        # This preserves text selection, editing, cursor movement, etc.

    def _submit(self) -> None:
        """Submit the current text content."""
        message = self.text.strip()

        if not message:
            return

        # Add to history (avoid duplicates at the end)
        if message and (not self._input_history or self._input_history[-1] != message):
            self._input_history.append(message)

        # Reset history navigation state
        self._history_index = -1
        self._current_draft = ""

        # Post the Submitted message (bubbles up to parent)
        self.post_message(self.Submitted(message))

        # Clear the input
        self.clear()

    def action_history_prev(self) -> None:
        """Navigate to the previous history item (Ctrl+Up)."""
        if not self._input_history:
            return

        # Save current text as draft when starting navigation
        if self._history_index == -1:
            self._current_draft = self.text

        # Move to previous (older) item in history
        if self._history_index < len(self._input_history) - 1:
            self._history_index += 1
            self.text = self._input_history[-(self._history_index + 1)]
            # Move cursor to end of text
            self._move_cursor_to_end()

    def action_history_next(self) -> None:
        """Navigate to the next history item (Ctrl+Down)."""
        if not self._input_history or self._history_index == -1:
            return

        # Move to next (newer) item in history
        if self._history_index > 0:
            self._history_index -= 1
            self.text = self._input_history[-(self._history_index + 1)]
            # Move cursor to end of text
            self._move_cursor_to_end()
        else:
            # Return to the draft text
            self._history_index = -1
            self.text = self._current_draft
            self._current_draft = ""
            # Move cursor to end of text
            self._move_cursor_to_end()

    def _move_cursor_to_end(self) -> None:
        """Move the cursor to the end of the text."""
        if self.text:
            lines = self.text.split("\n")
            last_line_idx = len(lines) - 1
            last_col = len(lines[-1])
            self.cursor_location = (last_line_idx, last_col)

    def clear(self) -> None:
        """Clear all text from the input box."""
        self.text = ""
        # Reset cursor to start
        self.cursor_location = (0, 0)
