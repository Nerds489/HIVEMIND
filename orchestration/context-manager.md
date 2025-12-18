# HIVEMIND Context Manager

## Overview

The Context Manager maintains shared state between agents, ensuring information persists across handoffs and enabling intelligent context retrieval. It acts as the collective memory of HIVEMIND.

---

## Core Functions

```
┌─────────────────────────────────────────────────────────────────────┐
│                       CONTEXT MANAGER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │   STORE     │  │  RETRIEVE   │  │   RELATE    │  │   EXPIRE   │ │
│  │   Context   │  │   Context   │  │   Context   │  │   Context  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    CONTEXT STORE                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│  │  │  Tasks   │  │ Decisions│  │ Artifacts│  │ Sessions │    │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Context Types

### 1. Task Context
Information about active and completed tasks.

```json
{
  "task_context": {
    "task_id": "TASK-DEV-20240115-001",
    "title": "Implement User Authentication API",
    "status": "in_progress",
    "created_at": "2024-01-15T09:00:00Z",
    "updated_at": "2024-01-15T14:30:00Z",

    "ownership": {
      "created_by": "DEV-001",
      "current_owner": "DEV-002",
      "team": "Development"
    },

    "requirements": {
      "original_request": "Build OAuth 2.0 authentication",
      "acceptance_criteria": [
        "Support Google and GitHub OAuth",
        "Token refresh mechanism",
        "Rate limiting on auth endpoints"
      ],
      "constraints": ["Must use existing user table schema"]
    },

    "progress": {
      "phase": "implementation",
      "completion_percentage": 65,
      "milestones_completed": ["design_approved", "backend_started"],
      "milestones_remaining": ["testing", "security_review", "deployment"]
    },

    "related_tasks": ["TASK-SEC-20240115-001", "TASK-QA-20240115-001"],
    "blocking_tasks": [],
    "blocked_by": []
  }
}
```

### 2. Decision Context
Record of decisions made during task execution.

```json
{
  "decision_context": {
    "decision_id": "DEC-20240115-001",
    "task_id": "TASK-DEV-20240115-001",
    "made_by": "DEV-001",
    "made_at": "2024-01-15T10:00:00Z",

    "decision": {
      "title": "Use JWT for session tokens",
      "description": "Chose JWT over opaque tokens for the authentication system",
      "rationale": "Stateless verification reduces database load, standard format enables easier integration",
      "alternatives_considered": [
        {"option": "Opaque tokens", "rejected_because": "Requires database lookup on every request"},
        {"option": "Session cookies", "rejected_because": "Doesn't work well for API-only access"}
      ]
    },

    "impact": {
      "affected_components": ["auth_service", "api_gateway", "user_service"],
      "affected_agents": ["DEV-002", "SEC-001", "INF-001"]
    },

    "approval": {
      "required": true,
      "approved_by": "SEC-001",
      "approved_at": "2024-01-15T11:00:00Z"
    },

    "reversible": true,
    "reversal_cost": "medium"
  }
}
```

### 3. Artifact Context
Tracking of produced deliverables.

```json
{
  "artifact_context": {
    "artifact_id": "ART-20240115-001",
    "task_id": "TASK-DEV-20240115-001",
    "created_by": "DEV-002",
    "created_at": "2024-01-15T14:00:00Z",

    "artifact": {
      "type": "code",
      "name": "Authentication Service",
      "path": "/src/services/auth/",
      "description": "OAuth 2.0 authentication service implementation",
      "version": "0.1.0"
    },

    "validation": {
      "tests_run": true,
      "tests_passed": 45,
      "tests_failed": 0,
      "coverage": "87%",
      "lint_status": "clean",
      "security_scan": "pending"
    },

    "dependencies": {
      "depends_on": ["ART-20240114-005"],
      "depended_by": []
    },

    "retention": {
      "policy": "permanent",
      "classification": "internal"
    }
  }
}
```

### 4. Session Context
State for ongoing multi-agent interactions.

```json
{
  "session_context": {
    "session_id": "SES-20240115-001",
    "started_at": "2024-01-15T09:00:00Z",
    "last_activity": "2024-01-15T14:30:00Z",
    "status": "active",

    "participants": [
      {"agent": "DEV-001", "role": "initiator", "joined_at": "2024-01-15T09:00:00Z"},
      {"agent": "DEV-002", "role": "implementer", "joined_at": "2024-01-15T10:00:00Z"},
      {"agent": "SEC-001", "role": "reviewer", "joined_at": "2024-01-15T11:00:00Z"}
    ],

    "workflow": "full-sdlc",
    "current_phase": "implementation",

    "shared_state": {
      "design_approved": true,
      "security_requirements_defined": true,
      "test_plan_created": false
    },

    "conversation_summary": "Designing and implementing OAuth 2.0 authentication. Architecture approved, JWT chosen for tokens, implementation 65% complete."
  }
}
```

---

## Context Operations

### Store Context

```python
def store_context(context_type: str, context_data: dict) -> str:
    """
    Store context in the appropriate store.

    Args:
        context_type: One of 'task', 'decision', 'artifact', 'session'
        context_data: The context payload

    Returns:
        context_id: Unique identifier for stored context
    """
    context_id = generate_context_id(context_type)

    # Add metadata
    context_data['_metadata'] = {
        'id': context_id,
        'type': context_type,
        'stored_at': now(),
        'stored_by': current_agent(),
        'version': 1
    }

    # Store in appropriate location
    store_path = f"/artifacts/context/{context_type}/{context_id}.json"
    write_json(store_path, context_data)

    # Index for retrieval
    update_context_index(context_type, context_id, context_data)

    return context_id
