#!/bin/bash
#
# HIVEMIND Installation

set -euo pipefail

HIVEMIND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing HIVEMIND..."

LAUNCH_MODE="${LAUNCH_MODE:-auto}"  # auto|yes|no
PATH_MODE="${PATH_MODE:-auto}"      # auto|yes|no

while [[ $# -gt 0 ]]; do
  case "$1" in
    --launch) LAUNCH_MODE="yes"; shift ;;
    --no-launch) LAUNCH_MODE="no"; shift ;;
    --path) PATH_MODE="yes"; shift ;;
    --no-path) PATH_MODE="no"; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

check_dep() {
    if ! command -v "$1" &> /dev/null; then
        echo "Warning: $1 not found. Install it for $2 support."
        return 1
    fi
    return 0
}

echo "Checking engines..."
check_dep "codex" "Codex CLI" || true
check_dep "claude" "Claude Code CLI" || true

ensure_user_bin() {
  local user_bin="$HOME/.local/bin"
  mkdir -p "$user_bin"
  ln -sf "$HIVEMIND_ROOT/hivemind" "$user_bin/hivemind"
  ln -sf "$HIVEMIND_ROOT/bin/hm" "$user_bin/hm"
  echo "Installed (user): $user_bin/hivemind"
  echo "Installed (user): $user_bin/hm"
}

