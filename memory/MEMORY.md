# HIVEMIND Memory System

```
███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗
████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗╚██╗ ██╔╝
██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝ ╚████╔╝
██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗  ╚██╔╝
██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║
╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝

      Persistent Intelligence for HIVEMIND Agents
```

## Overview

The HIVEMIND Memory System provides persistent, shared, and contextual memory across all 24 agents. It enables agents to learn from past interactions, share knowledge, maintain project context across sessions, and continuously improve their performance.

### Core Principles

1. **Persistence** - Memory survives session boundaries
2. **Shareability** - Agents can read/write shared memories
3. **Isolation** - Project and agent-specific memories stay scoped
4. **Scalability** - System grows without becoming unwieldy
5. **Discoverability** - Memories are indexed and searchable
6. **Lifecycle** - Memories age, archive, and cleanup automatically

---

## Architecture

### Directory Structure

```
memory/
├── MEMORY.md                    # This documentation
├── schemas/                     # JSON schemas for validation
│   ├── memory-entry.json        # Base memory schema
│   ├── factual.json             # Factual memory schema
│   ├── procedural.json          # Procedural memory schema
│   ├── episodic.json            # Episodic memory schema
│   ├── semantic.json            # Semantic memory schema
│   ├── working.json             # Working memory schema
│   ├── index.json               # Index file schema
│   └── query.json               # Query request schema
│
├── global/                      # Shared across ALL agents
│   ├── _index.json              # Global memory index
│   ├── facts/                   # Factual memories
│   │   ├── user-profile.json    # User preferences & history
│   │   ├── system-config.json   # System configurations
│   │   └── codebase-map.json    # Repository knowledge
│   ├── procedures/              # How-to knowledge
│   │   ├── successful-patterns.json
│   │   ├── failed-approaches.json
│   │   └── optimizations.json
│   └── learnings/               # Accumulated wisdom
│       ├── best-practices.json
│       ├── lessons-learned.json
│       └── domain-knowledge.json
│
├── teams/                       # Team-scoped memories
│   ├── development/
│   │   ├── _index.json
│   │   ├── coding-standards.json
│   │   ├── architecture-decisions.json
│   │   └── tech-debt.json
│   ├── security/
│   │   ├── _index.json
│   │   ├── threat-models.json
│   │   ├── vulnerability-patterns.json
│   │   └── incident-history.json
│   ├── infrastructure/
│   │   ├── _index.json
│   │   ├── system-inventory.json
│   │   ├── runbooks.json
│   │   └── capacity-baselines.json
│   └── qa/
│       ├── _index.json
│       ├── test-strategies.json
│       ├── defect-patterns.json
│       └── coverage-baselines.json
│
├── agents/                      # Agent-specific memories
│   ├── DEV-001/                 # Architect's personal memory
│   │   ├── _index.json
│   │   ├── design-patterns.json
│   │   └── preferences.json
│   ├── DEV-002/                 # Backend Developer
│   ├── ... (all 24 agents)
│   └── QA-006/
│
├── projects/                    # Project-isolated memories
│   ├── _index.json              # Project registry
│   └── [project-id]/
│       ├── _meta.json           # Project metadata
│       ├── _index.json          # Project memory index
│       ├── context.json         # Project context
│       ├── decisions.json       # Project decisions
│       ├── tasks/               # Task memories
│       └── artifacts/           # Referenced artifacts
│
├── sessions/                    # Session memories
│   ├── active/
│   │   └── [session-id].json    # Current session context
│   └── completed/
│       └── [session-id].json    # Archived sessions
│
├── working/                     # Ephemeral working memory
│   ├── current-task.json        # Active task context
│   ├── handoffs.json            # Pending handoffs
│   ├── blockers.json            # Active blockers
│   └── scratch.json             # Temporary notes
│
├── user/                        # User-specific memories
│   ├── profile.json             # User preferences
│   ├── history.json             # Interaction history
│   ├── feedback.json            # User corrections/feedback
│   └── projects.json            # User's project list
│
└── archive/                     # Archived memories
    ├── memories/                # Old memories by date
    │   └── YYYY-MM/
    └── sessions/                # Old sessions
        └── YYYY-MM/
```

---

## Memory Types

### 1. Factual Memory

**Purpose:** Store facts, configurations, and objective information.

**Storage:** JSON files in `global/facts/`, team directories, or project directories.

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| fact_type | enum | user_pref, config, codebase, entity, relationship |
| subject | string | What the fact is about |
| predicate | string | The relationship or property |
| object | any | The value or related entity |
| confidence | float | 0.0-1.0 confidence level |
| source | string | Where this fact came from |
| verified | boolean | Human-verified or not |

**Examples:**
- User prefers TypeScript over JavaScript
- Project uses PostgreSQL 15
- Main API endpoint is at /api/v1

**Retention:** Permanent until explicitly updated or deleted.

**Access:** All agents can read; specific agents can write based on domain.

---

### 2. Procedural Memory

**Purpose:** Store "how-to" knowledge - successful approaches, failed attempts, optimizations.

