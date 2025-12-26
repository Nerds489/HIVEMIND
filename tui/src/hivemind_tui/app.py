"""Main HIVEMIND TUI Application - v3.0 TUI-Only Mode."""

import asyncio
import os
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.driver import Driver

from .engine.auth import AuthManager
from .screens.auth_screen import AuthScreen
from .screens.main import MainScreen
from .screens.chat import ChatScreen


class HivemindApp(App):
    """HIVEMIND Textual Application - v3.0."""

    CSS_PATH = "styles.css"
    TITLE = "HIVEMIND - AI Assistant"
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("question_mark", "help", "Help", key_display="?"),
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

    def action_refresh(self) -> None:
        """Refresh current screen."""
        self.refresh()

    def action_help(self) -> None:
        """Show help information."""
        help_text = """
HIVEMIND v3.0 Keyboard Shortcuts:

  Q     - Quit application
  C     - Open full chat screen
  M     - Return to main view
  D     - Toggle dark/light mode
  Enter - Focus chat input
  Esc   - Go back
  ?     - Show this help

Chat:
  Ctrl+Enter - Send message
  Ctrl+L     - Clear messages

HIVEMIND is your AI assistant.
For simple questions, I answer directly.
For complex work, I coordinate with Claude and specialized agents.
"""
        self.notify(help_text, title="HIVEMIND Help", timeout=10)

    @property
    def launch_dir(self) -> Path:
        """Get the directory from which HIVEMIND was launched."""
        return self._launch_dir


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
