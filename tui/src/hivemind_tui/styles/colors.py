"""Color palette definitions for HIVEMIND TUI."""

from typing import Dict


# Primary colors (main UI elements)
PRIMARY_COLORS: Dict[str, str] = {
    "primary": "#89b4fa",
    "primary_light": "#b4befe",
    "primary_dark": "#5886c5",
    "primary_contrast": "#1e1e2e",
}


# Secondary colors (supporting elements)
SECONDARY_COLORS: Dict[str, str] = {
    "secondary": "#cba6f7",
    "secondary_light": "#f5c2e7",
    "secondary_dark": "#9965c4",
    "secondary_contrast": "#1e1e2e",
}


# Accent colors (highlights and emphasis)
ACCENT_COLORS: Dict[str, str] = {
    "accent": "#f9e2af",
    "accent_light": "#fdefc9",
    "accent_dark": "#c6b58c",
    "accent_contrast": "#1e1e2e",
    "glow": "#89dceb",
}


# Status colors (feedback and states)
STATUS_COLORS: Dict[str, str] = {
    "success": "#a6e3a1",
    "success_bg": "#213920",
    "error": "#f38ba8",
    "error_bg": "#3d2028",
    "warning": "#f9e2af",
    "warning_bg": "#3d3520",
    "info": "#89dceb",
    "info_bg": "#1f3540",
    "pending": "#fab387",
    "pending_bg": "#3d2d20",
    "idle": "#585b70",
    "idle_bg": "#1e1e2e",
}


# Team colors (agent teams)
TEAM_COLORS: Dict[str, str] = {
    # Development team
    "dev": "#89b4fa",
    "dev_bg": "#1f2d40",
    "dev_bright": "#b4befe",

    # Security team
    "sec": "#f38ba8",
    "sec_bg": "#3d2028",
    "sec_bright": "#f5c2e7",

    # Infrastructure team
    "inf": "#a6e3a1",
    "inf_bg": "#213920",
    "inf_bright": "#c3f0c0",

    # QA team
    "qa": "#cba6f7",
    "qa_bg": "#2d2040",
    "qa_bright": "#f5c2e7",

    # Research team
    "res": "#f9e2af",
    "res_bg": "#3d3520",
    "res_bright": "#fdefc9",

    # Operations team
    "ops": "#fab387",
    "ops_bg": "#3d2d20",
    "ops_bright": "#fcc9a6",
}


# UI element colors
UI_COLORS: Dict[str, str] = {
    # Backgrounds
    "bg_primary": "#1e1e2e",
    "bg_secondary": "#181825",
    "bg_tertiary": "#11111b",
    "bg_overlay": "#313244",

    # Foregrounds
    "fg_primary": "#cdd6f4",
    "fg_secondary": "#a6adc8",
    "fg_tertiary": "#585b70",
    "fg_dim": "#45475a",

    # Borders
    "border_normal": "#45475a",
    "border_focus": "#89b4fa",
    "border_error": "#f38ba8",
    "border_success": "#a6e3a1",

    # Scrollbar
    "scrollbar_track": "#313244",
    "scrollbar_thumb": "#585b70",
    "scrollbar_thumb_hover": "#6c7086",

    # Selection
    "selection_bg": "#313244",
    "selection_fg": "#cdd6f4",
}


# Chat message colors
CHAT_COLORS: Dict[str, str] = {
    "user_bubble": "#313244",
    "user_text": "#cdd6f4",
    "user_border": "#45475a",

    "assistant_bubble": "#181825",
    "assistant_text": "#cdd6f4",
    "assistant_border": "#585b70",

    "system_bubble": "#11111b",
    "system_text": "#a6adc8",
    "system_border": "#45475a",

    "code_block_bg": "#11111b",
    "code_block_border": "#45475a",
    "code_inline_bg": "#313244",
    "code_inline_fg": "#f5c2e7",
}


# Syntax highlighting colors
SYNTAX_COLORS: Dict[str, str] = {
    "keyword": "#f5c2e7",
    "string": "#a6e3a1",
    "number": "#fab387",
    "boolean": "#fab387",
    "comment": "#6c7086",
    "function": "#89dceb",
    "class": "#f9e2af",
    "variable": "#cdd6f4",
    "operator": "#89b4fa",
    "builtin": "#cba6f7",
    "regex": "#f38ba8",
}


# Markdown element colors
MARKDOWN_COLORS: Dict[str, str] = {
    "heading1": "#89b4fa",
    "heading2": "#cba6f7",
    "heading3": "#f9e2af",
    "heading4": "#a6e3a1",
    "heading5": "#fab387",
    "heading6": "#f38ba8",

    "bold": "#cdd6f4",
    "italic": "#a6adc8",
    "strikethrough": "#6c7086",
    "link": "#89dceb",
    "link_hover": "#b4defe",

    "quote_border": "#585b70",
    "quote_bg": "#181825",
    "quote_text": "#a6adc8",

    "list_bullet": "#89b4fa",
    "list_number": "#cba6f7",

    "hr": "#45475a",
}


def get_team_color(team: str) -> str:
    """Get color for a team.

    Args:
        team: Team identifier (e.g., 'dev', 'sec', 'inf', 'qa').

    Returns:
        Hex color string.
    """
    team_lower = team.lower()
    return TEAM_COLORS.get(team_lower, TEAM_COLORS.get("dev", "#89b4fa"))


def get_status_color(status: str) -> str:
    """Get color for a status.

    Args:
        status: Status identifier (e.g., 'success', 'error', 'warning').

    Returns:
        Hex color string.
    """
    status_lower = status.lower()
    return STATUS_COLORS.get(status_lower, STATUS_COLORS.get("info", "#89dceb"))
