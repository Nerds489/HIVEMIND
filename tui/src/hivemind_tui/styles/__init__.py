"""TUI styling and themes."""

from .themes import Theme, DARK_THEME, LIGHT_THEME, HACKER_THEME, get_theme
from .colors import (
    PRIMARY_COLORS,
    SECONDARY_COLORS,
    ACCENT_COLORS,
    STATUS_COLORS,
    TEAM_COLORS,
)

__all__ = [
    "Theme",
    "DARK_THEME",
    "LIGHT_THEME",
    "HACKER_THEME",
    "get_theme",
    "PRIMARY_COLORS",
    "SECONDARY_COLORS",
    "ACCENT_COLORS",
    "STATUS_COLORS",
    "TEAM_COLORS",
]
