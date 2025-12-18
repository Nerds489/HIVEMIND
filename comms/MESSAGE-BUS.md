# HIVEMIND Message Bus

> Internal communication infrastructure for agent-to-agent messaging.
> **ALL COMMUNICATION IS INVISIBLE TO USER** - See runtime/OUTPUT-FILTER.md

---

## Overview

The Message Bus enables any agent to communicate with any other agent through structured message passing. All communication is internal and never exposed to the user.

---

## Message Types

### 1. REQUEST

Agent requests work from another agent.

```json
{
  "type": "REQUEST",
  "id": "msg_a1b2c3d4e5f6",
  "timestamp": "2025-12-18T10:00:00Z",
  "from": {
    "agent_id": "DEV-002",
    "team": "development"
  },
  "to": {
    "agent_id": "INF-004",
    "team": "infrastructure"
  },
  "priority": "P2",
  "content": {
    "action": "review_schema",
    "payload": {
      "schema_path": "/db/schemas/users.sql",
      "concerns": ["performance", "indexing"]
    }
  },
  "response_required": true,
  "timeout_ms": 30000
}
```

### 2. RESPONSE

Agent returns results from a request.

```json
{
  "type": "RESPONSE",
  "id": "msg_f6e5d4c3b2a1",
  "in_reply_to": "msg_a1b2c3d4e5f6",
  "timestamp": "2025-12-18T10:00:15Z",
  "from": {
    "agent_id": "INF-004",
    "team": "infrastructure"
  },
  "to": {
    "agent_id": "DEV-002",
    "team": "development"
  },
  "status": "success",
  "content": {
    "findings": [
      {"type": "recommendation", "detail": "Add index on user_id"},
      {"type": "approval", "detail": "Schema structure is sound"}
    ]
  }
}
```

### 3. BROADCAST

Agent sends to multiple recipients.

```json
{
  "type": "BROADCAST",
  "id": "msg_broadcast001",
  "timestamp": "2025-12-18T10:00:00Z",
  "from": {
    "agent_id": "SEC-006",
    "team": "security"
  },
  "to": {
    "scope": "all_teams",
    "agents": ["*"]
  },
  "priority": "P0",
  "content": {
    "alert": "Security incident detected",
    "action_required": "Pause all deployments"
  }
}
```

### 4. CONSULTATION

Agent seeks advisory input (non-blocking).

```json
{
  "type": "CONSULTATION",
  "id": "msg_consult001",
  "timestamp": "2025-12-18T10:00:00Z",
  "from": {
    "agent_id": "DEV-001",
    "team": "development"
  },
  "to": {
    "agents": ["SEC-001", "INF-001", "QA-001"]
  },
  "priority": "P3",
  "content": {
    "question": "Architecture approach for new auth system",
    "options": ["OAuth2", "JWT", "Session-based"],
    "context": "High-security financial application"
  },
  "response_required": false,
  "collect_until": "first_response"
}
```

### 5. HANDOFF

Agent transfers task ownership.

```json
{
  "type": "HANDOFF",
  "id": "msg_handoff001",
  "timestamp": "2025-12-18T10:00:00Z",
  "from": {
    "agent_id": "DEV-002",
    "team": "development"
  },
  "to": {
    "agent_id": "DEV-004",
    "team": "development"
  },
  "content": {
    "task_id": "TASK-001",
    "summary": "Implementation complete, ready for review",
    "artifacts": ["/src/auth/", "/tests/auth/"],
    "context_package": "See protocols/handoffs.md schema"
  }
}
```

---

## Routing Rules

### Priority-Based Routing

| Priority | Behavior |
|----------|----------|
| P0 | Immediate delivery, interrupt current work |
| P1 | High priority queue, process within 5 min |
| P2 | Standard queue, FIFO processing |
| P3 | Low priority, batch processing OK |
| P4 | Best effort, may defer |

### Agent Addressing

```
Direct:     agent_id: "DEV-002"
Team:       team: "security", agents: ["*"]
All:        scope: "all", agents: ["*"]
Selective:  agents: ["DEV-001", "SEC-001", "INF-001"]
Role:       role: "team_lead"  → DEV-001, SEC-001, INF-001, QA-001
```

### Cross-Team Rules