**Storage:** JSON files in `global/procedures/` or team directories.

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| procedure_type | enum | success, failure, optimization, pattern |
| task_category | string | Type of task this applies to |
| context | object | When this procedure applies |
| steps | array | Steps or approach taken |
| outcome | string | What happened |
| metrics | object | Performance metrics if available |
| applicability | array | Conditions when to use/avoid |

**Examples:**
- When deploying to production, always run smoke tests first
- Don't use recursive CTEs for this database - causes timeouts
- For React performance issues, check useMemo/useCallback first

**Retention:** Long-term; reviewed quarterly for relevance.

**Access:** All agents read; relevant agents write based on task type.

---

### 3. Episodic Memory

**Purpose:** Store event-based memories - what happened, when, outcomes.

**Storage:** JSON files in project directories or `archive/`.

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| episode_type | enum | task, incident, decision, conversation, milestone |
| timestamp | ISO8601 | When it happened |
| participants | array | Agents/users involved |
| summary | string | Brief description |
| details | object | Full episode details |
| outcome | string | How it ended |
| lessons | array | Key takeaways |
| references | array | Related memories/artifacts |

**Examples:**
- On 2024-01-15, deployed v2.0 with zero downtime
- Security assessment on 2024-01-10 found 3 high-severity issues
- User asked about authentication patterns (link to conversation)

**Retention:** 1 year active, then archived. Incidents kept 3 years.

**Access:** All agents read; creating agent writes.

---

### 4. Semantic Memory

**Purpose:** Store conceptual knowledge - definitions, relationships, domain models.

**Storage:** JSON files in `global/learnings/` or team directories.

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| concept | string | The concept name |
| definition | string | What it means in this context |
| category | string | Domain category |
| relationships | array | Related concepts |
| examples | array | Concrete examples |
| anti_examples | array | What it's NOT |
| context_notes | string | Context-specific understanding |

**Examples:**
- "User" in this system means authenticated customer, not admin
- "Deploy" means push to staging first, then production
- The "Order" entity connects Customer → Product → Payment

**Retention:** Permanent until domain changes.

**Access:** All agents read; domain experts write.

---

### 5. Working Memory

**Purpose:** Store ephemeral, session-specific context - current task, active state.

**Storage:** JSON files in `working/` directory.

**Schema Fields:**
| Field | Type | Description |
|-------|------|-------------|
| memory_type | enum | task, handoff, blocker, note |
| created_at | ISO8601 | Creation time |
| expires_at | ISO8601 | Auto-cleanup time |
| priority | enum | P0-P4 |
| content | object | The actual content |
| agent_id | string | Owning agent |
| status | enum | active, pending, resolved |

**Examples:**
- Currently working on: API endpoint implementation
- Pending handoff: Code ready for review (DEV-002 → DEV-004)
- Blocker: Waiting for database schema from INF-004

**Retention:** Session-length; cleared on session end or resolution.

**Access:** All agents read/write.

---

## Memory Operations

### CREATE

**Automatic Creation Triggers:**
| Trigger | Memory Type | Location |
|---------|-------------|----------|
| User states preference | Factual | user/profile.json |
| Task completed successfully | Procedural | global/procedures/ |
| Task failed with lesson | Procedural | global/procedures/ |
| New project started | Episodic | projects/[id]/ |
| Decision made | Episodic | projects/[id]/decisions.json |
| New concept introduced | Semantic | global/learnings/ |
| Handoff initiated | Working | working/handoffs.json |

**Manual Creation:**
```
/remember [type] [content]
/remember fact "User prefers dark mode in all interfaces"
/remember procedure "For this repo, run npm install before npm test"
/remember decision "Using PostgreSQL over MySQL for ACID compliance"
```

**Validation Rules:**
1. Memory must have valid type
2. Content must not be empty
3. Duplicate detection (similarity > 0.9 triggers merge prompt)
4. Size limits: 10KB per memory, 1MB per index
5. Required fields must be present per schema

**Creation Response:**
```json
{
  "status": "created",
  "memory_id": "MEM-20240115-ABC123",
  "location": "global/facts/user-profile.json",
  "indexed": true,
  "related_memories": ["MEM-20240110-XYZ789"]
}
```

---

### READ

**Query Syntax:**
```
/recall [query]
/recall "user preferences for code style"
/recall --type procedural --tag deployment
/recall --project my-project --recent 7d
/recall --agent DEV-001 --type semantic
```

**Query Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| --type | Memory type filter | factual, procedural, episodic |
| --scope | Scope filter | global, team, agent, project |
| --tag | Tag filter | deployment, security, api |
| --agent | Agent filter | DEV-001, SEC-002 |
| --team | Team filter | development, security |
| --project | Project filter | project-id |
| --recent | Time filter | 7d, 30d, 1y |
| --limit | Result limit | 10 (default 5) |
| --format | Output format | summary, full, refs |

**Relevance Scoring:**
```
Score = (keyword_match × 0.3) +
        (recency × 0.2) +
        (access_frequency × 0.2) +
        (scope_match × 0.2) +
        (agent_relevance × 0.1)
```

**Context Loading Budget:**
- Maximum: 50 memories per query
- Token budget: ~8000 tokens for memory context
- Prioritization: Higher relevance scores loaded first
- Summarization: Memories > 500 tokens auto-summarized

