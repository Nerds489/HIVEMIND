"""Status Log Widget - Rolling status updates with timestamps."""

from datetime import datetime

from rich.text import Text
from textual.widgets import RichLog


class StatusLog(RichLog):
    """Rolling status log for orchestration progress."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            max_lines=200,
            auto_scroll=True,
            wrap=True,
            markup=True,
            **kwargs,
        )
        self._last_message: str | None = None

    def log(self, message: str) -> None:
        """Append a status message with timestamp."""
        cleaned = message.strip()
        if not cleaned or cleaned == self._last_message:
            return

        self._last_message = cleaned
        timestamp = datetime.now().strftime("%H:%M:%S")

        line = Text()
        line.append(timestamp, style="dim")
        line.append(" | ", style="dim")
        line.append(cleaned)
        self.write(line)
