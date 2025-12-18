# HIVEMIND Handoff Protocol

## Overview

This protocol defines the complete procedure for transferring work between agents, ensuring context is preserved and quality is maintained across handoffs.

---

## Pre-Handoff Phase

### Completion Verification Checklist

Before initiating a handoff, the sending agent MUST verify:

```
WORK COMPLETION
[ ] All assigned tasks completed or explicitly handed off
[ ] No work-in-progress that could be lost
[ ] All branches committed and pushed
[ ] All changes saved and persisted

QUALITY VERIFICATION
[ ] Work meets acceptance criteria
[ ] Self-review completed
[ ] No known critical issues
[ ] Code compiles/tests pass (if applicable)

DOCUMENTATION
[ ] Work documented appropriately
[ ] Decisions documented with rationale
[ ] Open questions clearly listed
[ ] Assumptions explicitly stated

ARTIFACTS
[ ] All artifacts in correct locations
[ ] Artifacts properly named per conventions
[ ] Artifacts accessible to receiving agent
[ ] No temporary files or debug code
```

### Artifact Preparation

All artifacts must be:
1. **Located** in standard paths: `/artifacts/[team]/[date]/[task_id]/`
2. **Named** per convention: `[task_id]-[type]-[version].[ext]`
3. **Validated** where applicable (tests pass, linting clean)
4. **Documented** with README if complex

### Context Summarization

Create a summary that answers:
- What was the goal?
- What was accomplished?
- What decisions were made and why?
- What remains to be done?
- What should the next agent know?

### Dependency Documentation

List all dependencies:
- External systems required
- Data sources needed
- Credentials or access required
- Other tasks this work depends on
- Tasks that depend on this work

---

## Handoff Package

### Complete Schema