---

### UPDATE

**Update Syntax:**
```
/update-memory [memory-id] [changes]
/update-memory MEM-20240115-ABC123 --content "Updated preference"
/update-memory MEM-20240115-ABC123 --tag add:important
/update-memory MEM-20240115-ABC123 --verified true
```

**Conflict Resolution:**

When two agents attempt to update the same memory:

1. **Last-Write-Wins (default for working memory)**
   - Most recent update takes precedence
   - Previous value logged in history

2. **Merge (default for factual/semantic)**
   - Attempt automatic merge
   - If conflict, flag for human resolution
   - Both versions preserved until resolved

3. **Append (default for episodic/procedural)**
   - New information appended, not replaced
   - Creates version chain

**Version History:**
```json
{
  "current_version": 3,
  "versions": [
    {"version": 1, "timestamp": "...", "author": "DEV-001", "content": "..."},
    {"version": 2, "timestamp": "...", "author": "SEC-001", "content": "..."},
    {"version": 3, "timestamp": "...", "author": "DEV-001", "content": "..."}
  ]
}
```

---

### DELETE / ARCHIVE

**Deletion Types:**

1. **Soft Delete (Archive)**
   - Memory moved to `archive/`
   - Metadata retained for reference
   - Recoverable for 90 days

2. **Hard Delete**
   - Memory permanently removed
   - Requires explicit confirmation
   - Audit log entry created

**Archive Syntax:**
```
/archive-memory [memory-id]
/archive-memory MEM-20240115-ABC123 --reason "outdated"
```

**Delete Syntax:**
```
/delete-memory [memory-id] --confirm
```

**Automatic Cleanup Rules:**
| Memory Type | Cleanup Trigger | Action |
|-------------|-----------------|--------|
| Working | Session end | Delete |
| Working | 24h no access | Archive |
| Episodic | > 1 year old | Archive |
| Procedural | 0 accesses in 6 months | Flag for review |
| Factual | Contradicted by newer fact | Flag for review |
| Session | Session complete | Move to completed/ |

**Protected Memories (Never Auto-Delete):**
- User profile
- Critical incidents
- Architecture decisions (ADRs)
- Compliance-related facts
- Memories tagged `protected`

---

## Memory Indexing

### Index Structure

Each directory with memories has an `_index.json`:

```json
{
  "index_version": "1.0",
  "last_updated": "2024-01-15T10:30:00Z",
  "memory_count": 42,
  "memories": [
    {
      "id": "MEM-20240115-ABC123",
      "type": "factual",
      "title": "User prefers TypeScript",
      "tags": ["user", "preferences", "language"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "access_count": 5,
      "last_accessed": "2024-01-15T14:00:00Z",
      "file": "user-profile.json",
      "path": "$.preferences.language",
      "summary": "User prefers TypeScript for all new projects",
      "relevance_hints": ["typescript", "javascript", "language choice"]
    }
  ],
  "tag_counts": {
    "user": 10,
    "preferences": 8,
    "deployment": 15
  },
  "type_counts": {
    "factual": 20,
    "procedural": 12,
    "episodic": 10
  }
}
```

### Tag Taxonomy

```yaml
# Hierarchical tag structure
tags:
  domain:
    - development
    - security
    - infrastructure
    - quality

  lifecycle:
    - active
    - archived
    - deprecated
    - protected

  priority:
    - critical
    - important
    - normal
    - low

  scope:
    - global
    - team
    - agent
    - project
    - session

  content:
    - preference
    - decision
    - procedure
    - incident
    - lesson
    - fact
    - concept

  technology:
    - python
    - javascript
    - typescript
    - react
    - postgresql
    - kubernetes
    - terraform
    # (extensible)
```

### Auto-Tagging Rules

```yaml
auto_tag_rules:
  - pattern: "user prefer|user like|user want"
    tags: [user, preferences]

  - pattern: "deploy|release|production"
    tags: [deployment, infrastructure]

  - pattern: "security|vulnerability|exploit"
    tags: [security, critical]

  - pattern: "test|coverage|qa"
    tags: [quality, testing]

  - pattern: "error|fail|bug|issue"
    tags: [incident, debugging]

  - pattern: "decision|chose|decided|selected"
    tags: [decision]

  - pattern: "learned|realized|discovered"
    tags: [lesson]
```

### Cross-Reference Maps

`_references.json` in each directory:

```json
{
  "references": {
    "MEM-20240115-ABC123": {
      "references": ["MEM-20240110-XYZ789", "MEM-20240112-DEF456"],
      "referenced_by": ["MEM-20240116-GHI012"],
      "related_projects": ["project-alpha"],
      "related_agents": ["DEV-001", "DEV-002"]
    }
  }
}
```

---

## Context Loading

### Automatic Loading Rules

**Per Agent Type:**