```

### Retrieve Context

```python
def retrieve_context(
    context_type: str = None,
    task_id: str = None,
    agent_id: str = None,
    keywords: list = None,
    time_range: tuple = None
) -> list:
    """
    Retrieve relevant context based on filters.

    Returns list of matching context objects, sorted by relevance.
    """
    results = []

    # Filter by type
    if context_type:
        results = query_by_type(context_type)
    else:
        results = query_all()

    # Apply filters
    if task_id:
        results = [r for r in results if r.get('task_id') == task_id]

    if agent_id:
        results = [r for r in results if involves_agent(r, agent_id)]

    if keywords:
        results = rank_by_keyword_relevance(results, keywords)

    if time_range:
        start, end = time_range
        results = [r for r in results if start <= r['_metadata']['stored_at'] <= end]

    return sort_by_relevance(results)
```

### Relate Context

```python
def relate_context(context_id_1: str, context_id_2: str, relationship: str):
    """
    Create a relationship between two context objects.

    Relationships:
    - 'depends_on': First depends on second
    - 'supersedes': First replaces second
    - 'related_to': General association
    - 'derived_from': First was created from second
    """
    relationship_record = {
        'source': context_id_1,
        'target': context_id_2,
        'type': relationship,
        'created_at': now(),
        'created_by': current_agent()
    }

    store_relationship(relationship_record)
    update_graph_index(context_id_1, context_id_2, relationship)
```

### Expire Context

```python
def expire_context(context_id: str, reason: str):
    """
    Mark context as expired (soft delete).

    Expired context remains queryable but is excluded from default queries.
    """
    context = get_context(context_id)
    context['_metadata']['expired'] = True
    context['_metadata']['expired_at'] = now()
    context['_metadata']['expiration_reason'] = reason

    update_context(context_id, context)

    # Archive if retention policy allows
    if should_archive(context):
        archive_context(context_id)
```

---

## Context Retrieval Patterns

### Pattern 1: Task Continuation
When agent picks up existing task:

```yaml
retrieval_query:
  purpose: "Continue work on task"
  filters:
    task_id: "TASK-DEV-20240115-001"
  retrieve:
    - Task context (current state)
    - All decisions related to task
    - All artifacts produced
    - Handoff packages received
  present_to_agent:
    - Summary of progress
    - Key decisions made
    - Open questions
    - Next steps
```

### Pattern 2: Related Work Discovery
Finding relevant prior work:

```yaml
retrieval_query:
  purpose: "Find similar implementations"
  filters:
    keywords: ["authentication", "oauth", "jwt"]
    time_range: ["2023-01-01", "now"]
    context_type: "artifact"
  retrieve:
    - Similar code artifacts
    - Related design decisions
    - Lessons learned
  present_to_agent:
    - Reusable patterns
    - Past issues encountered
    - Recommended approaches
```

### Pattern 3: Cross-Task Dependencies
Understanding task relationships:

```yaml
retrieval_query:
  purpose: "Identify dependencies"
  filters:
    relationship_type: ["depends_on", "blocked_by"]
    root_task: "TASK-DEV-20240115-001"
  retrieve:
    - Upstream tasks
    - Downstream tasks
    - Blocking issues
  present_to_agent:
    - Dependency graph
    - Blocking items
    - Impact analysis
```

### Pattern 4: Agent History
What has an agent worked on:

```yaml
retrieval_query:
  purpose: "Agent work history"
  filters:
    agent_id: "DEV-002"
    time_range: ["7_days_ago", "now"]
  retrieve:
    - Tasks owned
    - Decisions made
    - Artifacts created
    - Handoffs sent/received
  present_to_agent:
    - Recent activity summary
    - In-progress work
    - Pending handoffs