```json
{
  "handoff_package": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "version": "1.0",
    "created_at": "2024-01-15T14:30:00Z",

    "source": {
      "agent_id": "DEV-002",
      "agent_name": "Backend Developer",
      "team": "Development",
      "task_id": "TASK-DEV-20240115-001",
      "task_title": "Implement User Profile API"
    },

    "destination": {
      "agent_id": "DEV-004",
      "agent_name": "Code Reviewer",
      "team": "Development",
      "expected_action": "Code review and approval"
    },

    "context": {
      "summary": "Implemented REST API endpoints for user profile CRUD operations. All 5 endpoints complete with unit tests. Ready for code review.",

      "detailed_notes": "Implementation follows FastAPI patterns established in existing codebase. Used SQLAlchemy ORM for database operations. Added input validation using Pydantic models. Implemented proper error handling with custom exception classes.",

      "background": {
        "original_request": "Create user profile management API per design spec ADR-042",
        "business_context": "Part of user management system overhaul",
        "timeline_context": "Sprint 23, due Jan 20"
      },

      "decisions_made": [
        {
          "decision": "Used async SQLAlchemy for database operations",
          "rationale": "Consistency with existing async API patterns",
          "alternatives_considered": ["sync SQLAlchemy", "raw SQL"],
          "approved_by": "DEV-001"
        },
        {
          "decision": "Implemented soft delete for user profiles",
          "rationale": "Compliance requirement for data retention",
          "alternatives_considered": ["hard delete"],
          "approved_by": "SEC-005"
        }
      ],

      "assumptions": [
        {
          "assumption": "Database schema from INF-004 is finalized",
          "risk_if_wrong": "May need to update model definitions",
          "verification_status": "Confirmed with INF-004"
        },
        {
          "assumption": "Authentication middleware handles token validation",
          "risk_if_wrong": "Would need to add auth checks to endpoints",
          "verification_status": "Confirmed with DEV-001"
        }
      ],

      "open_questions": [
        {
          "question": "Should profile updates trigger notification to user?",
          "context": "Not specified in requirements",
          "suggested_resolution": "Clarify with product owner",
          "blocking": false
        }
      ],

      "blockers_encountered": [
        {
          "blocker": "Database connection pool exhaustion under load",
          "resolution": "Increased pool size, added connection timeout",
          "time_lost": "2 hours"
        }
      ],

      "blockers_current": []
    },

    "artifacts": [
      {
        "artifact_id": "ART-001",
        "name": "API Implementation",
        "type": "code",
        "path": "/src/api/users/",
        "description": "FastAPI router and endpoint implementations",
        "validation": {
          "status": "passed",
          "tests_run": 45,
          "tests_passed": 45,
          "coverage": "87%"
        }
      },
      {
        "artifact_id": "ART-002",
        "name": "Unit Tests",
        "type": "code",
        "path": "/tests/api/users/",
        "description": "pytest unit tests for all endpoints",
        "validation": {
          "status": "passed",
          "tests_run": 45,
          "tests_passed": 45
        }
      },
      {
        "artifact_id": "ART-003",
        "name": "API Documentation",
        "type": "document",
        "path": "/docs/api/users.md",
        "description": "OpenAPI spec and usage examples",
        "validation": {
          "status": "not_applicable"
        }
      },
      {
        "artifact_id": "ART-004",
        "name": "Database Migrations",
        "type": "config",
        "path": "/migrations/versions/20240115_user_profile.py",
        "description": "Alembic migration for user profile table",
        "validation": {
          "status": "passed",
          "notes": "Tested upgrade and downgrade"
        }
      }
    ],

    "next_steps": {
      "required_actions": [
        {
          "action": "Review code for security vulnerabilities",
          "priority": "high",
          "guidance": "Focus on input validation and SQL injection prevention"
        },
        {
          "action": "Review code for maintainability",
          "priority": "medium",
          "guidance": "Check adherence to existing patterns"
        },
        {
          "action": "Approve or request changes",
          "priority": "high",
          "guidance": "Block merge until all critical issues resolved"
        }
      ],

      "suggested_actions": [
        {
          "action": "Consider adding integration tests",
          "rationale": "Would improve confidence in database operations"
        }
      ],

      "success_criteria": [
        "No critical or high security findings",
        "Code follows established patterns",
        "Adequate test coverage maintained",
        "Documentation is complete and accurate"
      ],

      "handoff_after_completion": {
        "next_agent": "QA-004",
        "next_action": "Security scan",
        "conditions": "Only if code review approved"
      }
    },

    "metadata": {
      "priority": "P2",
      "deadline": "2024-01-16T18:00:00Z",
      "deadline_type": "soft",
      "security_classification": "internal",
      "compliance_relevant": true,
      "audit_trail_required": true
    },

    "handoff_checklist": {
      "sender_completed": [
        "✓ Implementation complete",
        "✓ Unit tests written and passing",
        "✓ Documentation updated",
        "✓ Self-review completed",
        "✓ PR created: #1234"
      ],
      "receiver_required": [
        "☐ Code review completed",
        "☐ Security review completed",
        "☐ Approve or request changes",
        "☐ Document review findings"
      ]
    }
  }
}
```

---

## Acceptance Protocol

### Receiving Agent Steps

When a handoff package arrives:

#### Step 1: Acknowledge Receipt
```json
{
  "acknowledgment": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "received_by": "DEV-004",
    "received_at": "2024-01-15T14:35:00Z",
    "status": "acknowledged"
  }
}
```

#### Step 2: Verify Package Completeness
Check that all required elements are present:
- [ ] Context summary is clear
- [ ] All listed artifacts exist and are accessible
- [ ] Success criteria are defined
- [ ] No critical information missing

#### Step 3: Verify Artifacts
For each artifact:
- [ ] Artifact exists at specified path
- [ ] Artifact is readable/accessible
- [ ] Artifact matches description
- [ ] Validation status is acceptable

#### Step 4: Confirm or Reject

**If Acceptable:**
```json
{
  "acceptance": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "accepted_by": "DEV-004",
    "accepted_at": "2024-01-15T14:40:00Z",
    "status": "accepted",
    "estimated_completion": "2024-01-15T17:00:00Z",
    "notes": "All artifacts verified. Beginning review."
  }
}
```

