#!/bin/bash
#
# Claude Code CLI Adapter for HIVEMIND

set -euo pipefail

source "$(dirname "$0")/engine.sh"

run_claude_code() {
    local system_prompt="$1"
    local task="$2"
    local mode="${3:-interactive}"

    run_engine "claude-code" "$system_prompt" "$task" "$mode"
}

run_claude_code_background() {
    local system_prompt="$1"
    local task="$2"
    local output_dir="$3"

    claude --print \
           --system-prompt "$system_prompt" \
           "$task" \
           > "$output_dir/stdout.log" 2>&1 &

    echo $!
}

export -f run_claude_code
export -f run_claude_code_background

