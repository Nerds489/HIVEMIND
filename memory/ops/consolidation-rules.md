# Automatic Memory Consolidation Rules

## Trigger Conditions

Consolidation runs automatically when:

| Trigger | Condition | Action |
|---------|-----------|--------|
| Session End | Always | Consolidate working memories |
| Index Overflow | entry_count > 100 | Consolidate that index |
| Weekly | Sunday 00:00 | Full consolidation pass |
| Manual | `/memory consolidate` | Immediate consolidation |

---

## Consolidation Actions

### 1. Merge Duplicates

**Detection Criteria:**
- Same type AND same subtype
- Tag overlap > 80%
- Content similarity > 80%

**Merge Process:**
```
1. Keep the NEWER memory
2. Combine unique content fields
3. Union all tags
4. Set supersedes = [older ID]
5. Update older: superseded_by = [newer ID]
6. Archive older memory
7. Update indices
```

### 2. Summarize Verbose Episodic

**Criteria:**
- type = "episodic"
- created_at > 30 days ago
- content.details exists and length > 5000 chars

**Summarization:**
```
1. Extract key facts:
   - What happened
   - Who was involved
   - Outcome
   - Key learnings
2. Replace content.details with summary
3. Add tag: "summarized"
4. Preserve content.timeline (first/last 3 entries)
5. Update updated_at
```

### 3. Promote Patterns

**Criteria:**
- type = "procedural"
- access_count >= 5
- scope = "agent"

**Promotion:**
```
1. Copy memory to team scope
2. Update scope = "team"
3. Update scope_id = team name
4. Add tag: "promoted"
5. Keep original in agent scope
6. Link: original.promoted_to = new ID
```

**Second-level promotion:**
- Team procedural + access_count >= 10 → global

### 4. Archive Stale

**Criteria:**
- access_count = 0 OR last_accessed > 90 days
- priority != "critical"
- NOT tagged "permanent"

**Archive Process:**
```
1. Move to ./archive/
2. Update original _index.json (remove entry)
3. Update ./archive/_index.json (add entry)
4. Preserve full content
```

---

## Conflict Resolution During Consolidation

| Scenario | Resolution |
|----------|------------|
| Both memories have changes | Keep both, flag for review |
| Same user, different times | Latest wins |
| Different users | Keep both as separate |
| Critical vs non-critical | Critical always preserved |

---

## Consolidation Log

All consolidation actions logged to:
`./ops/consolidation-log.json`

```json
{
  "entries": [
    {
      "timestamp": "2025-12-18T00:00:00Z",
      "trigger": "session_end",
      "actions": [
        {
          "type": "merge",
          "source_ids": ["mem_xxx", "mem_yyy"],
          "result_id": "mem_zzz"
        },
        {
          "type": "archive",
          "memory_id": "mem_aaa",
          "reason": "stale"
        }
      ],
      "stats": {
        "memories_merged": 2,
        "memories_archived": 5,
        "memories_promoted": 1
      }
    }
  ]
}
```

---

## Consolidation Exclusions

Never consolidate:
- priority = "critical"
- tags includes "permanent" or "protected"
- created_by = "USER" (without explicit consent)
- type = "semantic" with subtype = "decision"
- Memories < 7 days old

---

## Performance Guidelines

- Process max 50 memories per consolidation run
- Pause 100ms between index updates
- Run intensive consolidation during low-activity periods
- Log all operations for audit trail
