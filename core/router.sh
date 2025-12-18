#!/bin/bash
#
# Routing helper (keyword-based)

set -euo pipefail

HIVEMIND_ROOT="${HIVEMIND_ROOT:-$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")" && pwd)}"

choose_agents_for_task() {
  local task="${1:-}"
  if [[ -z "$task" ]]; then
    return 1
  fi

  local routing_json="$HIVEMIND_ROOT/config/routing.json"
  if ! command -v jq >/dev/null 2>&1 || [[ ! -f "$routing_json" ]]; then
    echo "DEV-001"
    return 0
  fi

  local t
  t="$(printf '%s' "$task" | tr '[:upper:]' '[:lower:]')"

  # Choose the best matching rule by lowest priority, then pick primary + up to 2 secondaries.
  jq -r --arg t "$t" '
    .routing_rules.keyword_routing.rules
    | map(select(any(.keywords[]; ($t | contains((. | ascii_downcase)))))))
    | sort_by(.priority)
    | .[0] // empty
    | ([.primary_agent] + (.secondary_agents // []))
    | .[0:3]
    | .[]
  ' "$routing_json" 2>/dev/null | head -n 3
}

export -f choose_agents_for_task