| Agent | Auto-Load Memories |
|-------|-------------------|
| DEV-001 (Architect) | architecture-decisions, tech-debt, system-inventory |
| DEV-002 (Backend) | coding-standards, api-patterns, database-schemas |
| DEV-003 (Frontend) | ui-patterns, component-library, a11y-standards |
| DEV-004 (Reviewer) | coding-standards, review-checklist, past-reviews |
| SEC-001 (Security Arch) | threat-models, security-standards, compliance |
| SEC-002 (Pentester) | vulnerability-patterns, exploit-history |
| SEC-006 (Incident) | incident-history, runbooks, escalation-contacts |
| INF-001 (Infra Arch) | system-inventory, capacity-baselines, cloud-configs |
| INF-005 (SRE) | runbooks, monitoring-config, incident-history |
| QA-001 (QA Arch) | test-strategies, coverage-baselines, defect-patterns |

**Per Task Type:**

| Task Keywords | Auto-Load |
|--------------|-----------|
| "deploy", "release" | deployment-procedures, rollback-runbook |
| "review", "PR" | coding-standards, past-reviews |
| "security", "pentest" | vulnerability-patterns, threat-models |
| "incident", "outage" | incident-history, runbooks |
| "new project" | user-profile, project-templates |
| "debug", "fix" | related-incidents, known-issues |

**Per Project:**

When project ID detected:
1. Load `projects/[id]/_meta.json`
2. Load `projects/[id]/context.json`
3. Load recent `projects/[id]/tasks/`
4. Load relevant `projects/[id]/decisions.json`

### On-Demand Loading

```
# Explicit memory requests
/recall "authentication patterns we've used"
/load-context project:alpha task:api-design
/memories --relevant-to "database optimization"
```

### Context Budget Management

```yaml
context_budget:
  total_tokens: 8000
  allocation:
    user_profile: 500      # Always loaded
    project_context: 1500  # If project active
    task_relevant: 3000    # Highest relevance
    agent_specific: 1500   # Agent's default memories
    recent_episodes: 1500  # Recent interactions

  overflow_strategy:
    - summarize memories > 500 tokens
    - drop lowest relevance first
    - preserve user_profile always
    - log dropped memories for reference
```

---

## Memory Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ CREATION │───►│  ACTIVE  │───►│  AGING   │───►│ ARCHIVED │───►│ DELETED  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │               │
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
  Validate      Accessed         Stale          Compressed       Purged
  Index         Updated          Flagged        Indexed          Logged
  Tag           Referenced       Reviewed       Recoverable      Audit
```

### Lifecycle Transitions

| Transition | Criteria | Action |
|------------|----------|--------|
| Creation → Active | Passes validation | Index, tag, notify |
| Active → Aging | No access for 30d (factual) or 7d (working) | Flag for review |
| Aging → Active | Accessed again | Reset aging timer |
| Aging → Archived | Confirmed stale OR 90d in aging | Move to archive/, compress |
| Archived → Active | Explicit restore | Decompress, re-index |
| Archived → Deleted | 90d in archive + not protected | Purge, audit log |

### Lifecycle Commands

```
/memory-status [memory-id]     # Check lifecycle state
/extend-memory [memory-id]     # Reset aging timer
/protect-memory [memory-id]    # Mark as protected
/restore-memory [memory-id]    # Restore from archive
```

---

## Cross-Agent Memory Sharing

### Direct Sharing

**Write-Read Pattern:**
```
Agent DEV-002 writes:
  /remember procedure "For this API, use JWT with 1h expiry"
  → Saved to: teams/development/api-patterns.json
  → Indexed with: [api, authentication, jwt]

Agent DEV-003 reads (auto):
  Task: "Implement login form"
  → Auto-loads: teams/development/api-patterns.json
  → Sees: "For this API, use JWT with 1h expiry"
```

**Subscription Pattern:**
```json
// Agent memory profile subscription
{
  "agent_id": "DEV-003",
  "subscriptions": [
    {"scope": "teams/development", "types": ["procedural", "factual"]},
    {"scope": "global/facts", "tags": ["frontend", "ui"]},
    {"agent": "DEV-002", "types": ["procedural"]}  // Subscribe to specific agent
  ]
}
```

### Memory Handoffs

When work transfers between agents, memory context transfers too:

```json
{
  "handoff_id": "HO-20240115-001",
  "from_agent": "DEV-002",
  "to_agent": "DEV-004",
  "memory_package": {
    "include_memories": [
      "MEM-20240115-ABC123",  // Specific relevant memories
      "MEM-20240114-DEF456"
    ],
    "include_context": {
      "task": "working/current-task.json",
      "decisions": "projects/alpha/decisions.json#recent"
    },
    "summary": "API endpoint complete, needs review for auth handling"
  }
}
```

### Conflict Resolution

**Scenario: Two agents have different "facts" about the same thing**

```json
{
  "conflict_id": "CONF-20240115-001",
  "memory_subject": "database connection limit",
  "conflicting_values": [
    {"agent": "INF-004", "value": 100, "timestamp": "2024-01-10"},
    {"agent": "DEV-002", "value": 50, "timestamp": "2024-01-15"}
  ],
  "resolution_strategy": "latest_wins",  // or "expert_wins", "human_decides"
  "resolved_value": 50,
  "resolution_note": "INF-004 confirmed DEV-002's value after checking config"
}
```

**Resolution Strategies:**
1. **latest_wins** - Most recent update wins
2. **expert_wins** - Domain expert agent's value wins
3. **human_decides** - Flag for human resolution
4. **merge** - Combine if compatible
5. **branch** - Keep both with context labels

---

## Project Memory Isolation

### Project Container

```
projects/
└── alpha-api/
    ├── _meta.json           # Project metadata
    ├── _index.json          # Project memory index
    ├── context.json         # Project context
    ├── decisions.json       # ADRs for this project
    ├── entities.json        # Domain entities
    ├── tasks/
    │   ├── TASK-001.json    # Task memories
    │   └── TASK-002.json
    └── artifacts/
        └── references.json  # Links to artifacts
