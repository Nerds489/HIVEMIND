#!/bin/bash
#
# HIVEMIND Engine Abstraction Layer
# Provides unified interface for different CLI engines

set -euo pipefail

HIVEMIND_ROOT="${HIVEMIND_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"

# Resolve an executable even when PATH is incomplete (common in GUI launches).
find_executable() {
    local name="$1"

    local from_path
    from_path="$(command -v "$name" 2>/dev/null || true)"
    if [[ -n "$from_path" ]]; then
        echo "$from_path"
        return 0
    fi

    local candidates=()

    # User-local installs
    candidates+=("$HOME/.local/bin/$name")
    candidates+=("$HOME/.cargo/bin/$name")
    candidates+=("$HOME/.bun/bin/$name")
    candidates+=("$HOME/.volta/bin/$name")
    candidates+=("$HOME/.asdf/shims/$name")

    # System locations
    candidates+=("/usr/local/bin/$name")
    candidates+=("/usr/bin/$name")

    # NVM (pick highest version)
    if [[ -d "$HOME/.nvm/versions/node" ]]; then
        local best
        best="$(ls -1d "$HOME/.nvm/versions/node"/v*/bin/"$name" 2>/dev/null | sort -V | tail -n 1 || true)"
        [[ -n "$best" ]] && candidates+=("$best")
    fi

    local p
    for p in "${candidates[@]}"; do
        if [[ -x "$p" ]]; then
            echo "$p"
            return 0
        fi
    done

    return 1
}

# Load engine config
load_engine_config() {
    local engine_type="$1"  # "hivemind" or "agents"

    # Parse engines.yaml to get active engine
    # Using simple grep/sed for portability (or yq if available)
    if command -v yq &> /dev/null; then
        yq -r ".active.$engine_type" "$HIVEMIND_ROOT/config/engines.yaml"
    else
        # Fallback: read from simple config
        grep "^  $engine_type:" "$HIVEMIND_ROOT/config/engines.yaml" | awk '{print $2}'
    fi
}

# Get engine command (name, not resolved path)
get_engine_command() {
    local engine="$1"

    case "$engine" in
        codex)
            echo "codex"
            ;;
        claude-code|claude)
            echo "claude"
            ;;
        *)
            echo "codex"  # Default
            ;;
    esac
}

resolve_engine_command() {
    local engine="$1"
    local name
    name="$(get_engine_command "$engine")"
    find_executable "$name"
}

engine_is_available() {
    local engine="$1"
    resolve_engine_command "$engine" >/dev/null 2>&1
}

is_interactive_tty() {
    [[ -t 0 && -t 1 ]]
}

codex_is_logged_in() {
    local codex_cmd="$1"
    "$codex_cmd" login status >/dev/null 2>&1
}

codex_has_api_key_env() {
    [[ -n "${OPENAI_API_KEY:-}" ]]
}

claude_is_logged_in() {
    [[ -n "${ANTHROPIC_API_KEY:-}" || -n "${CLAUDE_API_KEY:-}" || -f "$HOME/.claude/.credentials.json" ]]
}

prompt_codex_login() {
    local codex_cmd="$1"

    cat >&2 <<'EOF'
Codex is installed but not authenticated.

Choose a login method:
  1) Browser login (device auth)
  2) Paste API key (stdin)
  q) Cancel
EOF
    printf >&2 "Selection: "
    local choice
    read -r choice
    case "$choice" in
        1)
            "$codex_cmd" login --device-auth >&2
            ;;
        2)
            printf >&2 "OPENAI_API_KEY: "
            local key
            IFS= read -rs key
            echo >&2
            printf '%s' "$key" | "$codex_cmd" login --with-api-key >/dev/null
            ;;
        q|Q|"")
            return 1
            ;;
        *)
            echo "Invalid selection." >&2
            return 1
            ;;
    esac
}

prompt_claude_login() {
    local claude_cmd="$1"
    cat >&2 <<'EOF'
Claude is installed but not authenticated.

Tip: Claude Code can authenticate via browser/token.
Press Enter to run: claude setup-token
Or type 'q' to cancel.
EOF
    printf >&2 "Selection: "
    local choice
    read -r choice
    case "$choice" in
        q|Q)
            return 1
            ;;
        *)
            "$claude_cmd" setup-token >&2
            ;;
    esac
}