**If Incomplete/Unclear:**
```json
{
  "rejection": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "rejected_by": "DEV-004",
    "rejected_at": "2024-01-15T14:40:00Z",
    "status": "rejected",
    "reason": "incomplete",
    "issues": [
      {
        "issue": "Missing unit tests for DELETE endpoint",
        "required_action": "Add tests for user deletion"
      },
      {
        "issue": "Artifact ART-003 not found at specified path",
        "required_action": "Verify path or provide correct location"
      }
    ],
    "requested_resubmission_by": "2024-01-15T16:00:00Z"
  }
}
```

### Partial Acceptance

For large handoffs, partial acceptance is allowed:
```json
{
  "partial_acceptance": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "accepted_by": "DEV-004",
    "accepted_at": "2024-01-15T14:40:00Z",
    "status": "partial",
    "accepted_items": ["ART-001", "ART-002", "ART-004"],
    "pending_items": ["ART-003"],
    "notes": "Beginning review of code. API docs path issue reported separately."
  }
}
```

---

## Post-Handoff Phase

### Progress Visibility

The receiving agent MUST provide visibility:

#### Initial Status (within 1 hour of acceptance)
```json
{
  "status_update": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "from": "DEV-004",
    "timestamp": "2024-01-15T15:30:00Z",
    "progress": "25%",
    "current_activity": "Reviewing endpoint implementations",
    "findings_so_far": 2,
    "blockers": [],
    "estimated_completion": "2024-01-15T17:00:00Z"
  }
}
```

#### Check-In Intervals
- **P0/P1:** Every 30 minutes
- **P2:** Every 2 hours
- **P3/P4:** Daily

### Completion Notification

When work is complete:
```json
{
  "completion_notification": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "completed_by": "DEV-004",
    "completed_at": "2024-01-15T16:45:00Z",
    "status": "completed",

    "outcome": {
      "result": "approved_with_comments",
      "summary": "Code review passed. Minor improvements suggested."
    },

    "findings": [
      {
        "severity": "minor",
        "location": "/src/api/users/router.py:45",
        "issue": "Consider using more descriptive variable name",
        "suggestion": "Rename 'x' to 'user_count'"
      }
    ],

    "artifacts_produced": [
      {
        "name": "Code Review Report",
        "path": "/artifacts/reviews/PR-1234-review.md"
      }
    ],

    "next_handoff": {
      "destination": "QA-004",
      "handoff_id": "HO-DEV004-QA004-20240115-164500",
      "action": "Security scan"
    }
  }
}
```

### Feedback Loop

Source agent receives feedback:
```json
{
  "feedback": {
    "handoff_id": "HO-DEV002-DEV004-20240115-143000",
    "from": "DEV-004",
    "to": "DEV-002",
    "timestamp": "2024-01-15T16:50:00Z",

    "handoff_quality": {
      "rating": "good",
      "context_clarity": "excellent",
      "artifact_quality": "good",
      "documentation": "good"
    },

    "suggestions": [
      "Include PR link in handoff package for faster access",
      "Consider adding performance benchmarks for API endpoints"
    ],

    "positive_notes": [
      "Excellent decision documentation",
      "Complete test coverage made review efficient"
    ]
  }
}
```

---

## Handoff Patterns

### Sequential Handoff Chain
```
Agent A → Agent B → Agent C → Agent D

Each agent:
1. Receives handoff from predecessor
2. Does their work
3. Creates new handoff to successor
4. Notifies predecessor of completion
```

### Parallel Handoff Split
```
           ┌→ Agent B ─┐
Agent A ───┼→ Agent C ─┼→ Agent E (aggregates)
           └→ Agent D ─┘

Agent A:
1. Creates 3 handoff packages (one per recipient)
2. Each package contains agent-specific subset
3. Includes information about parallel work

Agent E:
1. Receives from B, C, D (in any order)
2. Waits for all before proceeding
3. Aggregates results
```

