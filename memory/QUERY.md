# Memory Query Interface

> How to search and retrieve memories from the HIVEMIND memory system.

---

## Query Commands

### Basic Search

```
/recall [keywords]
```

Searches all accessible memories for matching content.

**Examples:**
```
/recall authentication
/recall user login bug
/recall deployment procedure
```

### Filtered Search

```
/recall [options] [keywords]
```

**Options:**
- `type:[type]` - Filter by memory type
- `scope:[scope]` - Filter by scope
- `tags:[tag1,tag2]` - Filter by tags
- `agent:[id]` - Filter by creator
- `recent:[duration]` - Filter by recency
- `priority:[level]` - Filter by priority

**Examples:**
```
/recall type:procedural deployment
/recall scope:team:security vulnerability
/recall tags:api,authentication login
/recall agent:DEV-001 architecture
/recall recent:7d bug fix
/recall priority:critical security
```

### Combined Filters

```
/recall type:procedural scope:team recent:30d tags:deployment aws
```

---

## Query Format (JSON)

For programmatic queries:

```json
{
  "query": {
    "text": "keyword search text",
    "type": ["factual", "procedural"],
    "scope": "global|team|agent|project",
    "scope_id": "development",
    "tags": {
      "include": ["tag1", "tag2"],
      "exclude": ["tag3"],
      "match": "all|any"
    },
    "created_by": "DEV-001",
    "created_after": "2025-01-01T00:00:00Z",
    "created_before": "2025-12-31T23:59:59Z",
    "priority": ["critical", "high"],
    "limit": 10,
    "offset": 0,
    "sort": "relevance|recency|priority|access_count",
    "sort_direction": "desc|asc"
  }
}
```

---

## Query Shortcuts

### By Type

| Shortcut | Expands To |
|----------|------------|
| `/facts [query]` | `/recall type:factual [query]` |
| `/procedures [query]` | `/recall type:procedural [query]` |
| `/events [query]` | `/recall type:episodic [query]` |
| `/concepts [query]` | `/recall type:semantic [query]` |
| `/decisions [query]` | `/recall type:semantic subtype:decision [query]` |

### By Scope

| Shortcut | Expands To |
|----------|------------|
| `/global [query]` | `/recall scope:global [query]` |
| `/team [query]` | `/recall scope:team [query]` |
| `/project [query]` | `/recall scope:project [query]` |
| `/my [query]` | `/recall scope:agent:[current-agent] [query]` |

### By Recency

| Shortcut | Expands To |
|----------|------------|
| `/recent [query]` | `/recall recent:7d [query]` |
| `/today [query]` | `/recall recent:1d [query]` |
| `/thisweek [query]` | `/recall recent:7d [query]` |
| `/thismonth [query]` | `/recall recent:30d [query]` |

---

## List Commands

### List Memories

```
/memories                    # Recent relevant memories
/memories --all              # All accessible memories
/memories --type procedural  # Filter by type
/memories --scope team       # Filter by scope
/memories --limit 20         # Set limit
```

### View Specific Memory

```
/memory [id]                 # Full memory details
/memory mem_a7b3c9d2e4f1     # Example
```

### Memory Status

```
/memory-status               # System overview
```

Shows:
- Total memories by scope
- Total memories by type
- Recent activity
- Health status

---

## Search Algorithm

### Relevance Scoring

Memories are scored by:

| Factor | Weight | Description |
|--------|--------|-------------|
| Tag match | 3.0 | Each matching tag |
| Keyword in title | 2.5 | Query keyword in title |
| Keyword in summary | 2.0 | Query keyword in summary |
| Keyword in content | 1.0 | Query keyword in content |
| Priority boost | +5/+3/+1/0 | critical/high/medium/low |
| Recency boost | 0-1.0 | Newer = higher |
| Access frequency | 0.5 | Per access count |

### Scoring Formula

```
score = (tag_matches * 3.0) +
        (title_matches * 2.5) +
        (summary_matches * 2.0) +
        (content_matches * 1.0) +
        priority_boost +
        (recency_factor * 1.0) +
        (access_count * 0.1)
```

### Result Ordering

1. Filter by query criteria
2. Calculate relevance scores
3. Sort by score (descending)
4. Apply limit
5. Return top N results

---

## Index-Based Search

For performance, queries first search `_index.json` files:

```
1. Load relevant _index.json files
2. Filter entries by query criteria
3. Score matching entries
4. Load full content for top results
5. Re-score with full content
6. Return final results
```

### Index Fields Searched

- `id` - Exact match
- `type` - Exact match
- `subtype` - Exact match
- `tags` - Array contains
- `summary` - Text search
- `priority` - Exact match
- `created_at` - Range comparison

---

## Query Context

Queries automatically consider:

### Current Context
- Active project (scope to project memories)
- Current agent (include agent memories)
- Active workflow (include workflow memories)

### User Context
- User preferences (from user-profile)
- Recent queries (for relevance)
- Access patterns (for personalization)

---

## Query Examples

### Find Deployment Procedures

```
/recall type:procedural tags:deployment,production
```

### Find Recent Security Issues

```
/recall scope:team:security type:episodic recent:30d vulnerability
```

### Find Architecture Decisions for Project

```
/recall scope:project type:semantic subtype:decision architecture
```

### Find All Runbooks

```
/procedures tags:runbook scope:team:infrastructure
```

### Find User Preferences

```
/recall scope:global type:factual tags:user,preference
```

### Complex Query

```json
{
  "query": {
    "text": "authentication api",
    "type": ["factual", "procedural"],
    "scope": "team",
    "scope_id": "development",
    "tags": {
      "include": ["api", "security"],
      "match": "any"
    },
    "created_after": "2025-06-01T00:00:00Z",
    "priority": ["critical", "high"],
    "limit": 5,
    "sort": "relevance"
  }
}
```

---

## Query Performance

### Optimization Tips

1. Use specific types when known
2. Use tags for filtering (indexed)
3. Limit scope when possible
4. Use date ranges to narrow results
5. Set reasonable limits

### Performance Targets

- Index search: < 100ms
- Full content search: < 500ms
- Complex queries: < 1s

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No results | No matches | Broaden query |
| Too many results | Query too broad | Add filters |
| Invalid query | Syntax error | Check format |
| Scope access denied | Permission | Check agent scope |