```

**Project Metadata:**
```json
{
  "project_id": "alpha-api",
  "name": "Alpha API Project",
  "created_at": "2024-01-01T00:00:00Z",
  "status": "active",
  "team": "development",
  "lead_agent": "DEV-001",
  "participants": ["DEV-001", "DEV-002", "DEV-003", "QA-002"],
  "tags": ["api", "backend", "priority"],
  "memory_policy": {
    "retention": "project_lifetime",
    "sharing": "participants_only",
    "inherit_from": "templates/api-project"
  }
}
```

### Project Lifecycle

**Creation:**
```
/new-project [name] --template [template]
```
- Creates project directory
- Copies template memories if specified
- Initializes indexes
- Registers in projects/_index.json

**Active:**
- All project memories scoped to directory
- Cross-project access requires explicit reference
- Project context auto-loads for participants

**Completion:**
```
/complete-project [project-id]
```
- Mark as completed
- Archive task memories
- Preserve decisions and learnings
- Update statistics

**Archival:**
```
/archive-project [project-id]
```
- Move to archive/projects/
- Compress memories
- Retain in search (with archived flag)

---

## Memory File Formats

### Base Memory Entry Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "created_at", "created_by", "content"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^MEM-[0-9]{8}-[A-Z0-9]{6}$"
    },
    "type": {
      "enum": ["factual", "procedural", "episodic", "semantic", "working"]
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "created_by": {
      "type": "string",
      "pattern": "^(DEV|SEC|INF|QA)-[0-9]{3}$|^USER$|^SYSTEM$"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_by": {
      "type": "string"
    },
    "scope": {
      "enum": ["global", "team", "agent", "project", "session"]
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"}
    },
    "priority": {
      "enum": ["critical", "high", "normal", "low"]
    },
    "ttl": {
      "type": "string",
      "description": "Time-to-live: null (permanent), '30d', '1y', etc."
    },
    "protected": {
      "type": "boolean",
      "default": false
    },
    "content": {
      "type": "object"
    },
    "references": {
      "type": "array",
      "items": {"type": "string"}
    },
    "access_count": {
      "type": "integer",
      "default": 0
    },
    "last_accessed": {
      "type": "string",
      "format": "date-time"
    },
    "version": {
      "type": "integer",
      "default": 1
    }
  }
}
```

### Factual Memory Content

```json
{
  "content": {
    "fact_type": "preference",
    "subject": "user",
    "predicate": "prefers",
    "object": "TypeScript",
    "context": "for all new projects",
    "confidence": 1.0,
    "source": "user statement",
    "verified": true,
    "verification_date": "2024-01-15T10:30:00Z"
  }
}
```

### Procedural Memory Content

```json
{
  "content": {
    "procedure_type": "success",
    "task_category": "deployment",
    "title": "Zero-downtime deployment to production",
    "context": {
      "system": "kubernetes",
      "environment": "production",
      "scale": "> 100 pods"
    },
    "prerequisites": [
      "All tests passing",
      "Staging deployment verified"
    ],
    "steps": [
      "Create new deployment with updated image",
      "Wait for rollout status",
      "Run smoke tests",
      "Switch traffic gradually (10% → 50% → 100%)",
      "Monitor error rates for 15 minutes",
      "Mark deployment complete or rollback"
    ],
    "outcome": "Successful deployment with 0 errors",
    "metrics": {
      "duration_minutes": 25,
      "error_rate": 0,
      "rollback_needed": false
    },
    "applicability": {
      "use_when": ["production deployment", "stateless services"],
      "avoid_when": ["database migrations", "breaking changes"]
    }
  }
}
```

### Episodic Memory Content

```json
{
  "content": {
    "episode_type": "incident",
    "title": "Database connection exhaustion",
    "timestamp": "2024-01-10T14:30:00Z",
    "duration_minutes": 45,
    "severity": "P1",
    "participants": ["INF-004", "INF-005", "DEV-002"],
    "summary": "Production database ran out of connections causing 503 errors",
    "timeline": [
      {"time": "14:30", "event": "Alerts fired for 503 errors"},
      {"time": "14:35", "event": "INF-005 identified connection pool exhaustion"},
      {"time": "14:45", "event": "INF-004 increased pool size"},
      {"time": "15:00", "event": "Services recovered"},
      {"time": "15:15", "event": "Root cause identified: connection leak in new code"}
    ],
    "root_cause": "Connection leak in payment service introduced in v2.3.1",
    "resolution": "Hotfix deployed to close connections properly",
    "lessons": [
      "Add connection pool monitoring",
      "Code review should check for connection handling",
      "Set connection timeout to prevent accumulation"
    ],
    "prevention": [
      "Added connection pool size alert",
      "Updated code review checklist",
      "Added integration test for connection cleanup"
    ]
  }
}
```

