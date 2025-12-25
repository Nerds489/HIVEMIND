# HIVEMIND Memory System

## Directory Structure

```
memory/
├── session/       # Current session state
├── project/       # Cross-session project memory
└── agent/         # Per-agent memory profiles
```

## Usage

Memory is managed by HEAD_CODEX and persists:
- Task context
- Agent performance data
- Project decisions
- Learnings

## Format

JSON files with structured data per memory type.
