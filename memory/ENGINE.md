# ACTIVE LEARNING ENGINE

## ON EVERY TASK COMPLETION
1. Extract: What worked? What didn't?
2. Pattern: Is this similar to past tasks?
3. Store: Add to learnings with confidence score
4. Link: Connect to related memories

## CONFIDENCE SCORING
- New learning: 0.3
- Confirmed by success: +0.2
- Contradicted by failure: -0.3
- User corrected: set to 0.9
- User confirmed: set to 1.0

## AUTO-CONSOLIDATION (end of session)
- Merge similar learnings
- Promote high-confidence to permanent
- Demote low-confidence to review
- Archive stale episodic memories

## FORGETTING PROTOCOL
- confidence < 0.2 after 5 sessions → delete
- contradicted 3+ times → delete
- explicitly told to forget → delete immediately

---

# HIVEMIND Memory Engine (Reference)

> File-based persistent memory with automatic triggers and recall.

---

## Memory Schema

### Entry Structure

Every memory entry follows this schema:

```json
{
  "id": "mem_[12-char-alphanumeric]",
  "type": "fact|pattern|preference|decision|event|anti_pattern",
  "content": "The actual information",
  "tags": ["searchable", "tags"],
  "confidence": 0.0-1.0,
  "created_at": "ISO8601 timestamp",
  "updated_at": "ISO8601 timestamp",
  "access_count": 0,
  "source": "user|system|inferred"
}
```

---

## Storage Operations

### STORE

Write new memory to appropriate file:

```
STORE(content, type, tags):
  1. Generate ID: "mem_" + 12 random alphanumeric
  2. Create entry with timestamp
  3. Determine target file:
     - fact, pattern, anti_pattern → learnings.json
     - preference, rule → preferences.json
     - tech_stack, tool, convention → project.json
     - decision → decisions.json
     - event, incident, milestone → events.json
  4. Append to entries array
  5. Return ID
```

### RECALL

Query memories by relevance:

```
RECALL(query, filters):
  1. Parse query into keywords
  2. For each memory file:
     - Score entries by:
       * Tag match: +3 per matching tag
       * Content keyword match: +2 per keyword
       * Recency: +1 if < 7 days old
       * Access frequency: +0.5 per access
       * Confidence: multiply by confidence score
  3. Sort by score descending
  4. Return top 10 matches
```

### UPDATE

Modify existing memory:

```
UPDATE(id, new_content):
  1. Find entry by ID
  2. Update content
  3. Set updated_at to now
  4. Increment access_count
```

### DELETE

Remove memory:

```
DELETE(id):
  1. Find entry by ID
  2. Remove from entries array
  3. Log deletion in episodic/events.json
```

---

## Auto-Trigger Detection

Scan every user message for these patterns:

### Storage Triggers

| Pattern | Action | File | Type |
|---------|--------|------|------|
| `remember that...` | STORE rest of sentence | learnings.json | fact |
| `don't forget...` | STORE rest of sentence | learnings.json | fact |
| `we decided...` | STORE decision | decisions.json | decision |
| `the decision is...` | STORE decision | decisions.json | decision |
| `I prefer...` | STORE preference | preferences.json | preference |
| `I like...` | STORE preference | preferences.json | preference |
| `always...` | STORE rule | preferences.json | rule |
| `never...` | STORE anti-rule | preferences.json | rule |
| `our stack is...` | STORE tech stack | project.json | tech_stack |
| `we use...` | STORE tool | project.json | tool |
| `our convention is...` | STORE convention | project.json | convention |
| `the fix was...` | STORE pattern | learnings.json | pattern |
| `the solution is...` | STORE pattern | learnings.json | pattern |
| `this worked...` | STORE pattern | learnings.json | pattern |
| `this didn't work...` | STORE anti-pattern | learnings.json | anti_pattern |
| `the problem was...` | STORE anti-pattern | learnings.json | anti_pattern |

### Recall Triggers

| Pattern | Action |
|---------|--------|
| `what did we decide about...` | RECALL from decisions.json |
| `how do we...` | RECALL from learnings.json |
| `what's our...` | RECALL from project.json |
| `remind me...` | RECALL from all files |
| `what do we know about...` | RECALL from all files |

---

## Session Lifecycle

### On Session Start

