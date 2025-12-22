"""Main HIVEMIND TUI Application."""

import asyncio
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.driver import Driver

from .screens.main import MainScreen
from .screens.chat import ChatScreen


class HivemindApp(App):
    """HIVEMIND Textual Application."""

    CSS_PATH = "styles.css"
    TITLE = "HIVEMIND - Multi-Agent Command Center"
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("question_mark", "help", "Help", key_display="?"),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("c", "show_chat", "Chat View"),
        Binding("m", "show_main", "Main View"),
        Binding("ctrl+r", "refresh", "Refresh"),
    ]

    def __init__(
        self,
        driver_class: Optional[type[Driver]] = None,
        css_path: Optional[str] = None,
        watch_css: bool = False,
        api_base_url: str = "http://localhost:8000",
        ws_base_url: str = "ws://localhost:8000",
    ):
        """Initialize the HIVEMIND TUI application.

        Args:
            driver_class: Optional Textual driver class
            css_path: Optional path to CSS file
            watch_css: Whether to watch CSS file for changes
            api_base_url: Base URL for HTTP API
            ws_base_url: Base URL for WebSocket connections
        """
        super().__init__(driver_class=driver_class, css_path=css_path, watch_css=watch_css)
        self.api_base_url = api_base_url
        self.ws_base_url = ws_base_url
        self.dark = True

    def on_mount(self) -> None:
        """Handle app mount event."""
        self.push_screen(MainScreen())

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_show_chat(self) -> None:
        """Show chat screen."""
        try:
            # Check if chat screen already exists
            self.screen
            if not isinstance(self.screen, ChatScreen):
                self.push_screen(ChatScreen())
        except NoMatches:
            self.push_screen(ChatScreen())

    def action_show_main(self) -> None:
        """Show main screen."""
        if not isinstance(self.screen, MainScreen):
            # Pop all screens and show main
            while len(self.screen_stack) > 1:
                self.pop_screen()

    def action_refresh(self) -> None:
        """Refresh current screen."""
        self.refresh()

    def action_help(self) -> None:
        """Show help information."""
        help_text = """
HIVEMIND Keyboard Shortcuts:

  Q     - Quit application
  C     - Open full chat screen
  M     - Return to main view
  D     - Toggle dark/light mode
  Enter - Focus chat input
  Esc   - Go back
  ?     - Show this help

Chat Shortcuts:
  Ctrl+Enter - Send message
  Ctrl+L     - Clear messages
  Ctrl+Up    - Previous message
  Ctrl+Down  - Next message
"""
        self.notify(help_text, title="HIVEMIND Help", timeout=10)


def main() -> None:
    """Main entry point for the TUI application."""
    import argparse
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(description="HIVEMIND TUI - Multi-Agent Command Center")
    parser.add_argument(
        "--api-url",
        default=os.getenv("HIVEMIND_API_URL", "http://localhost:8000"),
        help="Base URL for HIVEMIND API",
    )
    parser.add_argument(
        "--ws-url",
        default=os.getenv("HIVEMIND_WS_URL", "ws://localhost:8000"),
        help="Base URL for WebSocket connections",
    )
    parser.add_argument(
        "--watch-css",
        action="store_true",
        help="Watch CSS file for changes (development mode)",
    )

    args = parser.parse_args()

    app = HivemindApp(
        api_base_url=args.api_url,
        ws_base_url=args.ws_url,
        watch_css=args.watch_css,
    )

    app.run()


if __name__ == "__main__":
    main()
