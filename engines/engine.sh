#!/bin/bash
#
# HIVEMIND Engine Abstraction Layer
# Provides unified interface for different CLI engines

set -euo pipefail

HIVEMIND_ROOT="${HIVEMIND_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"

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

# Get engine command
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

# Get engine flags
get_engine_flags() {
    local engine="$1"
    local flag_type="$2"

    case "$engine" in
        codex)
            case "$flag_type" in
                model)  echo "--model" ;;
                system) echo "--system-prompt" ;;
                quiet)  echo "--quiet" ;;
                print)  echo "--print" ;;
            esac
            ;;
        claude-code|claude)
            case "$flag_type" in
                model)  echo "--model" ;;
                system) echo "--system-prompt" ;;
                quiet)  echo "-q" ;;
                print)  echo "--print" ;;
            esac
            ;;
    esac
}

# Run engine with unified interface
run_engine() {
    local engine="$1"
    local system_prompt="$2"
    local task="$3"
    local output_mode="${4:-interactive}"  # interactive, print, quiet

    local cmd
    cmd="$(get_engine_command "$engine")"

    local model_flag
    model_flag="$(get_engine_flags "$engine" "model")"

    local system_flag
    system_flag="$(get_engine_flags "$engine" "system")"

    local args=()

    # Add model if set
    if [[ -n "${HIVEMIND_MODEL:-}" ]]; then
        args+=("$model_flag" "$HIVEMIND_MODEL")
    fi

    # Add system prompt
    if [[ -n "$system_prompt" ]]; then
        args+=("$system_flag" "$system_prompt")
    fi

    # Add output mode flags
    case "$output_mode" in
        print)
            args+=("$(get_engine_flags "$engine" "print")")
            ;;
        quiet)
            args+=("$(get_engine_flags "$engine" "quiet")")
            ;;
    esac

    # Add task
    args+=("$task")

    # Execute
    "$cmd" "${args[@]}"
}

export -f load_engine_config
export -f get_engine_command
export -f get_engine_flags
export -f run_engine

