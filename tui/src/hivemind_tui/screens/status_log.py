"""Status Log Screen - Popup status log view."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Static
from textual.binding import Binding

from ..widgets.status_log import StatusLog


class StatusLogScreen(ModalScreen):
    """Modal popup showing the status log."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=True),
        Binding("q", "dismiss", "Close", show=False),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="status-log-modal"):
            with Vertical():
                yield Static("STATUS LOG", id="status-log-title")
                yield StatusLog(id="status-log-list")
                yield Static("Press Esc to close", id="status-log-hint")

    def on_mount(self) -> None:
        log_widget = self.query_one("#status-log-list", StatusLog)
        log_widget.clear()
        app = self.app
        if hasattr(app, "get_status_log_entries"):
            for timestamp, message in app.get_status_log_entries():
                log_widget.write(f"[dim]{timestamp}[/dim] | {message}")

    def append_entry(self, timestamp: str, message: str) -> None:
        log_widget = self.query_one("#status-log-list", StatusLog)
        log_widget.write(f"[dim]{timestamp}[/dim] | {message}")