### Query Schema

```json
{
  "query": {
    "text": "deployment procedures for kubernetes",
    "filters": {
      "type": ["procedural"],
      "scope": ["global", "team:infrastructure"],
      "tags": ["deployment", "kubernetes"],
      "created_after": "2024-01-01",
      "created_by": ["INF-001", "INF-005"]
    },
    "options": {
      "limit": 10,
      "offset": 0,
      "sort": "relevance",
      "include_archived": false,
      "format": "summary"
    }
  }
}
```

---

## Agent Memory Integration

### Agent Memory Profile

Each agent has a memory profile in their agent file:

```yaml
# Addition to agent .md files
## Memory Profile

### Default Subscriptions
- global/facts/system-config.json
- teams/development/_index.json
- global/procedures/coding-standards.json

### Write Permissions
- teams/development/*
- agents/DEV-002/*
- projects/*/tasks/*

### Read Permissions
- global/*
- teams/development/*
- teams/security/* (read-only)
- agents/DEV-002/*
- projects/* (participant projects)

### Auto-Save Triggers
| Event | Memory Type | Location |
|-------|-------------|----------|
| Task completed | episodic | projects/[id]/tasks/ |
| Decision made | episodic | projects/[id]/decisions.json |
| Pattern discovered | procedural | teams/development/ |
| Bug fixed | procedural | global/procedures/ |
| User preference stated | factual | user/profile.json |

### Context Loading Priority
1. Current project context
2. Active task memories
3. Subscribed team memories
4. Recent relevant episodes
5. Global procedures for task type
```

### Memory-Aware Prompting

Update to CLAUDE.md:

```markdown
## Memory Integration

### Pre-Task Memory Loading

Before executing any task:

1. **Identify Memory Scope**
   - Is this within a project? Load project context
   - What task type? Load relevant procedures
   - Which agent(s) involved? Load agent subscriptions

2. **Load User Profile**
   - Always load: memory/user/profile.json
   - Check for relevant preferences

3. **Load Relevant Context**
   - Query: /recall --relevant-to "[task description]" --limit 10
   - Load highest-relevance memories within budget

4. **Check for Precedents**
   - Has similar task been done before?
   - Were there issues/lessons learned?

### During-Task Memory Updates

1. **Track Decisions**
   - Major decisions → save to working/scratch.json
   - Will commit to decisions.json at task end

2. **Note Discoveries**
   - New patterns found → note for procedural memory
   - New facts learned → note for factual memory

3. **Record Blockers**
   - Any blockers → save to working/blockers.json
   - Include what was tried

### Post-Task Memory Commits

1. **Commit Episodic Memory**
   - Task summary → projects/[id]/tasks/[task-id].json
   - Include: what, outcome, duration, participants

2. **Commit Learnings**
   - Successful new approaches → global/procedures/
   - Failures with lessons → global/procedures/failed-approaches.json

3. **Update Facts**
   - Any new facts discovered → appropriate factual memory
   - User preferences stated → user/profile.json

4. **Clear Working Memory**
   - Resolve blockers
   - Clear scratch notes
   - Archive completed handoffs
```

### Memory Commands Reference

```markdown
## Memory Commands

### Recall Commands
/recall [query]                    # Search memories by text
/recall --type [type]              # Filter by type
/recall --scope [scope]            # Filter by scope
/recall --tag [tag]                # Filter by tag
/recall --recent [time]            # Recent memories (7d, 30d)
/recall --project [id]             # Project memories
/recall --agent [id]               # Agent memories

### Remember Commands
/remember [content]                # Auto-detect type
/remember fact "[content]"         # Save as factual
/remember procedure "[content]"    # Save as procedural
/remember decision "[content]"     # Save as episodic decision
/remember lesson "[content]"       # Save as learning

### Memory Management
/memories                          # List relevant memories
/memory-status [id]                # Check memory status
/update-memory [id] [changes]      # Update memory
/archive-memory [id]               # Archive memory
/delete-memory [id] --confirm      # Delete memory
/protect-memory [id]               # Mark as protected
/restore-memory [id]               # Restore from archive

### Project Memory
/project-context                   # Show current project memory
/new-project [name]                # Create project with memory
/switch-project [id]               # Switch project context
/project-memories [id]             # List project memories

### Session Memory
/session-context                   # Show current session
/save-session                      # Save session state
/load-session [id]                 # Load previous session
/clear-session                     # Clear working memory

### Maintenance
/memory-stats                      # Memory system statistics
/memory-health                     # Check for issues
/consolidate-memories              # Merge related memories
/cleanup-memories                  # Archive stale memories
```

---

## Memory Maintenance

### Consolidation

**Automated Consolidation Rules:**