ensure_engine_ready() {
    local engine="$1"
    local output_mode="$2"

    local cmd
    cmd="$(resolve_engine_command "$engine" 2>/dev/null || true)"
    if [[ -z "$cmd" ]]; then
        echo "Error: engine '$engine' not found (missing '$(get_engine_command "$engine")')." >&2
        echo "Hint: run '$HIVEMIND_ROOT/hivemind --setup' to install/authenticate engines." >&2
        return 127
    fi

    # Only prompt for auth when running interactively.
    case "$engine" in
        codex)
            if [[ "$output_mode" == "interactive" ]] && is_interactive_tty; then
                if ! codex_is_logged_in "$cmd" && ! codex_has_api_key_env; then
                    prompt_codex_login "$cmd" || true
                fi
            else
                if ! codex_is_logged_in "$cmd" && ! codex_has_api_key_env; then
                    echo "Error: Codex is not authenticated (no login + OPENAI_API_KEY not set)." >&2
                    echo "Hint: run '$HIVEMIND_ROOT/hivemind --setup' (or 'codex login --device-auth')." >&2
                    return 78
                fi
            fi
            ;;
        claude|claude-code)
            if [[ "$output_mode" == "interactive" ]] && is_interactive_tty; then
                if ! claude_is_logged_in; then
                    prompt_claude_login "$cmd" || true
                fi
            else
                if ! claude_is_logged_in; then
                    echo "Error: Claude is not authenticated (no credentials + no API key env set)." >&2
                    echo "Hint: run '$HIVEMIND_ROOT/hivemind --setup' (or 'claude setup-token')." >&2
                    return 78
                fi
            fi
            ;;
    esac

    echo "$cmd"
    return 0
}

# Run engine with unified interface
run_engine() {
    local engine="$1"
    local system_prompt="$2"
    local task="$3"
    local output_mode="${4:-interactive}"  # interactive, print, quiet

    local cmd
    cmd="$(ensure_engine_ready "$engine" "$output_mode")" || return $?

    local args=()

    # Add model override if set (otherwise let the CLI pick its default).
    if [[ -n "${HIVEMIND_MODEL:-}" ]]; then
        args+=("--model" "$HIVEMIND_MODEL")
    fi

    case "$engine" in
        codex)
            # Codex does not currently support a dedicated --system-prompt flag.
            # Combine system + task into a single initial prompt for compatibility.
            local combined_prompt
            if [[ -n "$system_prompt" ]]; then
                combined_prompt=$(cat <<EOF
SYSTEM PROMPT:
$system_prompt

TASK:
$task
EOF
)
            else
                combined_prompt="$task"
            fi

            case "$output_mode" in
                interactive)
                    "$cmd" "${args[@]}" "$combined_prompt"
                    ;;
                print|quiet)
                    local out_file
                    out_file="$(mktemp "${TMPDIR:-/tmp}/hivemind_codex_out.XXXXXX")"
                    if [[ "$output_mode" == "quiet" ]]; then
                        "$cmd" exec "${args[@]}" -o "$out_file" "$combined_prompt" >/dev/null 2>&1
                    else
                        # Keep stdout clean (only the final message), send engine chatter to stderr.
                        "$cmd" exec "${args[@]}" -o "$out_file" "$combined_prompt" 1>&2
                    fi
                    cat "$out_file"
                    rm -f "$out_file"
                    ;;
            esac
            ;;
        claude|claude-code)
            # Claude supports an explicit system prompt and print mode.
            if [[ -n "$system_prompt" ]]; then
                args+=("--system-prompt" "$system_prompt")
            fi
            case "$output_mode" in
                interactive)
                    "$cmd" "${args[@]}" "$task"
                    ;;
                print)
                    "$cmd" --print "${args[@]}" "$task"
                    ;;
                quiet)
                    "$cmd" -q "${args[@]}" "$task"
                    ;;
            esac
            ;;
        *)
            echo "Error: unknown engine '$engine'." >&2
            return 2
            ;;
    esac
}

export -f load_engine_config
export -f get_engine_command
export -f find_executable
export -f resolve_engine_command
export -f engine_is_available
export -f run_engine
