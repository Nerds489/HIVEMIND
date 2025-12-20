"""Theme definitions for HIVEMIND TUI."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Theme:
    """Theme definition."""

    name: str

    # Background colors
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str

    # Foreground colors
    fg_primary: str
    fg_secondary: str
    fg_dim: str

    # Accent colors
    accent_primary: str
    accent_secondary: str

    # Status colors
    success: str
    error: str
    warning: str
    info: str

    # Team colors
    team_dev: str
    team_sec: str
    team_inf: str
    team_qa: str

    # UI element colors
    border_normal: str
    border_focus: str
    scrollbar_track: str
    scrollbar_thumb: str

    # Chat colors
    user_bubble: str
    assistant_bubble: str
    system_message: str
    code_block_bg: str
    code_block_border: str

    # Syntax highlighting
    syntax_keyword: str
    syntax_string: str
    syntax_number: str
    syntax_comment: str
    syntax_function: str


# Dark theme (default)
DARK_THEME = Theme(
    name="dark",

    # Backgrounds
    bg_primary="#1e1e2e",
    bg_secondary="#181825",
    bg_tertiary="#11111b",

    # Foreground
    fg_primary="#cdd6f4",
    fg_secondary="#a6adc8",
    fg_dim="#585b70",

    # Accents
    accent_primary="#89b4fa",
    accent_secondary="#b4befe",

    # Status
    success="#a6e3a1",
    error="#f38ba8",
    warning="#f9e2af",
    info="#89dceb",

    # Teams
    team_dev="#89b4fa",    # Blue
    team_sec="#f38ba8",    # Red
    team_inf="#a6e3a1",    # Green
    team_qa="#cba6f7",     # Purple

    # UI elements
    border_normal="#45475a",
    border_focus="#89b4fa",
    scrollbar_track="#313244",
    scrollbar_thumb="#585b70",

    # Chat
    user_bubble="#313244",
    assistant_bubble="#181825",
    system_message="#45475a",
    code_block_bg="#11111b",
    code_block_border="#45475a",

    # Syntax
    syntax_keyword="#f5c2e7",
    syntax_string="#a6e3a1",
    syntax_number="#fab387",
    syntax_comment="#6c7086",
    syntax_function="#89dceb",
)


# Light theme
LIGHT_THEME = Theme(
    name="light",

    # Backgrounds
    bg_primary="#eff1f5",
    bg_secondary="#e6e9ef",
    bg_tertiary="#dce0e8",

    # Foreground
    fg_primary="#4c4f69",
    fg_secondary="#5c5f77",
    fg_dim="#9ca0b0",

    # Accents
    accent_primary="#1e66f5",
    accent_secondary="#7287fd",

    # Status
    success="#40a02b",
    error="#d20f39",
    warning="#df8e1d",
    info="#209fb5",

    # Teams
    team_dev="#1e66f5",    # Blue
    team_sec="#d20f39",    # Red
    team_inf="#40a02b",    # Green
    team_qa="#8839ef",     # Purple

    # UI elements
    border_normal="#9ca0b0",
    border_focus="#1e66f5",
    scrollbar_track="#ccd0da",
    scrollbar_thumb="#9ca0b0",

    # Chat
    user_bubble="#dce0e8",
    assistant_bubble="#e6e9ef",
    system_message="#ccd0da",
    code_block_bg="#e6e9ef",
    code_block_border="#9ca0b0",

    # Syntax
    syntax_keyword="#8839ef",
    syntax_string="#40a02b",
    syntax_number="#fe640b",
    syntax_comment="#acb0be",
    syntax_function="#209fb5",
)


# Hacker theme (green on black)
HACKER_THEME = Theme(
    name="hacker",

    # Backgrounds
    bg_primary="#000000",
    bg_secondary="#0a0a0a",
    bg_tertiary="#050505",

    # Foreground
    fg_primary="#00ff00",
    fg_secondary="#00cc00",
    fg_dim="#006600",

    # Accents
    accent_primary="#00ff00",
    accent_secondary="#00ffff",

    # Status
    success="#00ff00",
    error="#ff0000",
    warning="#ffff00",
    info="#00ffff",

    # Teams
    team_dev="#00ccff",    # Cyan
    team_sec="#ff0000",    # Red
    team_inf="#00ff00",    # Green
    team_qa="#ff00ff",     # Magenta

    # UI elements
    border_normal="#006600",
    border_focus="#00ff00",
    scrollbar_track="#0a0a0a",
    scrollbar_thumb="#006600",

    # Chat
    user_bubble="#0a0a0a",
    assistant_bubble="#050505",
    system_message="#0f0f0f",
    code_block_bg="#050505",
    code_block_border="#006600",

    # Syntax
    syntax_keyword="#00ffff",
    syntax_string="#00ff00",
    syntax_number="#ffff00",
    syntax_comment="#006600",
    syntax_function="#00ccff",
)


# Theme registry
_THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "hacker": HACKER_THEME,
}


def get_theme(name: Optional[str] = None) -> Theme:
    """Get theme by name.

    Args:
        name: Theme name. Defaults to 'dark'.

    Returns:
        Theme instance.

    Raises:
        ValueError: If theme not found.
    """
    if name is None:
        name = "dark"

    theme = _THEMES.get(name.lower())
    if theme is None:
        available = ", ".join(_THEMES.keys())
        raise ValueError(f"Unknown theme '{name}'. Available: {available}")

    return theme