```
1. Generate session_id
2. Set started_at to now
3. Load long-term memories:
   - Read preferences.json → apply to response style
   - Read project.json → set project context
   - Read learnings.json → prepare for recall
   - Read decisions.json → prepare for recall
4. Initialize short-term files:
   - context.json: new session state
   - working.json: empty
   - decisions.json: empty
```

### During Session

```
On every message:
1. Update context.json with message
2. Scan for storage triggers → STORE
3. Scan for recall triggers → RECALL
4. Update last_activity timestamp
5. Track active agents in context
```

### On Session End

```
1. Review short-term/decisions.json
   - Promote important decisions to long-term
2. Extract patterns from conversation
   - Successful solutions → learnings.json
   - Failed attempts → learnings.json (anti_pattern)
3. Archive session summary to episodic/events.json
4. Clear short-term files
```

---

## Memory Injection

When processing a task, inject relevant memories:

```
INJECT_CONTEXT(task):
  1. Extract keywords from task
  2. RECALL relevant memories
  3. For each recalled memory:
     - Add to agent context
     - Increment access_count
  4. Return enriched context
```

### Injection Points

- Before routing: Load general preferences
- After routing: Load domain-specific learnings
- Before response: Check for relevant decisions
- After response: Check for storage opportunities

---

## Consolidation

Periodic cleanup to maintain quality:

### Duplicate Detection

```
CONSOLIDATE_DUPLICATES():
  For each file:
    1. Compare entries by content similarity (>80%)
    2. If duplicates found:
       - Keep highest confidence version
       - Merge tags
       - Sum access_counts
       - Delete others
```

### Staleness Check

```
CONSOLIDATE_STALE():
  For each entry:
    1. If access_count == 0 AND age > 90 days:
       - Move to archive (don't delete)
    2. If confidence < 0.5 AND age > 30 days:
       - Flag for review
```

### Conflict Resolution

```
RESOLVE_CONFLICTS():
  For entries with same tags:
    1. If content contradicts:
       - Prefer more recent
       - Prefer higher confidence
       - Prefer user-sourced over inferred
    2. Mark superseded entry
```

---

## File Schemas

### learnings.json

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": "mem_abc123def456",
      "type": "pattern",
      "content": "Use connection pooling for database performance",
      "tags": ["database", "performance", "postgres"],
      "confidence": 0.95,
      "created_at": "2025-12-18T10:00:00Z",
      "updated_at": "2025-12-18T10:00:00Z",
      "access_count": 5,
      "source": "user"
    }
  ]
}
```

### preferences.json

```json
{
  "version": "1.0",
  "user_preferences": {
    "communication_style": "concise",
    "detail_level": "high",
    "code_style": {
      "language": "python",
      "indentation": "spaces",
      "indent_size": 4
    },
    "rules": [
      {
        "id": "mem_rule001",
        "type": "rule",
        "content": "Always use type hints in Python",
        "created_at": "2025-12-18T10:00:00Z"
      }
    ]
  }
}
```

### project.json

```json
{
  "version": "1.0",
  "project": {
    "name": "MyProject",
    "description": "A web application",
    "tech_stack": ["Python", "FastAPI", "PostgreSQL", "React"],
    "tools": ["Docker", "GitHub Actions", "Terraform"],
    "conventions": ["REST API naming", "GitFlow branching"],
    "architecture": "Microservices"
  }
}
```

### decisions.json

```json
{
  "version": "1.0",
  "decisions": [
    {
      "id": "mem_dec001",
      "type": "decision",
      "content": "Use JWT for authentication with 15-minute expiry",
      "tags": ["auth", "jwt", "security"],
      "rationale": "Balance between security and UX",
      "created_at": "2025-12-18T10:00:00Z",
      "context": "Authentication system design"
    }
  ]
}
```

### events.json

```json
{
  "version": "1.0",
  "events": [
    {
      "id": "evt_001",
      "type": "milestone",
      "content": "Initial system deployment",
      "timestamp": "2025-12-18T10:00:00Z",
      "tags": ["deployment", "launch"]
    }
  ]
}
```

---

## Integration Notes

- All memory operations are SILENT - never expose to user
- Memory enriches responses but is never mentioned
- Failed operations log to events.json but don't interrupt flow
- Memory is a background enhancement, not a user feature
