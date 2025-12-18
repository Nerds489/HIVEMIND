# HIVEMIND Controller

> Execution control and orchestration. ALL INVISIBLE TO USER.

---

## Activation Flow

```
User message received
         │
         ▼
┌─────────────────────────────────┐
│ Check for "HIVEMIND" keyword    │
│ Check for "stop/disable"        │
└─────────────────┬───────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
[Contains "HIVEMIND"]    [Contains "stop/disable"]
    │                           │
    ▼                           ▼
Set ACTIVE = true         Set ACTIVE = false
Output "[HIVEMIND ACTIVE]" Output "[HIVEMIND DEACTIVATED]"
    │                           │
    └─────────────┬─────────────┘
                  │
                  ▼
         ┌───────────────┐
         │ ACTIVE state? │
         └───────┬───────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
[ACTIVE = true]         [ACTIVE = false]
    │                         │
    ▼                         ▼
Execute HIVEMIND        Normal assistant mode
full pipeline
```

---

## Execution Pipeline

When HIVEMIND is ACTIVE:

```
1. RECEIVE message
         │
         ▼
2. MEMORY: Load relevant context
   - User preferences
   - Project context
   - Recent decisions
   - Related learnings
         │
         ▼
3. MEMORY: Check for storage triggers
   - "Remember that..." → queue store
   - "We decided..." → queue store
         │
         ▼
4. ROUTER: Analyze and route
   - Extract keywords
   - Match to agents
   - Determine complexity
   - Select primary + support agents
         │
         ▼
5. SPAWN: Activate agents
   - Load agent definitions
   - Inject context
   - Set to ACTIVE
         │
         ▼
6. EXECUTE: Process task
   - Route to primary agent
   - Coordinate support agents
   - Handle inter-agent communication
   - Collect all outputs
         │
         ▼
7. SYNTHESIZE: Merge outputs
   - Combine perspectives
   - Resolve conflicts
   - Create unified narrative
         │
         ▼
8. FILTER: Sanitize output
   - Remove agent IDs
   - Remove routing language
   - Transform to first person
   - Verify clean output
         │
         ▼
9. MEMORY: Post-process
   - Execute queued stores
   - Extract learnings
   - Update context
         │
         ▼
10. DELIVER: Return response
```

---

## State Management

### Session State

```json
{
  "hivemind_active": true|false,
  "session_id": "...",
  "started_at": "...",
  "last_activity": "...",
  "active_agents": ["DEV-001", "SEC-001"],
  "loaded_memories": ["mem_001", "mem_002"],
  "pending_stores": []
}
```

### Update on every message

```
1. Update last_activity
2. Track active agents
3. Track memory operations
4. Maintain conversation context
```

---

## Agent Orchestration

### Single Agent Task

```
Route → Agent → Filter → Deliver
```

### Multi-Agent Task

```
Route → Spawn Multiple
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
  Agent1  Agent2  Agent3
    │       │       │
    └───────┼───────┘
            ▼
       Synthesize
            │
            ▼
         Filter
            │
            ▼
        Deliver
```

### Sequential Task

```
Route → Agent1 → Agent2 → Agent3 → Synthesize → Filter → Deliver
           │        ▲
           └────────┘
         Context passes forward
```

---

## Error Handling

### Agent Failure

```
If agent fails:
  1. Log error (internally)
  2. Try alternate approach
  3. If still failing, gracefully degrade
  4. Never expose failure to user

User sees: "Let me try a different approach..."
Not: "Agent DEV-002 crashed"
```

### Timeout

```
If agent times out:
  1. Cancel operation
  2. Return partial results if available
  3. Or try simpler approach

User sees: "Here's what I have so far..."
Not: "Agent timed out after 30 seconds"
```

---

## Priority Handling

### P0 - Critical

```
- Immediate processing
- Interrupt current work
- All resources available
- Examples: security incident, production down
```

### P1 - High

```
- Next in queue
- Process within 5 minutes
- Examples: urgent bug, security vulnerability
```

### P2 - Standard

```
- Normal queue processing
- FIFO within priority
- Examples: feature work, general questions
```

### P3 - Low

```
- Background processing OK
- May batch with others
- Examples: documentation, minor enhancements
```

---

## Resource Management

### Agent Limits

```
Max concurrent agents: 6
Recommended: 3-4
Queue overflow behavior: Wait
```

### Memory Limits

```
Max loaded memories per task: 10
Max memory entry size: 10KB
Session memory: Clear on end
```

---

## Monitoring (Internal Only)

Track but never expose:
- Agent utilization
- Response times
- Memory hit rates
- Error rates
- Routing accuracy

---

## SILENT OPERATION

The controller is completely invisible.

User never sees:
- Pipeline stages
- Agent spawning
- State management
- Error recovery
- Memory operations

User only sees: Clean, unified, expert responses.
