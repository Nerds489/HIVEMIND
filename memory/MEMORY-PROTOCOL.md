# HIVEMIND Memory Protocol

> Complete specification for automatic memory operations.

---

## Core Principles

1. **Zero Manual Intervention**: Memory operations are automatic
2. **Always Persistent**: File-based storage survives everything
3. **Context-Aware**: Right memories loaded for right tasks
4. **Self-Maintaining**: Auto-cleanup, consolidation, organization

---

## Memory Entry Structure

Every memory follows this structure:

```json
{
  "id": "mem_a7b3c9d2e4f1",
  "type": "factual|procedural|episodic|semantic|working",
  "subtype": "specific-category",
  "created_by": "DEV-001|COORDINATOR|SYSTEM|USER",
  "created_at": "2025-12-18T00:00:00Z",
  "updated_at": "2025-12-18T00:00:00Z",
  "scope": "global|team|agent|project|session",
  "scope_id": "specific-identifier",
  "tags": ["tag1", "tag2"],
  "priority": "critical|high|medium|low",
  "ttl": "permanent|P30D|PT4H",
  "content": { },
  "references": [],
  "confidence": 0.95,
  "access_count": 0,
  "last_accessed": null
}
```

---

## Automatic Operations

### On Session Start (ALWAYS)

```
1. Check ./sessions/current.json
   - If exists AND last_activity < 4 hours → CONTINUE session
   - If exists AND last_activity >= 4 hours → ARCHIVE and create NEW
   - If not exists → Create NEW session

2. Load global context:
   - ./global/user-profile.json
   - ./global/system-config.json
   - ./global/terminology.json

3. If project context detected:
   - Load ./projects/[project-id]/context.json
   - Load ./projects/[project-id]/_index.json

4. Update session state:
   - Set last_activity to NOW
   - Set user_context.loaded_profile = true
```

### On Task Receipt (BEFORE PROCESSING)

```
1. Parse task for:
   - Keywords (nouns, technical terms)
   - Entities (files, functions, APIs)
   - Intent (create, fix, review, deploy)

2. Determine relevant scopes:
   - Always: global
   - If team task: team/[team]
   - If agent assigned: agents/[agent-id]
   - If project context: projects/[project]

3. Query memory indices:
   FOR EACH relevant scope:
     - Load _index.json
     - Score entries by:
       * Tag match (weight: 3)
       * Keyword in summary (weight: 2)
       * Recency (weight: 1)
       * Priority boost (critical: +5, high: +3)
       * Access frequency (weight: 0.5)

4. Load top 10 memories by score:
   - Read full memory content
   - Inject into agent context
   - Update access_count and last_accessed

5. Update session working memory:
   - Record task in task_history
   - Update current_task
   - Track entities_mentioned
```

### On Task Completion (ALWAYS)

```
1. Extract learnings:
   - New facts discovered → factual memory
   - Procedures that worked → procedural memory
   - Errors and solutions → procedural memory
   - Decisions made → semantic memory
   - Task summary → episodic memory

2. For each learning:
   - Generate memory ID
   - Determine scope (most specific appropriate)
   - Create memory entry
   - Update relevant _index.json

3. Check for contradictions:
   - Query existing memories with same tags
   - If contradiction found:
     * If new info more recent → supersede old
     * If uncertain → flag for review
     * Update supersedes/superseded_by links

4. Update session state:
   - Append to task_history
   - Clear current_task
   - Record memories_created
```

### On Agent Handoff (ALWAYS)

```
1. Source agent packages:
   {
     "handoff_memory": {
       "working_memory_snapshot": [current working memory],
       "memories_loaded": [IDs of memories in context],
       "memories_created": [IDs created this task],
       "task_summary": "what was done",
       "pending_items": ["what remains"],
       "recommended_context": [IDs for receiving agent]
     }
   }

2. Write to session:
   - Update ./sessions/current.json
   - Record handoff in task_history

3. Receiving agent loads:
   - All memories in memories_loaded
   - All memories in recommended_context
   - working_memory_snapshot as starting context
   - Agent-specific memories from ./agents/[ID]/
```

