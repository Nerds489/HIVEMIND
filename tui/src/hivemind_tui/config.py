"""TUI configuration management."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional
import json


@dataclass
class KeyBindings:
    """Keybinding configuration."""

    quit: str = "q"
    help: str = "?"
    focus_agents: str = "a"
    focus_chat: str = "c"
    focus_input: str = "i"
    send_message: str = "ctrl+s"
    clear_input: str = "ctrl+l"
    next_agent: str = "j"
    prev_agent: str = "k"
    toggle_sidebar: str = "ctrl+b"
    toggle_metrics: str = "m"
    switch_theme: str = "t"
    refresh: str = "r"
    scroll_up: str = "up"
    scroll_down: str = "down"
    page_up: str = "pageup"
    page_down: str = "pagedown"
    home: str = "home"
    end: str = "end"


@dataclass
class TUIConfig:
    """TUI configuration."""

    # Theme
    theme: str = "dark"

    # Backend connection
    backend_url: str = "http://localhost:8000"
    api_timeout: int = 30

    # UI settings
    show_timestamps: bool = True
    show_agent_status: bool = True
    show_metrics: bool = True
    sidebar_width: int = 30
    max_message_length: int = 10000

    # Auto-refresh
    auto_refresh: bool = True
    refresh_interval: int = 5

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None

    # Keybindings
    keybindings: KeyBindings = field(default_factory=KeyBindings)

    # Feature flags
    enable_syntax_highlighting: bool = True
    enable_markdown_rendering: bool = True
    enable_tool_output: bool = True
    enable_thinking_display: bool = True

    @classmethod
    def from_file(cls, path: Path) -> "TUIConfig":
        """Load configuration from JSON file.

        Args:
            path: Path to configuration file.

        Returns:
            TUIConfig instance.

        Raises:
            FileNotFoundError: If file doesn't exist.
            json.JSONDecodeError: If file is invalid JSON.
        """
        with open(path) as f:
            data = json.load(f)

        # Extract keybindings if present
        keybindings_data = data.pop("keybindings", {})
        keybindings = KeyBindings(**keybindings_data)

        return cls(keybindings=keybindings, **data)

    @classmethod
    def from_env(cls) -> "TUIConfig":
        """Load configuration from environment variables.

        Returns:
            TUIConfig instance.
        """
        config = cls()

        # Theme
        if theme := os.getenv("HIVEMIND_THEME"):
            config.theme = theme

        # Backend
        if backend_url := os.getenv("HIVEMIND_BACKEND_URL"):
            config.backend_url = backend_url

        if api_timeout := os.getenv("HIVEMIND_API_TIMEOUT"):
            config.api_timeout = int(api_timeout)

        # UI settings
        if show_timestamps := os.getenv("HIVEMIND_SHOW_TIMESTAMPS"):
            config.show_timestamps = show_timestamps.lower() == "true"

        if show_agent_status := os.getenv("HIVEMIND_SHOW_AGENT_STATUS"):
            config.show_agent_status = show_agent_status.lower() == "true"

        if show_metrics := os.getenv("HIVEMIND_SHOW_METRICS"):
            config.show_metrics = show_metrics.lower() == "true"

        if sidebar_width := os.getenv("HIVEMIND_SIDEBAR_WIDTH"):
            config.sidebar_width = int(sidebar_width)

        # Auto-refresh
        if auto_refresh := os.getenv("HIVEMIND_AUTO_REFRESH"):
            config.auto_refresh = auto_refresh.lower() == "true"

        if refresh_interval := os.getenv("HIVEMIND_REFRESH_INTERVAL"):
            config.refresh_interval = int(refresh_interval)

        # Logging
        if log_level := os.getenv("HIVEMIND_LOG_LEVEL"):
            config.log_level = log_level.upper()

        if log_file := os.getenv("HIVEMIND_LOG_FILE"):
            config.log_file = log_file

        # Feature flags
        if syntax_highlighting := os.getenv("HIVEMIND_SYNTAX_HIGHLIGHTING"):
            config.enable_syntax_highlighting = syntax_highlighting.lower() == "true"

        if markdown_rendering := os.getenv("HIVEMIND_MARKDOWN_RENDERING"):
            config.enable_markdown_rendering = markdown_rendering.lower() == "true"

        if tool_output := os.getenv("HIVEMIND_TOOL_OUTPUT"):
            config.enable_tool_output = tool_output.lower() == "true"

        if thinking_display := os.getenv("HIVEMIND_THINKING_DISPLAY"):
            config.enable_thinking_display = thinking_display.lower() == "true"

        return config

    def to_file(self, path: Path) -> None:
        """Save configuration to JSON file.

        Args:
            path: Path to save configuration.
        """
        data = {
            "theme": self.theme,
            "backend_url": self.backend_url,
            "api_timeout": self.api_timeout,
            "show_timestamps": self.show_timestamps,
            "show_agent_status": self.show_agent_status,
            "show_metrics": self.show_metrics,
            "sidebar_width": self.sidebar_width,
            "max_message_length": self.max_message_length,
            "auto_refresh": self.auto_refresh,
            "refresh_interval": self.refresh_interval,
            "log_level": self.log_level,
            "log_file": self.log_file,
            "keybindings": {
                "quit": self.keybindings.quit,
                "help": self.keybindings.help,
                "focus_agents": self.keybindings.focus_agents,
                "focus_chat": self.keybindings.focus_chat,
                "focus_input": self.keybindings.focus_input,
                "send_message": self.keybindings.send_message,
                "clear_input": self.keybindings.clear_input,
                "next_agent": self.keybindings.next_agent,
                "prev_agent": self.keybindings.prev_agent,
                "toggle_sidebar": self.keybindings.toggle_sidebar,
                "toggle_metrics": self.keybindings.toggle_metrics,
                "switch_theme": self.keybindings.switch_theme,
                "refresh": self.keybindings.refresh,
                "scroll_up": self.keybindings.scroll_up,
                "scroll_down": self.keybindings.scroll_down,
                "page_up": self.keybindings.page_up,
                "page_down": self.keybindings.page_down,
                "home": self.keybindings.home,
                "end": self.keybindings.end,
            },
            "enable_syntax_highlighting": self.enable_syntax_highlighting,
            "enable_markdown_rendering": self.enable_markdown_rendering,
            "enable_tool_output": self.enable_tool_output,
            "enable_thinking_display": self.enable_thinking_display,
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)


def get_config_path() -> Path:
    """Get default configuration file path.

    Returns:
        Path to configuration file.
    """
    # Check XDG_CONFIG_HOME first
    if xdg_config := os.getenv("XDG_CONFIG_HOME"):
        return Path(xdg_config) / "hivemind" / "tui.json"

    # Fall back to ~/.config
    return Path.home() / ".config" / "hivemind" / "tui.json"


def load_config(config_path: Optional[Path] = None) -> TUIConfig:
    """Load configuration.

    Loads in order of precedence:
    1. Specified config file
    2. Default config file
    3. Environment variables
    4. Defaults

    Args:
        config_path: Optional path to configuration file.

    Returns:
        TUIConfig instance.
    """
    # Start with environment variables
    config = TUIConfig.from_env()

    # Try to load from file
    if config_path and config_path.exists():
        try:
            file_config = TUIConfig.from_file(config_path)
            # Merge file config with env config (env takes precedence)
            return file_config
        except Exception as e:
            # Log error but continue with env/default config
            print(f"Warning: Failed to load config from {config_path}: {e}")
    else:
        # Try default config path
        default_path = get_config_path()
        if default_path.exists():
            try:
                return TUIConfig.from_file(default_path)
            except Exception as e:
                print(f"Warning: Failed to load config from {default_path}: {e}")

    return config


def save_config(config: TUIConfig, config_path: Optional[Path] = None) -> None:
    """Save configuration.

    Args:
        config: Configuration to save.
        config_path: Optional path to save to. Defaults to default config path.
    """
    if config_path is None:
        config_path = get_config_path()

    config.to_file(config_path)
