# HIVEMIND Memory System

> Automatic, persistent, cross-session memory for the HIVEMIND multi-agent system.

## Overview

The memory system provides:
- **Persistent Context**: Survives sessions, restarts, and reboots
- **Shared Knowledge**: Cross-agent learning and knowledge transfer
- **Automatic Operation**: Zero manual intervention required
- **Self-Maintaining**: Auto-consolidation, cleanup, and organization

## Quick Start

Memory is **automatic**. You don't need to do anything. The system:
1. Loads relevant context when you start
2. Captures learnings as you work
3. Saves everything when you finish
4. Restores context in future sessions

## Memory Types

| Type | Purpose | Auto-Captured |
|------|---------|---------------|
| **Factual** | Facts, configs, preferences | User preferences, system settings |
| **Procedural** | How-to knowledge | Successful procedures, fixes |
| **Episodic** | Events, incidents | Tasks completed, errors resolved |
| **Semantic** | Concepts, decisions | Architecture decisions, terminology |
| **Working** | Session context | Current task state, handoffs |

## Memory Scopes

| Scope | Visibility | Location |
|-------|------------|----------|
| `global` | All agents | `./global/` |
| `team` | Team members | `./teams/[team]/` |
| `agent` | Single agent | `./agents/[ID]/` |
| `project` | Project context | `./projects/[name]/` |
| `session` | Current session | `./sessions/current.json` |

## Directory Structure

```
memory/
├── README.md                 # This file
├── MEMORY-PROTOCOL.md        # How memory works
├── TRIGGERS.md               # Automatic trigger map
├── QUERY.md                  # Query interface
├── schemas/                  # JSON schemas
├── global/                   # System-wide memories
├── teams/                    # Team-scoped memories
├── agents/                   # Agent-specific memories
├── projects/                 # Project memories
├── sessions/                 # Session state
├── archive/                  # Archived memories
└── ops/                      # Operations config
```

## Commands

```bash
/remember [content]           # Save a memory
/recall [query]               # Search memories
/memories                     # List relevant memories
/memory [id]                  # Show specific memory
/memory-status                # System health
```

## Key Files

- `MEMORY-PROTOCOL.md` - Detailed operation protocol
- `TRIGGERS.md` - When memories are auto-created
- `QUERY.md` - How to search memories
- `global/user-profile.json` - Your preferences
- `sessions/current.json` - Current session state

## How It Works

1. **Session Start**: Loads user profile, system config, relevant context
2. **Task Processing**: Queries memories for relevant knowledge
3. **During Work**: Updates working memory, tracks entities
4. **Task Complete**: Captures learnings, updates indices
5. **Session End**: Archives session, consolidates memories

See `MEMORY-PROTOCOL.md` for complete details.
