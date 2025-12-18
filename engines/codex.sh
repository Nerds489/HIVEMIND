#!/bin/bash
#
# Codex CLI Adapter for HIVEMIND

set -euo pipefail

source "$(dirname "$0")/engine.sh"

run_codex() {
    local system_prompt="$1"
    local task="$2"
    local mode="${3:-interactive}"

    run_engine "codex" "$system_prompt" "$task" "$mode"
}

run_codex_background() {
    local system_prompt="$1"
    local task="$2"
    local output_dir="$3"

    (
      set -euo pipefail
      run_engine "codex" "$system_prompt" "$task" "print" > "$output_dir/stdout.log" 2>&1
    ) &
    echo $!
}

export -f run_codex
export -f run_codex_background
