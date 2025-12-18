# HIVEMIND Message Bus

> Internal agent-to-agent communication. ALL INVISIBLE TO USER.

---

## Message Types

### REQUEST

Agent asks another agent for work.

```json
{
  "type": "REQUEST",
  "id": "msg_[unique]",
  "from": "DEV-002",
  "to": "INF-004",
  "priority": "P2",
  "content": {
    "action": "review_schema",
    "payload": {...}
  },
  "expects_response": true
}
```

### RESPONSE

Agent returns results.

```json
{
  "type": "RESPONSE",
  "id": "msg_[unique]",
  "reply_to": "msg_[original]",
  "from": "INF-004",
  "to": "DEV-002",
  "status": "success|partial|failed",
  "content": {
    "results": {...}
  }
}
```

### BROADCAST

Agent announces to multiple agents.

```json
{
  "type": "BROADCAST",
  "id": "msg_[unique]",
  "from": "SEC-006",
  "to": ["*"] | ["DEV-*"] | ["DEV-001", "INF-001"],
  "priority": "P0",
  "content": {
    "alert": "Security incident",
    "action": "Pause deployments"
  }
}
```

### CONSULTATION

Non-blocking advisory request.

```json
{
  "type": "CONSULTATION",
  "id": "msg_[unique]",
  "from": "DEV-001",
  "to": ["SEC-001", "INF-001", "QA-001"],
  "content": {
    "question": "Architecture approach?",
    "options": ["A", "B", "C"],
    "context": "..."
  },
  "collect": "all|first|majority"
}
```

---

## Routing Rules

### Priority Handling

| Priority | Behavior |
|----------|----------|
| P0 | Immediate, interrupts current work |
| P1 | Next in queue, within 5 min |
| P2 | Standard FIFO |
| P3 | Low priority, may batch |

### Addressing

```
Direct:     "to": "DEV-002"
Team:       "to": "DEV-*"
All:        "to": "*"
Select:     "to": ["DEV-001", "SEC-001"]
Leads:      "to": "LEADS" → [DEV-001, SEC-001, INF-001, QA-001]
```

### Cross-Team Rules

Messages crossing teams automatically CC team leads:
- DEV → SEC: CC SEC-001
- SEC → INF: CC INF-001
- Any → All: CC all leads

---

## Communication Patterns

### Pattern 1: Direct Request

```
DEV-002 ──REQUEST──> INF-004
         <──RESPONSE──
```

### Pattern 2: Multi-Agent Consultation

```
DEV-001 ──CONSULTATION──> SEC-001
     │                        │
     ├──CONSULTATION──> INF-001
     │                        │
     └──CONSULTATION──> QA-001
              │
              ▼
      [Aggregate responses]
```

### Pattern 3: Chain

```
DEV-001 → DEV-002 → DEV-004 → QA-002
   │         │         │         │
   └─────────┴─────────┴─────────┘
          Context flows forward
```

### Pattern 4: Fan-Out/Fan-In

```
           ┌──> Agent B ──┐
Agent A ───┼──> Agent C ──┼──> Agent A
           └──> Agent D ──┘
```

### Pattern 5: Broadcast

```
SEC-006 ──BROADCAST──> All agents
```

---

## Queue Management

Each agent has a priority queue:

```
Agent Queue:
├── P0: [] (immediate)
├── P1: [] (high)
├── P2: [msg1, msg2] (standard)
└── P3: [] (low)
```

Processing order: P0 → P1 → P2 → P3

---

## Error Handling

```
On delivery failure:
  1. Retry 3 times with backoff
  2. If still failing:
     - Notify sender
     - Escalate to team lead
     - Log to events

On timeout:
  1. Mark message TIMEOUT
  2. Notify sender
  3. Sender decides: retry, escalate, fail
```

---

## SILENT OPERATION

**CRITICAL**: No message bus activity ever appears in user output.

Never say:
- "Sending message to..."
- "Received response from..."
- "Consulting with..."
- "Broadcasting to..."

All communication is internal plumbing only.
