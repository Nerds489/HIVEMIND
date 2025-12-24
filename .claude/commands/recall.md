# Recall Command

Query the HIVEMIND memory system for stored knowledge.

## Usage

```
/recall [query]
/recall --type [type] [query]
/recall --agent [agent-id] [query]
/recall --team [team] [query]
```

## Options

- `--type` - Filter by memory type (factual, procedural, semantic, episodic)
- `--agent` - Search specific agent's memory
- `--team` - Search team knowledge base
- `--recent` - Only memories from last 24h
- `--all` - Include archived memories

## Examples

```
/recall deployment procedures
/recall --type procedural database migrations
/recall --agent DEV-002 API patterns
/recall --team security authentication
/recall --recent decisions
```

## Memory Types

| Type | Contains | Example |
|------|----------|---------|
| `factual` | Facts, preferences, configs | "User prefers snake_case" |
| `procedural` | How-to knowledge | "Steps to deploy to production" |
| `semantic` | Concepts, relationships | "Service A depends on Service B" |
| `episodic` | Past events, decisions | "We chose PostgreSQL because..." |

## Output Format

```
━━━ MEMORY RECALL ━━━
Query: "deployment procedures"
Found: 3 matches

[1] PROCEDURAL | Global | Updated 2d ago
    Production Deployment Steps
    "1. Run migrations 2. Deploy backend 3. Deploy frontend..."

[2] PROCEDURAL | DEV-006 | Updated 1w ago
    Rollback Procedure
    "If deployment fails: 1. Revert image tag 2. Apply previous..."

[3] EPISODIC | Global | Updated 3d ago
    Last Deployment Issue
    "Deployment on 12/19 failed due to missing env var..."

━━━━━━━━━━━━━━━━━━━━━━
```

## Memory Locations

```
memory/
├── global/           # Shared across all agents
├── teams/            # Team-specific knowledge
│   ├── development/
│   ├── security/
│   ├── infrastructure/
│   └── qa/
├── agents/           # Per-agent memory
│   ├── DEV-001/
│   ├── DEV-002/
│   └── ...
└── sessions/         # Current session state
```

## Behavior

1. Searches memory indexes based on query
2. Ranks by relevance and recency
3. Returns top matches with snippets
4. Automatically loads relevant context for next task