```yaml
consolidation:
  # Merge similar memories
  similarity_threshold: 0.85

  # Summarize verbose memories
  summarize_above_tokens: 1000

  # Deduplicate
  duplicate_detection: true

  # Run schedule
  schedule: "weekly"

  actions:
    - merge_similar_facts
    - summarize_long_episodes
    - deduplicate_procedures
    - update_indexes
```

**Manual Consolidation:**
```
/consolidate-memories --scope global --dry-run
/consolidate-memories --type procedural --execute
```

### Validation

**Validation Checks:**

| Check | Frequency | Action on Failure |
|-------|-----------|-------------------|
| Schema validation | On write | Reject write |
| Reference integrity | Daily | Flag broken refs |
| Index consistency | Daily | Rebuild index |
| Duplicate detection | Weekly | Flag for merge |
| Staleness check | Weekly | Flag for review |
| Size limits | On write | Reject or split |

**Validation Command:**
```
/memory-health
```

Output:
```
Memory System Health Report
===========================
Total memories: 342
  - Factual: 89
  - Procedural: 78
  - Episodic: 120
  - Semantic: 35
  - Working: 20

Index Status: OK
  - Last rebuilt: 2024-01-15T00:00:00Z
  - Entries indexed: 342/342

Issues Found: 2
  - [WARN] MEM-20240110-ABC123: No access in 45 days
  - [WARN] MEM-20240105-DEF456: References deleted memory

Recommendations:
  - Review 2 aging memories
  - Fix 1 broken reference
```

### Optimization

**Storage Optimization:**
```yaml
optimization:
  # Compress archived memories
  compress_archived: true
  compression: gzip

  # Split large files
  max_file_size_kb: 500
  split_strategy: "by_date"

  # Index optimization
  index_rebuild_threshold: 100  # Rebuild after N changes

  # Archive cold memories
  archive_after_days:
    working: 1
    episodic: 365
    procedural: 180  # If no access
    factual: null    # Never auto-archive
```

---

## Special Memory Categories

### User Profile Memory

**Location:** `memory/user/profile.json`

```json
{
  "user_id": "default",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",

  "identity": {
    "name": null,
    "role": "developer",
    "timezone": "UTC",
    "locale": "en-US"
  },

  "preferences": {
    "language": "TypeScript",
    "framework": "React",
    "editor": "VSCode",
    "style": {
      "code_style": "functional",
      "naming": "camelCase",
      "comments": "minimal"
    },
    "communication": {
      "verbosity": "concise",
      "examples": "prefer",
      "explanations": "when_asked"
    }
  },

  "expertise": {
    "strong": ["TypeScript", "React", "Node.js"],
    "familiar": ["Python", "PostgreSQL"],
    "learning": ["Rust", "Kubernetes"]
  },

  "project_history": [
    {
      "project_id": "alpha-api",
      "role": "lead",
      "dates": "2024-01-01 to present"
    }
  ],

  "feedback_history": [
    {
      "date": "2024-01-10",
      "type": "correction",
      "content": "Prefers async/await over .then()",
      "applied": true
    }
  ]
}
```

### Codebase Memory

**Location:** `memory/global/facts/codebase-map.json`

```json
{
  "repository": {
    "name": "my-project",
    "type": "monorepo",
    "language": "TypeScript",
    "framework": "Next.js"
  },

  "structure": {
    "src/": "Source code",
    "src/app/": "Next.js app router pages",
    "src/components/": "React components",
    "src/lib/": "Utility functions",
    "src/api/": "API route handlers",
    "tests/": "Test files",
    "docs/": "Documentation"
  },

  "key_files": {
    "src/lib/auth.ts": "Authentication utilities",
    "src/lib/db.ts": "Database connection",
    "src/api/users/route.ts": "User API endpoints"
  },

  "patterns": {
    "api_pattern": "REST with /api/v1 prefix",
    "component_pattern": "Functional components with hooks",
    "state_pattern": "React Query for server state, Zustand for client"
  },

  "conventions": {
    "naming": "camelCase for functions, PascalCase for components",
    "imports": "Absolute imports from @/",
    "testing": "Colocated test files with .test.ts suffix"
  },

  "known_issues": [
    {
      "location": "src/lib/legacy.ts",
      "issue": "Legacy code, needs refactoring",
      "priority": "low"
    }
  ]
}
```

### Decision Memory (ADR)

**Location:** `memory/projects/[id]/decisions.json`

```json
{
  "decisions": [
    {
      "id": "ADR-001",
      "title": "Use PostgreSQL for primary database",
      "date": "2024-01-05",
      "status": "accepted",
      "context": "Need relational database for complex queries and ACID compliance",
      "decision": "Use PostgreSQL 15 with Prisma ORM",
      "alternatives_considered": [
        {
          "option": "MySQL",
          "rejected_because": "Less feature-rich JSON support"
        },
        {
          "option": "MongoDB",
          "rejected_because": "Need strong consistency for financial data"
        }
      ],
      "consequences": {
        "positive": ["ACID compliance", "Rich query capabilities"],
        "negative": ["Horizontal scaling more complex"],
        "neutral": ["Team already familiar with PostgreSQL"]
      },
      "participants": ["DEV-001", "INF-004"],
      "references": ["MEM-20240105-DB001"]
    }
  ]
}
```

