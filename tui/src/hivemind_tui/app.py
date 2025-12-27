"""Main HIVEMIND TUI Application - v2.0 Minimal Output Mode."""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.driver import Driver
from textual.theme import Theme

from .engine.auth import AuthManager
from .screens.auth_screen import AuthScreen
from .screens.main import MainScreen
from .screens.chat import ChatScreen
from .screens.status_log import StatusLogScreen


CYBERPUNK_MATRIX_THEME = Theme(
    name="cyberpunk-matrix",
    primary="#ff0090",
    secondary="#00d4ff",
    accent="#00ffff",
    warning="#ffd200",
    error="#ff3b6b",
    success="#39ff14",
    foreground="#e6ffff",
    background="#05070b",
    surface="#0b1118",
    panel="#101a24",
    boost="#152231",
    variables={
        "footer-key-foreground": "#00ffff",
        "border": "#ff0090",
        "border-blurred": "#263040",
        "scrollbar": "#00ffff",
        "input-selection-background": "#00ffff 25%",
        "block-cursor-background": "#00ffff",
        "block-cursor-foreground": "#05070b",
        "button-color-foreground": "#05070b",
    },
)


class HivemindApp(App):
    """HIVEMIND Textual Application - v2.0."""

    CSS_PATH = "styles.css"
    TITLE = "HIVEMIND - HEAD_CODEX"
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("question_mark", "help", "Help", key_display="?"),
        Binding("ctrl+o", "status_log", "Status Log"),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("m", "show_main", "Main View"),
        Binding("ctrl+r", "refresh", "Refresh"),
    ]

    def __init__(
        self,
        driver_class: Optional[type[Driver]] = None,
        css_path: Optional[str] = None,
        watch_css: bool = False,
    ):
        """Initialize the HIVEMIND TUI application.

        Args:
            driver_class: Optional Textual driver class
            css_path: Optional path to CSS file
            watch_css: Whether to watch CSS file for changes
        """
        super().__init__(driver_class=driver_class, css_path=css_path, watch_css=watch_css)
        self.dark = True
        self.auth_manager = AuthManager()
        self._launch_dir = Path(os.environ.get("HIVEMIND_LAUNCH_DIR", os.getcwd()))
        self._status_log_entries: list[tuple[str, str]] = []
        self._status_log_limit = 300
        self.register_theme(CYBERPUNK_MATRIX_THEME)
        self.theme = os.environ.get("HIVEMIND_THEME", CYBERPUNK_MATRIX_THEME.name)

    def on_mount(self) -> None:
        """Handle app mount event."""
        # Start with auth screen
        self.push_screen(AuthScreen(self.auth_manager))

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_show_chat(self) -> None:
        """Show chat screen."""
        try:
            if not isinstance(self.screen, ChatScreen):
                self.push_screen(ChatScreen(self.auth_manager))
        except NoMatches:
            self.push_screen(ChatScreen(self.auth_manager))

    def action_show_main(self) -> None:
        """Show main screen."""
        # Pop screens until we get back to MainScreen
        while len(self.screen_stack) > 0:
            current = self.screen
            if isinstance(current, MainScreen):
                break
            try:
                self.pop_screen()
            except Exception:
                break

    def action_status_log(self) -> None:
        """Show the status log popup."""
        self.push_screen(StatusLogScreen())

    def action_refresh(self) -> None:
        """Refresh current screen."""
        self.refresh()

    def action_help(self) -> None:
        """Show help information."""
        help_text = """
HIVEMIND v2.0 Keyboard Shortcuts:

  Q     - Quit application
  C     - Open full chat screen
  Ctrl+O - Status log
  M     - Return to main view
  D     - Toggle dark/light mode
  Enter - Focus chat input
  Esc   - Go back
  ?     - Show this help

Chat:
  Ctrl+Enter - Send message
  Ctrl+L     - Clear messages

HIVEMIND runs in minimal-output mode.
Use /help for orchestration commands.
"""
        self.notify(help_text, title="HIVEMIND Help", timeout=10)

    @property
    def launch_dir(self) -> Path:
        """Get the directory from which HIVEMIND was launched."""
        return self._launch_dir

    def log_status(self, message: str) -> None:
        """Store a status message for the popup log."""
        cleaned = message.strip()
        if not cleaned:
            return
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._status_log_entries.append((timestamp, cleaned))
        if len(self._status_log_entries) > self._status_log_limit:
            self._status_log_entries = self._status_log_entries[-self._status_log_limit :]
        if isinstance(self.screen, StatusLogScreen):
            try:
                self.screen.append_entry(timestamp, cleaned)
            except Exception:
                pass

    def get_status_log_entries(self) -> list[tuple[str, str]]:
        """Return stored status log entries."""
        return list(self._status_log_entries)


def main() -> None:
    """Main entry point for the TUI application."""
    import argparse
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(description="HIVEMIND TUI - AI Assistant")
    parser.add_argument(
        "--watch-css",
        action="store_true",
        help="Watch CSS file for changes (development mode)",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Optional initial prompt",
    )

    args = parser.parse_args()

    app = HivemindApp(watch_css=args.watch_css)

    # Store initial prompt if provided
    if args.prompt:
        os.environ["HIVEMIND_INITIAL_PROMPT"] = args.prompt

    app.run()


if __name__ == "__main__":
    main()
