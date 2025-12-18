# HIVEMIND Memory Commands Reference

> Quick reference for memory operations in the HIVEMIND system.

---

## Memory Query Commands

### Basic Search

```
memory search <query>                    # Free-text search across all accessible memories
memory search <query> --type factual     # Search specific memory type
memory search <query> --scope global     # Search specific scope
memory search <query> --tags api,design  # Filter by tags
```

### Advanced Query

```
memory query --type procedural --tags deployment --scope team:infrastructure
memory query --created-after 2025-01-01 --created-by DEV-001
memory query --priority critical --lifecycle active
memory query --project my-project --type episodic
```

### Query Options

| Option | Values | Description |
|--------|--------|-------------|
| `--type` | factual, procedural, episodic, semantic, working | Memory type filter |
| `--scope` | global, team:*, agent:*, project:* | Scope filter |
| `--tags` | comma-separated | Include tags |
| `--exclude-tags` | comma-separated | Exclude tags |
| `--priority` | critical, high, normal, low | Priority filter |
| `--lifecycle` | active, aging, archived | Lifecycle state |
| `--created-by` | agent-id | Creator filter |
| `--created-after` | ISO date | Date range start |
| `--created-before` | ISO date | Date range end |
| `--limit` | 1-100 | Max results (default: 10) |
| `--format` | full, summary, ids | Output format |

---

## Memory CRUD Operations

### Create Memory

```
memory create --type factual --title "API Rate Limits"
memory create --type procedural --title "Deploy to Production" --scope team:infrastructure
memory create --type episodic --title "Incident 2025-01-15" --tags incident,outage
memory create --type semantic --title "Microservice" --tags architecture
memory create --type working --title "Current Task Context" --expires 2h
```

### Create with Content (Interactive)

```
memory create --type factual --title "Database Connection Strings" <<EOF
Production: postgres://prod.db.internal:5432/app
Staging: postgres://stage.db.internal:5432/app
Development: postgres://localhost:5432/app_dev
EOF
```

### Read Memory

```
memory read <memory-id>                  # Full memory with metadata
memory read <memory-id> --content-only   # Just the content
memory read <memory-id> --json           # JSON output
```

### Update Memory

```
memory update <memory-id> --title "New Title"
memory update <memory-id> --add-tags newtag1,newtag2
memory update <memory-id> --remove-tags oldtag
memory update <memory-id> --priority high
memory update <memory-id> --content                    # Opens editor
memory update <memory-id> --append "Additional info"   # Append to content
```

### Delete Memory

```
memory delete <memory-id>                # Soft delete (moves to deleted lifecycle)
memory delete <memory-id> --hard         # Permanent deletion (requires confirmation)
memory delete <memory-id> --reason "Outdated information"
```

---

## Index Operations

### View Index

```
memory index                             # Show current scope's index summary
memory index --scope global              # Show global index
memory index --scope team:security       # Show team index
memory index --full                      # Full index listing
memory index --stats                     # Index statistics only
```

### Rebuild Index

```
memory index rebuild                     # Rebuild current scope's index
memory index rebuild --scope global      # Rebuild specific scope
memory index rebuild --all               # Rebuild all indexes
memory index validate                    # Validate index integrity
```

---

## Lifecycle Management

### Archive Operations

```
memory archive <memory-id>               # Move to archived state
memory archive --older-than 90d          # Archive memories older than 90 days
memory archive --unused-for 60d          # Archive rarely accessed memories
memory archive --bulk --filter "scope:agent:DEV-001,lifecycle:aging"
```

### Restore Operations

```
memory restore <memory-id>               # Restore from archived
memory restore --list                    # List archived memories
memory restore --search <query>          # Search archived memories
```

### Cleanup

```
memory cleanup --dry-run                 # Preview what would be cleaned
memory cleanup --expired                 # Remove expired working memories
memory cleanup --orphaned                # Remove orphaned memories
memory cleanup --compact                 # Compact storage files
```

---

## Tag Operations

```
memory tags                              # List all tags with counts
memory tags --scope team:development     # Tags in specific scope
memory tags --suggest <memory-id>        # Suggest tags for memory
memory tags --rename old-tag new-tag     # Rename tag globally
memory tags --merge tag1,tag2 into tag3  # Merge tags
```

---

## Context Loading

### Load Context

```
memory context load                      # Load default context for current agent
memory context load --for DEV-001        # Load context for specific agent
memory context load --project my-project # Load project context
memory context load --task "implement auth" # Load task-relevant context
```

### Context Summary

```
memory context show                      # Show currently loaded context
memory context relevant <query>          # Find memories relevant to query
memory context score <memory-id>         # Get relevance score for memory
```

---

## Working Memory

### Session Operations