### Conditional Handoff
```
Agent A → Agent B
              │
              ├── If approved → Agent C
              └── If rejected → Agent A (rework)
```

---

## Handoff Anti-Patterns

### DON'T: Incomplete Handoffs
```
❌ "Here's the code, you figure it out"
✓ Complete context package with all required fields
```

### DON'T: Assumption Dumping
```
❌ "Should work, I tested it on my machine"
✓ Document environment, list dependencies, include test results
```

### DON'T: Silent Handoffs
```
❌ Dropping files in a shared location without notification
✓ Formal handoff package with explicit acceptance
```

### DON'T: Context-Free Artifacts
```
❌ Just code files with no explanation
✓ README, decision log, usage examples included
```

### DON'T: Handoff Abandonment
```
❌ Handing off and disappearing
✓ Remain available for questions during transition period
```

---

## Handoff Metrics

Track these for continuous improvement:

| Metric | Target | Red Flag |
|--------|--------|----------|
| Acceptance Rate | > 95% | < 85% |
| Rejection Rate | < 5% | > 10% |
| Avg Acceptance Time | < 30 min | > 2 hours |
| Rework Rate | < 10% | > 20% |
| Context Clarity Score | > 4/5 | < 3/5 |
| Missing Artifact Rate | < 2% | > 5% |

---

## Memory Handoff Requirements

### Context Package Structure

Every handoff MUST include a memory context package:

```json
{
  "memory_context": {
    "loaded_memories": ["mem_xxx", "mem_yyy"],
    "working_memory_snapshot": {
      "current_task": "task description",
      "progress": "what was done",
      "pending": ["items remaining"]
    },
    "memories_created_this_task": ["mem_zzz"],
    "memories_updated_this_task": ["mem_aaa"],
    "recommended_memories_for_next": ["mem_bbb", "mem_ccc"]
  }
}
```

### Sending Agent MUST

1. **Package Working Memory**
   - Export current working memory state
   - Include all notes and context
   - List pending items clearly

2. **List Memory Operations**
   - All memories loaded during task
   - All memories created during task
   - All memories updated during task

3. **Recommend Context**
   - Identify memories the receiving agent will need
   - Include rationale for recommendations
   - Prioritize by relevance

4. **Update Session State**
   - Record handoff in `./memory/sessions/current.json`
   - Update `agent_context.last_agent`
   - Append to `agent_context.agent_history`

### Receiving Agent MUST

1. **Load Handed-Off Memories**
   ```
   FOR EACH id IN loaded_memories:
     Load memory content
     Add to agent context
   
   FOR EACH id IN recommended_memories_for_next:
     Load memory content
     Add to agent context
   ```

2. **Inherit Working Memory**
   - Import `working_memory_snapshot` as starting context
   - Acknowledge pending items
   - Continue from current progress

3. **Acknowledge Handoff**
   - Confirm memory context received
   - Note any missing or unclear items
   - Request clarification if needed

4. **Load Agent-Specific Memories**
   - Load from `./memory/agents/[AGENT-ID]/`
   - Include working-memory.json
   - Merge with handoff context

### Handoff Memory Flow

```
[Sending Agent]
      |
      v
Package working memory ─────────────────┐
      |                                 |
      v                                 v
List memories used ──────> memory_context JSON
      |                                 |
      v                                 v
Recommend next context ─────────────────┤
      |                                 |
      v                                 v
Update session state                    |
      |                                 |
      └─────────> HANDOFF ──────────────┘
                    |
                    v
            [Receiving Agent]
                    |
                    v
            Load all handoff memories
                    |
                    v
            Import working memory
                    |
                    v
            Load agent memories
                    |
                    v
            Acknowledge and continue
```

### Handoff Quality Gates

Before completing handoff, verify:

| Check | Requirement |
|-------|-------------|
| Memory package complete | All fields populated |
| Memories accessible | All referenced IDs exist |
| Working memory exported | Snapshot is current |
| Recommendations provided | At least 1 recommended memory |
| Session state updated | current.json reflects handoff |