ensure_path() {
  if [[ "$PATH_MODE" == "no" ]]; then
    return 0
  fi

  local user_bin="$HOME/.local/bin"
  if [[ ":$PATH:" == *":$user_bin:"* ]]; then
    return 0
  fi

  # Only auto-modify bash startup files when PATH_MODE is yes or auto.
  # (auto is still safe: idempotent marker block)
  local marker_begin="# >>> HIVEMIND PATH >>>"
  local marker_end="# <<< HIVEMIND PATH <<<"
  local block="${marker_begin}
if [[ -d \"\\$HOME/.local/bin\" ]] && [[ \":\\$PATH:\" != *\":\\$HOME/.local/bin:\"* ]]; then
  export PATH=\"\\$HOME/.local/bin:\\$PATH\"
fi
${marker_end}"

  for rc in "$HOME/.bashrc" "$HOME/.profile"; do
    [[ -e "$rc" ]] || : > "$rc"
    if ! grep -Fq "$marker_begin" "$rc"; then
      printf "\n%s\n" "$block" >> "$rc"
      echo "Updated PATH in: $rc"
    fi
  done
}

is_gui_session() {
  [[ -n "${DISPLAY:-}" || -n "${WAYLAND_DISPLAY:-}" ]]
}

is_running() {
  local proc="$1"
  command -v pgrep >/dev/null 2>&1 || return 1
  pgrep -x "$proc" >/dev/null 2>&1 && return 0
  pgrep -f "(^|/)$proc(\\s|$)" >/dev/null 2>&1
}

launch_terminal() {
  local title="$1"
  local command_line="$2"

  # Try common terminals. Prefer konsole on KDE.
  if command -v konsole >/dev/null 2>&1; then
    nohup konsole -p tabtitle="$title" -e bash -lc "$command_line" >/dev/null 2>&1 &
    return 0
  fi
  if command -v gnome-terminal >/dev/null 2>&1; then
    nohup gnome-terminal -- bash -lc "$command_line" >/dev/null 2>&1 &
    return 0
  fi
  if command -v kgx >/dev/null 2>&1; then
    nohup kgx -- bash -lc "$command_line" >/dev/null 2>&1 &
    return 0
  fi
  if command -v xterm >/dev/null 2>&1; then
    nohup xterm -T "$title" -e bash -lc "$command_line" >/dev/null 2>&1 &
    return 0
  fi
  return 1
}

auto_launch_engines() {
  if [[ "$LAUNCH_MODE" == "no" ]] || [[ "${HIVEMIND_NO_LAUNCH:-}" == "1" ]]; then
    return 0
  fi
  if ! is_gui_session; then
    return 0
  fi

  local launched=0
  local base_cmd="cd \"$HIVEMIND_ROOT\""

  if command -v codex >/dev/null 2>&1; then
    if ! is_running codex; then
      if launch_terminal "HIVEMIND (Codex)" "$base_cmd; exec codex"; then
        launched=$((launched + 1))
      fi
    fi
  fi

  if command -v claude >/dev/null 2>&1; then
    if ! is_running claude; then
      if launch_terminal "HIVEMIND (Claude)" "$base_cmd; exec claude"; then
        launched=$((launched + 1))
      fi
    fi
  fi

  if [[ "$LAUNCH_MODE" == "yes" ]] && [[ "$launched" -eq 0 ]]; then
    echo "Note: No terminals launched (either engines already running or no supported terminal found)."
  fi
}

chmod +x "$HIVEMIND_ROOT/hivemind"
chmod +x "$HIVEMIND_ROOT/engines/"*.sh
chmod +x "$HIVEMIND_ROOT/bin/"*
chmod +x "$HIVEMIND_ROOT/core/"*.sh

mkdir -p "$HIVEMIND_ROOT/memory/global"
mkdir -p "$HIVEMIND_ROOT/memory/sessions"
mkdir -p "$HIVEMIND_ROOT/memory/agents"
mkdir -p "$HIVEMIND_ROOT/memory/long-term"
mkdir -p "$HIVEMIND_ROOT/memory/episodic"
mkdir -p "$HIVEMIND_ROOT/workspace"
mkdir -p "$HIVEMIND_ROOT/logs"

# Initialize memory (non-destructive)
[[ -f "$HIVEMIND_ROOT/memory/global/context.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/global/context.json"
[[ -f "$HIVEMIND_ROOT/memory/global/learnings.json" ]] || echo '{"entries":[]}' > "$HIVEMIND_ROOT/memory/global/learnings.json"
[[ -f "$HIVEMIND_ROOT/memory/global/preferences.json" ]] || echo '{"entries":[]}' > "$HIVEMIND_ROOT/memory/global/preferences.json"

# Initialize memory files with proper structure (non-destructive)
[[ -f "$HIVEMIND_ROOT/memory/long-term/learnings.json" ]] || echo '{"version":"1.0","entries":[]}' > "$HIVEMIND_ROOT/memory/long-term/learnings.json"
[[ -f "$HIVEMIND_ROOT/memory/long-term/preferences.json" ]] || echo '{"version":"1.0","user_preferences":{"communication_style":null,"detail_level":"standard","code_style":{"language":null,"indentation":"spaces","indent_size":2},"rules":[]}}' > "$HIVEMIND_ROOT/memory/long-term/preferences.json"
[[ -f "$HIVEMIND_ROOT/memory/long-term/decisions.json" ]] || echo '{"version":"1.0","decisions":[]}' > "$HIVEMIND_ROOT/memory/long-term/decisions.json"
[[ -f "$HIVEMIND_ROOT/memory/long-term/project.json" ]] || echo '{"version":"1.0","project":{"name":null,"description":null,"tech_stack":[],"tools":[],"conventions":[],"architecture":null}}' > "$HIVEMIND_ROOT/memory/long-term/project.json"
[[ -f "$HIVEMIND_ROOT/memory/episodic/events.json" ]] || echo '{"version":"1.0","events":[]}' > "$HIVEMIND_ROOT/memory/episodic/events.json"

ensure_user_bin
ensure_path

# Optional symlink to PATH (best-effort)
sudo_ln() {
  local src="$1"
  local dst="$2"

  if [[ "$(id -u)" -eq 0 ]]; then
    ln -sf "$src" "$dst" || true
    return 0
  fi

  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    sudo -n ln -sf "$src" "$dst" || true
    return 0
  fi

  return 1
}

if [[ -d "/usr/local/bin" ]]; then
    if sudo_ln "$HIVEMIND_ROOT/hivemind" /usr/local/bin/hivemind; then
        [[ -L "/usr/local/bin/hivemind" ]] && echo "Installed: /usr/local/bin/hivemind"
    else
        echo "Note: Skipping /usr/local/bin symlink (no passwordless sudo)."
    fi
fi

# Create hm alias
if [[ -d "/usr/local/bin" ]]; then
    sudo_ln "$HIVEMIND_ROOT/bin/hm" /usr/local/bin/hm || true
fi

auto_launch_engines

echo ""
echo "═══════════════════════════════════════════"
echo "        HIVEMIND INSTALLATION COMPLETE     "
echo "═══════════════════════════════════════════"
echo ""
echo "Usage:"
echo "  ./hivemind                  # Interactive mode"
echo "  ./hivemind \"task\"           # Direct task"
echo "  ./hivemind --config         # Show configuration"
echo "  ./hivemind --preset full-codex  # Switch engines"
echo ""
echo "Default configuration:"
echo "  HIVEMIND engine: codex"
echo "  Agent engine:    claude"
echo ""
echo "Run './hivemind' (or 'hm') to start."