---

## Implementation Checklist

### Phase 1: Core Structure (Day 1)

- [x] Create directory structure
- [ ] Create base schemas
  - [ ] memory-entry.json
  - [ ] index.json
  - [ ] query.json
- [ ] Create initial indexes
  - [ ] global/_index.json
  - [ ] teams/*/_index.json
  - [ ] projects/_index.json
- [ ] Create user profile template
- [ ] Create MEMORY.md documentation

### Phase 2: Memory Operations (Day 2-3)

- [ ] Implement CREATE operations
  - [ ] Memory validation
  - [ ] Auto-tagging
  - [ ] Index updates
- [ ] Implement READ operations
  - [ ] Query parsing
  - [ ] Search/filter
  - [ ] Relevance scoring
- [ ] Implement UPDATE operations
  - [ ] Version tracking
  - [ ] Conflict detection
- [ ] Implement DELETE/ARCHIVE
  - [ ] Soft delete to archive
  - [ ] Hard delete with confirm
  - [ ] Automatic cleanup

### Phase 3: Agent Integration (Day 4-5)

- [ ] Update CLAUDE.md with memory integration
- [ ] Add memory profile section to each agent
- [ ] Create memory command handlers
- [ ] Implement context loading logic
- [ ] Add auto-save triggers

### Phase 4: Advanced Features (Day 6-7)

- [ ] Implement project isolation
- [ ] Add session management
- [ ] Create consolidation routines
- [ ] Add validation/health checks
- [ ] Implement cross-agent sharing

### Phase 5: Testing & Refinement (Day 8+)

- [ ] Test all memory commands
- [ ] Test lifecycle transitions
- [ ] Test conflict resolution
- [ ] Performance optimization
- [ ] Documentation finalization

---

## Example Scenarios

### Scenario 1: New Project Onboarding

**User:** "Start a new project called 'payment-api'"

**Memory Actions:**
1. Create `projects/payment-api/` directory
2. Initialize `_meta.json` with project info
3. Initialize `_index.json` empty
4. Create `context.json` with basic structure
5. Load user profile preferences
6. Load relevant templates from `templates/api-project/`
7. Register in `projects/_index.json`

**Resulting Memory:**
```
projects/payment-api/
├── _meta.json
├── _index.json
├── context.json
└── decisions.json (empty)
```

### Scenario 2: Recurring Task

**User (Week 1):** "How do I deploy to production?"

**Memory Actions:**
1. No existing memory → provide answer
2. Save procedure: `/remember procedure "Production deployment: ..."`
3. Index in `global/procedures/`

**User (Week 2):** "Deploy to production"

**Memory Actions:**
1. Search: `/recall --type procedural "deploy production"`
2. Find: MEM-from-week-1
3. Load and apply procedure
4. Note: Access count incremented

### Scenario 3: Multi-Agent Workflow

**Security Assessment Workflow:**

```
SEC-001 (Security Architect)
  → Loads: threat-models.json, security-standards.json
  → Creates: assessment-context in working memory
  → Handoff to SEC-002 with memory package

SEC-002 (Pentester)
  → Receives: assessment-context
  → Loads: vulnerability-patterns.json
  → Creates: findings in project memory
  → Handoff to QA-004 with findings ref

QA-004 (Security Tester)
  → Receives: findings reference
  → Loads: test-strategies.json
  → Creates: test-results in project memory
  → Commits: lessons-learned to global
```

### Scenario 4: Learning from Mistakes

**Interaction:**
```
User: "Use MySQL for this"
Agent: [uses PostgreSQL]
User: "No, I said MySQL"
```

**Memory Actions:**
1. Detect correction
2. Save to `user/feedback.json`:
   ```json
   {
     "date": "2024-01-15",
     "type": "correction",
     "context": "database choice",
     "incorrect": "PostgreSQL",
     "correct": "MySQL",
     "learned": "Check user specification before applying defaults"
   }
   ```
3. Update user profile if pattern emerges
4. Flag for procedural memory if generalizable

### Scenario 5: Context Continuity

**Session End:**
1. Save session state to `sessions/active/SESSION-001.json`:
   ```json
   {
     "session_id": "SESSION-001",
     "started_at": "2024-01-15T10:00:00Z",
     "ended_at": "2024-01-15T12:00:00Z",
     "project": "payment-api",
     "task_summary": "Implemented user authentication endpoint",
     "working_state": {
       "current_file": "src/api/auth/route.ts",
       "pending_items": ["Add rate limiting", "Write tests"],
       "blockers": []
     },
     "memories_created": ["MEM-20240115-AUTH01"],
     "decisions_made": ["ADR-002: JWT for auth tokens"]
   }
   ```

**Next Session Start:**
1. Detect project from cwd or user mention
2. Load: `projects/payment-api/context.json`
3. Load: Recent session `sessions/completed/SESSION-001.json`
4. Present: "Last session you were implementing auth. Pending: rate limiting, tests."
5. Auto-load relevant memories from last session

---

*Memory System v1.0 - HIVEMIND Persistent Intelligence*
