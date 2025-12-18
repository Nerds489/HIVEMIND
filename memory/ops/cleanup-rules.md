# Automatic Memory Cleanup Rules

## Cleanup Schedule

| Frequency | Trigger | Operations |
|-----------|---------|------------|
| Per-Session | Session end | Clear expired working memory |
| Daily | First session of day | Remove expired TTL, validate indices |
| Weekly | Sunday | Archive stale, rebuild indices |
| Monthly | 1st of month | Full audit, compress archives |

---

## Daily Cleanup

### 1. Remove Expired TTL

```
FOR EACH memory in all indices:
  IF ttl != "permanent":
    IF NOW > created_at + ttl:
      Archive memory
      Remove from index
      Log: "TTL expired: {id}"
```

### 2. Clear Empty Sessions

```
FOR EACH file in ./sessions/archive/:
  IF file.task_history.length = 0:
    Delete file
    Log: "Empty session removed: {session_id}"
```

### 3. Validate Indices

```
FOR EACH _index.json:
  FOR EACH entry in entries:
    IF NOT exists(entry.file_path):
      Remove entry from index
      Log: "Orphan entry removed: {id}"

  Recalculate entry_count
  Rebuild tag_index from entries
  Rebuild type_index from entries
  Update last_updated
```

---

## Weekly Cleanup

### 1. Archive Unaccessed Memories

```
FOR EACH memory WHERE:
  - last_accessed < NOW - 60 days
  - access_count < 3
  - priority NOT IN ["critical", "high"]
  - "permanent" NOT IN tags

DO:
  Move to ./archive/
  Update indices
  Log: "Archived unaccessed: {id}"
```

### 2. Consolidate Duplicate Tags

```
Tag normalization:
  - Lowercase all tags
  - Remove duplicates
  - Merge similar: "javascript" = "js"
  - Update all affected memories
  - Rebuild tag_index
```

### 3. Reference Validation

```
FOR EACH memory with references:
  FOR EACH reference:
    IF NOT exists(reference.id):
      Remove reference
      Log: "Broken reference removed: {id} -> {ref_id}"
```

---

## Monthly Cleanup

### 1. Full Index Rebuild

```
FOR EACH scope (global, teams/*, agents/*, projects/*):
  Scan all .json files in directory
  Extract memory entries
  Rebuild _index.json from scratch
  Validate against schema
  Log stats
```

### 2. Remove Orphaned Memories

```
FOR EACH .json file in memory/:
  IF file not in any _index.json:
    IF file is valid memory:
      Add to appropriate index
    ELSE:
      Move to ./archive/orphans/
      Log: "Orphaned file archived: {filename}"
```

### 3. Compress Archives

```
FOR EACH file in ./archive/ older than 90 days:
  Summarize if episodic
  Remove redundant fields
  Update file
  Log: "Compressed: {filename}"
```

---

## Protected from Cleanup

NEVER automatically delete or archive:

| Protection | Criteria |
|------------|----------|
| Critical Priority | `priority = "critical"` |
| Permanent Tag | `"permanent" IN tags` |
| Protected Tag | `"protected" IN tags` |
| Core Tag | `"core" IN tags` |
| User Created | `created_by = "USER"` |
| Recent | `created_at > NOW - 7 days` |
| High Access | `access_count >= 10` |
| System Memory | Reserved IDs |

---

## Cleanup Log

All cleanup actions logged to:
`./ops/gc-log.json`

```json
{
  "entries": [
    {
      "timestamp": "2025-12-18T00:00:00Z",
      "type": "daily",
      "operations": {
        "ttl_expired": 3,
        "empty_sessions": 1,
        "orphan_entries": 2,
        "indices_validated": 8
      },
      "errors": []
    }
  ]
}
```

---

## Manual Cleanup Commands

```bash
/memory cleanup                    # Run daily cleanup
/memory cleanup --weekly           # Run weekly cleanup
/memory cleanup --full             # Run monthly cleanup
/memory cleanup --dry-run          # Preview without changes
/memory validate                   # Validate all indices
/memory rebuild-indices            # Force index rebuild
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Corrupted index | Rebuild from files |
| Missing file | Remove from index, log |
| Invalid JSON | Move to ./archive/corrupted/, log |
| Permission error | Skip, log, alert |

---

## Recovery

If cleanup causes issues:

1. Check `./ops/gc-log.json` for recent actions
2. Archived files preserved in `./archive/`
3. Manual restore: move file back, rebuild index
4. Superseded memories have `superseded_by` reference for rollback