```

---

## Context Summarization

For large context sets, provide summaries:

```yaml
summarization_rules:
  task_context:
    include_always:
      - task_id
      - title
      - status
      - current_owner
      - completion_percentage
    include_if_relevant:
      - original_request
      - blocking_tasks
      - recent_updates
    truncate:
      - detailed_notes (first 500 chars)
      - conversation_history (last 5 messages)

  decision_context:
    include_always:
      - decision title
      - made_by
      - approval_status
    include_if_relevant:
      - rationale (if agent asks)
      - alternatives (if reconsidering)
    omit:
      - full discussion history

  artifact_context:
    include_always:
      - artifact type
      - path
      - validation status
    include_if_relevant:
      - dependencies
      - version history
    omit:
      - full content (reference path instead)
```

---

## Context Lifecycle

```
┌──────────────────────────────────────────────────────────────────┐
│                    CONTEXT LIFECYCLE                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  CREATE ──▶ ACTIVE ──▶ STALE ──▶ EXPIRED ──▶ ARCHIVED           │
│     │         │          │          │            │               │
│     │         │          │          │            │               │
│     ▼         ▼          ▼          ▼            ▼               │
│  Stored    Queryable   Flagged   Soft-deleted  Compressed       │
│  Indexed   Updated     Warning   Hidden        Cold storage     │
│            Referenced  Reviewable Recoverable  Audit only       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

Lifecycle Transitions:
- CREATE → ACTIVE: On store
- ACTIVE → STALE: No updates in 7 days
- STALE → ACTIVE: On any update
- STALE → EXPIRED: No updates in 30 days
- EXPIRED → ARCHIVED: Per retention policy
```

---

## Integration with Agents

### Agent Context Package
What agents receive when starting work:

```json
{
  "agent_context_package": {
    "agent_id": "DEV-002",
    "task_assignment": {
      "task_id": "TASK-DEV-20240115-001",
      "assigned_at": "2024-01-15T14:30:00Z"
    },

    "task_context": {
      "summary": "Implement OAuth 2.0 authentication service",
      "current_status": "Design complete, implementation 40% done",
      "your_role": "Complete backend implementation"
    },

    "relevant_decisions": [
      {
        "id": "DEC-20240115-001",
        "summary": "Using JWT for session tokens",
        "implications_for_you": "Implement JWT signing and verification"
      }
    ],

    "existing_artifacts": [
      {
        "type": "design",
        "path": "/docs/auth-design.md",
        "relevance": "Implementation specification"
      },
      {
        "type": "code",
        "path": "/src/services/auth/",
        "relevance": "Partial implementation to continue"
      }
    ],

    "handoffs_received": [
      {
        "from": "DEV-001",
        "summary": "Architecture complete, ready for implementation",
        "key_points": ["Use existing user table", "Follow API conventions"]
      }
    ],

    "expectations": {
      "deliverables": ["Working auth endpoints", "Unit tests", "API docs"],
      "handoff_to": "DEV-004 for code review",
      "deadline": "2024-01-17T18:00:00Z"
    }
  }
}
```

### Agent Context Updates
What agents report back:

```json
{
  "agent_context_update": {
    "agent_id": "DEV-002",
    "task_id": "TASK-DEV-20240115-001",
    "timestamp": "2024-01-15T17:00:00Z",

    "progress_update": {
      "completion_percentage": 75,
      "milestone_completed": "core_auth_logic",
      "work_remaining": ["refresh_tokens", "rate_limiting", "tests"]
    },

    "decisions_made": [
      {
        "decision": "Using bcrypt for password hashing",
        "rationale": "Industry standard, configurable work factor",
        "needs_approval": false
      }
    ],

    "artifacts_created": [
      {
        "type": "code",
        "path": "/src/services/auth/oauth.py",
        "description": "OAuth provider integration"
      }
    ],

    "blockers": [],

    "questions_for_others": [
      {
        "question": "Token expiry time preference?",
        "directed_to": "SEC-001",
        "urgency": "medium"
      }
    ]
  }
}
```

---

## Retention Policies

| Context Type | Active Period | Stale Period | Archive After | Delete After |
|--------------|---------------|--------------|---------------|--------------|
| Task | Until closed + 30 days | 30 days | 1 year | 7 years |
| Decision | Permanent | N/A | Never | Never |
| Artifact | Until superseded | 90 days | 1 year | Policy-based |
| Session | Until ended + 7 days | 7 days | 30 days | 1 year |

---

## Security Considerations

```yaml
context_security:
  access_control:
    - Agents can only access context for their authorized tasks
    - Security classification inherited from associated task
    - Cross-team context requires explicit sharing

  sensitive_data:
    - Credentials never stored in context
    - PII flagged and encrypted
    - Security findings restricted access

  audit:
    - All context access logged
    - Modifications tracked with agent ID
    - Export requests require approval
```