```
memory working new                       # Start new working memory session
memory working note "Important finding"  # Quick note to working memory
memory working task "Current objective"  # Set current task context
memory working blocker "Waiting for API" # Record blocker
memory working handoff --to DEV-002 "Need frontend implementation"
```

### Session Management

```
memory working show                      # Show current working memory
memory working save                      # Persist working memory to session
memory working clear                     # Clear current working memory
memory working promote <item-id>         # Promote working memory to permanent
```

---

## Project Memory

### Project Operations

```
memory project create my-project --description "New web application"
memory project list                      # List all projects
memory project show my-project           # Show project details
memory project switch my-project         # Set as current project
memory project archive my-project        # Archive project and memories
```

### Project Memory Management

```
memory project memories my-project       # List project memories
memory project import my-project <file>  # Import memories into project
memory project export my-project         # Export project memories
```

---

## Import/Export

### Export

```
memory export <memory-id>                # Export single memory
memory export --scope global --format json > memories.json
memory export --tags architecture --format markdown > arch-docs.md
memory export --project my-project --bundle project-export.zip
```

### Import

```
memory import <file>                     # Import memory file
memory import memories.json --scope team:development
memory import --bundle project-export.zip --project new-project
memory import --validate-only <file>     # Validate without importing
```

---

## Statistics and Reports

```
memory stats                             # Overall memory statistics
memory stats --scope team:security       # Scope-specific stats
memory stats --by-agent                  # Stats grouped by agent
memory stats --by-type                   # Stats grouped by type
memory report usage --last 30d           # Usage report
memory report growth                     # Growth trends
memory report conflicts                  # Conflict report
```

---

## Conflict Resolution

```
memory conflicts                         # List pending conflicts
memory conflicts show <conflict-id>      # Show conflict details
memory conflicts resolve <conflict-id> --strategy latest-wins
memory conflicts resolve <conflict-id> --strategy merge
memory conflicts resolve <conflict-id> --manual   # Manual resolution
```

### Resolution Strategies

| Strategy | Description |
|----------|-------------|
| `latest-wins` | Most recent update wins |
| `expert-wins` | Higher authority agent wins |
| `merge` | Merge non-conflicting fields |
| `branch` | Create separate versions |
| `manual` | Human decision required |

---

## Agent Memory Commands

### For Agents

```
memory agent load                        # Load agent's memory profile
memory agent context                     # Get agent-specific context
memory agent learn <content>             # Add to agent's learned context
memory agent share <memory-id> --with DEV-002  # Share memory with agent
```

### Agent Profile

```
memory agent profile                     # Show agent memory profile
memory agent profile update --auto-load-tags "newtag"
memory agent stats                       # Agent-specific statistics
```

---

## Utility Commands

### Validation

```
memory validate <memory-id>              # Validate memory against schema
memory validate --scope global           # Validate all memories in scope
memory validate --fix                    # Auto-fix validation issues
```

### Maintenance

```
memory doctor                            # Run diagnostic checks
memory optimize                          # Optimize storage and indexes
memory backup                            # Create backup of all memories
memory backup --incremental              # Incremental backup
memory restore-backup <backup-file>      # Restore from backup
```

### Version Control

```
memory history <memory-id>               # Show memory change history
memory diff <memory-id> <version1> <version2>  # Diff between versions
memory rollback <memory-id> <version>    # Rollback to previous version
```

---

## Quick Reference

### Common Workflows

**Store a learning:**
```
memory create --type factual --title "User prefers TypeScript" \
  --tags user,preference,tech-stack \
  --content "User consistently chooses TypeScript for new projects"
```

**Record a decision:**
```
memory create --type episodic --title "Chose PostgreSQL over MySQL" \
  --tags decision,database,architecture \
  --scope project:my-app
```

**Document a procedure:**
```
memory create --type procedural --title "Deploy Hotfix Process" \
  --tags deployment,emergency,runbook \
  --scope team:infrastructure
```

**Find relevant context:**
```
memory context relevant "authentication implementation"
```

**Quick note during work:**
```
memory working note "User mentioned deadline is Friday"
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HIVEMIND_MEMORY_PATH` | Memory directory path | `./memory` |
| `HIVEMIND_AGENT_ID` | Current agent ID | auto-detected |
| `HIVEMIND_PROJECT` | Current project | none |
| `HIVEMIND_MEMORY_FORMAT` | Default output format | `full` |
| `HIVEMIND_AUTO_CONTEXT` | Auto-load context | `true` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Memory not found |
| 3 | Validation error |
| 4 | Permission denied |
| 5 | Conflict detected |
| 6 | Index error |

---

## See Also

- [MEMORY.md](./MEMORY.md) - Full memory system documentation
- [schemas/](./schemas/) - JSON schemas for all memory types
- [global/](./global/) - Global shared memories
- [teams/](./teams/) - Team-scoped memories
- [agents/](./agents/) - Agent-specific memories
