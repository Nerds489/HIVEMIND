# Status Command

Display current HIVEMIND system status and agent activity.

## Usage

```
/status [filter]
```

## Filters

- `(none)` - Quick overview
- `agents` - All 24 agents with current state
- `teams` - Team-level summary
- `memory` - Memory system stats
- `engine` - Active engine details
- `full` - Complete system status

## Examples

```
/status
/status agents
/status teams
/status memory
/status full
```

## Output: Quick Overview

```
━━━ HIVEMIND STATUS ━━━
State: ACTIVE
Engine: claude (claude-sonnet-4)
Uptime: 45m 23s

Teams:
  DEV ●●●●○○  4/6 ready
  SEC ●●●●●●  6/6 ready
  INF ●●●●●○  5/6 ready
  QA  ●●●●●●  6/6 ready

Memory: 42 entries loaded
Last task: 2m ago
━━━━━━━━━━━━━━━━━━━━━━━
```

## Output: Full Status

```
━━━ HIVEMIND FULL STATUS ━━━

SYSTEM
  State: ACTIVE
  Version: 1.0.0
  Started: 2024-12-22 14:30:00
  
ENGINE
  Active: claude
  Model: claude-sonnet-4-20250514
  Fallback: codex (available)
  
DEVELOPMENT TEAM
  DEV-001 Architect      ● Ready
  DEV-002 Backend        ● Ready
  DEV-003 Frontend       ● Ready
  DEV-004 Reviewer       ● Ready
  DEV-005 Writer         ○ Idle
  DEV-006 DevOps         ○ Idle

[... continues for all teams ...]

MEMORY
  Global: 15 entries
  Teams: 27 entries
  Sessions: 3 active
  Last write: 5m ago

RECENT ACTIVITY
  14:45 DEV-002 → API implementation
  14:42 SEC-002 → Security review
  14:38 QA-002 → Test automation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Behavior

This is an informational command that:
1. Does not route to any specific agent
2. Reads system state from memory and config
3. Formats output for terminal display
4. Updates in real-time if used in interactive mode