Messages crossing team boundaries:
1. CC team leads automatically
2. Security-related messages always CC SEC-001
3. Infrastructure changes always CC INF-001

---

## Message Patterns

### Pattern 1: Single Agent Request

```
DEV-002 ──REQUEST──> INF-004
DEV-002 <──RESPONSE── INF-004
```

### Pattern 2: Multi-Agent Consultation

```
DEV-001 ──CONSULTATION──> SEC-001
     │                       │
     ├──CONSULTATION──> INF-001
     │                       │
     └──CONSULTATION──> QA-001
             │
             ▼
     [Collect responses]
             │
             ▼
     [Synthesize decision]
```

### Pattern 3: Chain Communication

```
DEV-001 ──HANDOFF──> DEV-002 ──HANDOFF──> DEV-004 ──HANDOFF──> QA-002
  │                     │                     │                   │
  └─────────────────────┴─────────────────────┴───────────────────┘
                              Context flows forward
```

### Pattern 4: Broadcast Alert

```
                    ┌──> DEV-* (all dev agents)
                    │
SEC-006 ──BROADCAST─┼──> SEC-* (all sec agents)
                    │
                    ├──> INF-* (all infra agents)
                    │
                    └──> QA-* (all qa agents)
```

### Pattern 5: Fan-Out/Fan-In

```
              ┌──REQUEST──> Agent B ──┐
              │                       │
Agent A ──────┼──REQUEST──> Agent C ──┼──> Agent A [aggregates]
              │                       │
              └──REQUEST──> Agent D ──┘
```

---

## Queue Management

### Message Queue Structure

```json
{
  "queue_id": "queue_dev002",
  "agent_id": "DEV-002",
  "messages": {
    "p0": [],
    "p1": [],
    "p2": [
      {"id": "msg_001", "from": "INF-004", "age_ms": 5000}
    ],
    "p3": [],
    "p4": []
  },
  "processing": null,
  "stats": {
    "received_total": 150,
    "processed_total": 148,
    "avg_response_ms": 2500
  }
}
```

### Processing Order

1. All P0 messages (FIFO within priority)
2. All P1 messages
3. P2 messages (may interleave with new P0/P1)
4. P3/P4 during idle time

### Timeout Handling

```
On timeout:
1. Mark message as TIMEOUT
2. Notify sender with timeout error
3. Sender decides: retry, escalate, or fail
```

---

## Error Handling

### Delivery Failures

```json
{
  "type": "ERROR",
  "original_message_id": "msg_001",
  "error_code": "AGENT_UNAVAILABLE",
  "error_message": "Target agent INF-004 not responding",
  "retry_count": 3,
  "action_taken": "escalated_to_team_lead"
}
```

### Error Codes

| Code | Meaning | Auto-Action |
|------|---------|-------------|
| AGENT_UNAVAILABLE | Target agent not responding | Retry 3x, then escalate |
| TIMEOUT | Response not received in time | Notify sender |
| INVALID_MESSAGE | Message malformed | Reject with details |
| QUEUE_FULL | Target queue at capacity | Wait and retry |
| PERMISSION_DENIED | Agent lacks authorization | Reject, notify sender |

---

## Security

### Message Validation

All messages are validated:
1. Sender ID is valid agent
2. Recipient exists
3. Message structure is correct
4. Priority is appropriate for sender
5. Content does not violate policies

### Audit Trail

All messages are logged:
```json
{
  "log_id": "log_001",
  "message_id": "msg_001",
  "timestamp": "2025-12-18T10:00:00Z",
  "from": "DEV-002",
  "to": "INF-004",
  "type": "REQUEST",
  "status": "delivered",
  "response_id": "msg_002"
}
```

---

## Integration

### With Memory System

Messages can trigger memory operations:
- REQUEST completion → create episodic memory
- CONSULTATION results → create semantic memory
- ERROR patterns → create procedural memory

### With Spawn Protocol

Messages can trigger agent spawning:
- If target agent is DORMANT → spawn before delivery
- See `./SPAWN-PROTOCOL.md`

### With Output Filter

**CRITICAL**: No message content ever reaches user output.
All inter-agent communication is internal only.
See `../runtime/OUTPUT-FILTER.md`