### On Session End (ALWAYS)

```
1. Consolidate working memory:
   - Review all working memories created
   - Promote significant items to permanent storage
   - Delete ephemeral items

2. Archive session:
   - Copy current.json to ./sessions/archive/
   - Rename with session_id

3. Update indices:
   - Rebuild any modified _index.json
   - Update statistics

4. Create fresh current.json for next session
```

### On Error/Failure (ALWAYS)

```
1. Create episodic memory:
   {
     "type": "episodic",
     "subtype": "error",
     "content": {
       "error_type": "classification",
       "error_message": "what happened",
       "context": "what was being done",
       "resolution": "how it was fixed (if fixed)",
       "prevention": "how to avoid in future"
     },
     "tags": ["error", "error-type", "context-tags"]
   }

2. Link to related memories:
   - Find similar past errors
   - Link procedural memories with fixes

3. Pattern detection:
   - If same error 3+ times → flag as recurring
   - Create procedural memory for prevention
```

---

## Memory ID Generation

Format: `mem_[12 random alphanumeric]`

```
Characters: a-z, 0-9
Length: 12
Example: mem_a7b3c9d2e4f1

Generation:
1. Generate 12 random characters
2. Prefix with "mem_"
3. Check uniqueness across all indices
4. If collision, regenerate
```

---

## Index Structure

Every scope has an `_index.json`:

```json
{
  "version": "1.0.0",
  "last_updated": "2025-12-18T00:00:00Z",
  "entry_count": 0,
  "entries": [
    {
      "id": "mem_xxx",
      "type": "factual",
      "subtype": "preference",
      "tags": ["user", "preference"],
      "summary": "User prefers TypeScript",
      "priority": "medium",
      "created_at": "2025-12-18T00:00:00Z",
      "file_path": "user-profile.json"
    }
  ],
  "tag_index": {
    "user": ["mem_xxx", "mem_yyy"],
    "preference": ["mem_xxx"]
  },
  "type_index": {
    "factual": ["mem_xxx"],
    "procedural": ["mem_yyy"]
  }
}
```

---

## Priority Levels

| Priority | TTL Default | Auto-Load | Examples |
|----------|-------------|-----------|----------|
| critical | permanent | always | Security findings, user profile |
| high | 1 year | context-match | Architecture decisions |
| medium | 90 days | high-score | Task learnings |
| low | 30 days | explicit query | Minor notes |

---

## TTL (Time-to-Live)

| Value | Meaning |
|-------|---------|
| `permanent` | Never expires |
| `P1Y` | 1 year |
| `P90D` | 90 days |
| `P30D` | 30 days |
| `P7D` | 7 days |
| `PT4H` | 4 hours (working memory) |

---

## Conflict Resolution

When memories contradict:

1. **Same scope, same creator**: Latest wins, archive old
2. **Same scope, different creators**: Flag for review
3. **Different scopes**: More specific scope takes precedence
4. **User vs System**: User always wins
5. **Critical priority**: Never auto-overwrite

---

## Consolidation Rules

Automatic consolidation runs:
- On session end
- When entry_count > 100 in any index
- Weekly maintenance

Actions:
- Merge duplicate memories (>80% similar)
- Summarize old episodic memories (>30 days)
- Promote frequently accessed agent memories to team
- Archive unaccessed memories (>90 days)

---

## Backup & Recovery

- All memory is file-based (automatic persistence)
- Git-compatible (can version control memory/)
- Archive contains historical sessions
- Superseded memories retained for rollback

---

## Performance Guidelines

- Index files < 1000 entries (split if larger)
- Memory content < 10KB (summarize if larger)
- Load max 10 memories per task (relevance sorted)
- Archive access_count = 0 memories after 90 days
