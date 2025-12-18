# HIVEMIND System Check

> Run this verification to ensure all HIVEMIND components are operational.

---

## Quick Status

```
HIVEMIND STATUS: ACTIVE
Last verified: Check timestamps below
```

---

## Component Checklist

### 1. Core Identity

| Check | Status | Location |
|-------|--------|----------|
| CLAUDE.md exists | ✓ | ./CLAUDE.md |
| Silent operation rules | ✓ | Lines 7-57 |
| Mandatory activation | ✓ | Lines 61-86 |
| Forbidden phrases defined | ✓ | Lines 65-76 |

### 2. Output Filtering

| Check | Status | Location |
|-------|--------|----------|
| OUTPUT-FILTER.md | ✓ | ./runtime/OUTPUT-FILTER.md |
| VOICE-RULES.md | ✓ | ./runtime/VOICE-RULES.md |
| Forbidden patterns defined | ✓ | OUTPUT-FILTER.md |
| Voice transformation rules | ✓ | VOICE-RULES.md |

### 3. Agent System

| Check | Status | Location |
|-------|--------|----------|
| 24 agent definitions | ✓ | ./agents/*/*.md |
| Agent registry | ✓ | CLAUDE.md, COORDINATOR.md |
| Trigger keywords defined | ✓ | CLAUDE.md, SPAWN-PROTOCOL.md |

### 4. Communication System

| Check | Status | Location |
|-------|--------|----------|
| MESSAGE-BUS.md | ✓ | ./comms/MESSAGE-BUS.md |
| SPAWN-PROTOCOL.md | ✓ | ./comms/SPAWN-PROTOCOL.md |
| TEAM-COORDINATION.md | ✓ | ./comms/TEAM-COORDINATION.md |
| Message types defined | ✓ | MESSAGE-BUS.md |
| Agent lifecycle defined | ✓ | SPAWN-PROTOCOL.md |

### 5. Memory System

| Check | Status | Location |
|-------|--------|----------|
| Memory protocol | ✓ | ./memory/MEMORY-PROTOCOL.md |
| Triggers defined | ✓ | ./memory/TRIGGERS.md |
| Query system | ✓ | ./memory/QUERY.md |
| Global memories | ✓ | ./memory/global/*.json |
| Team memories | ✓ | ./memory/teams/*/*.json |
| Agent memories | ✓ | ./memory/agents/*/*.json |
| Session handling | ✓ | ./memory/sessions/current.json |

### 6. Orchestration

| Check | Status | Location |
|-------|--------|----------|
| COORDINATOR.md | ✓ | ./orchestration/COORDINATOR.md |
| Task routing | ✓ | COORDINATOR.md |
| Output sanitization | ✓ | COORDINATOR.md |

### 7. Protocols

| Check | Status | Location |
|-------|--------|----------|
| Handoffs | ✓ | ./protocols/handoffs.md |
| Messages | ✓ | ./protocols/messages.md |
| Security gates | ✓ | ./protocols/security-gates.md |
| Escalation | ✓ | ./protocols/escalation.md |

---

## Verification Commands

### Check Memory Operations

```
Read: ./memory/sessions/current.json
Verify: session_id exists, last_activity recent

Read: ./memory/global/user-profile.json
Verify: Structure valid, accessible
```

### Check Agent Definitions

```
Count files in ./agents/development/ → Should be 6
Count files in ./agents/security/ → Should be 6
Count files in ./agents/infrastructure/ → Should be 6
Count files in ./agents/qa/ → Should be 6
```

### Check Communication System

```
Verify: ./comms/MESSAGE-BUS.md exists
Verify: ./comms/SPAWN-PROTOCOL.md exists
Verify: ./comms/TEAM-COORDINATION.md exists
```

---

## Test Scenarios

### Test 1: Silent Operation

**Input:** "How do I sort a list in Python?"

**Expected:** Clean answer with no agent references

**Verify:**
- [ ] No agent IDs in output
- [ ] No "routing to..." language
- [ ] First person singular voice

### Test 2: Multi-Domain Question

**Input:** "Design a secure REST API"

**Expected:** Unified response covering architecture, security, and testing

**Verify:**
- [ ] Single coherent response
- [ ] No team attribution
- [ ] "I recommend..." not "The architect recommends..."

### Test 3: Memory Trigger

**Input:** "Remember that we use PostgreSQL for this project"

**Expected:** Acknowledgment, memory stored

**Verify:**
- [ ] Memory created in appropriate location
- [ ] Can be recalled later with "What database do we use?"

### Test 4: Complex Workflow

**Input:** "Build me a user authentication system with tests"

**Expected:** Complete deliverable

**Verify:**
- [ ] Architecture considerations included
- [ ] Security considerations included
- [ ] Test strategy included
- [ ] All from unified voice

---

## Health Metrics

### Memory System

```
Global memories: ./memory/global/_index.json
Team memories: 4 teams × ~4 files each
Agent memories: 24 agents × 2 files each
Session: ./memory/sessions/current.json
```

### File Counts

```
Agent definitions: 24
Protocol files: 4
Template files: 9
Config files: 4
Memory schemas: 8
```

---

## Troubleshooting

### If Agent IDs Leak to Output

1. Check ./runtime/OUTPUT-FILTER.md is being applied
2. Verify CLAUDE.md silent operation section
3. Check COORDINATOR.md output sanitization

### If Memory Not Persisting

1. Verify ./memory/sessions/current.json is writable
2. Check memory index files exist
3. Verify trigger patterns match input

### If Routing Fails

1. Check ./orchestration/COORDINATOR.md routing rules
2. Verify trigger keywords in SPAWN-PROTOCOL.md
3. Check agent definition files exist

---

## System Files Summary

```
HIVEMIND/
├── BOOTSTRAP.md                 # Single entry point + load order
├── CLAUDE.md                    # Core identity + rules
├── SYSTEM-CHECK.md              # This file
├── runtime/
│   ├── OUTPUT-FILTER.md         # Forbidden patterns
│   ├── VOICE-RULES.md           # Voice transformation
│   ├── PROJECT-DETECTOR.md      # Project detection
│   ├── PREFLIGHT.md             # Pre-task checks
│   ├── POSTTASK.md              # Post-task learning
│   ├── SELF-IMPROVE.md          # Continuous improvement loop
│   └── PREDICTOR.md             # Predictive assistance
├── comms/
│   ├── MESSAGE-BUS.md           # Agent messaging
│   ├── SPAWN-PROTOCOL.md        # Agent lifecycle
│   └── TEAM-COORDINATION.md     # Cross-team protocols
├── orchestration/
│   └── COORDINATOR.md           # Central orchestration
├── protocols/
│   ├── handoffs.md              # Handoff procedures
│   ├── messages.md              # Message formats
│   ├── security-gates.md        # Security checkpoints
│   ├── QUALITY-GATES.md         # Pre-output validation
│   └── escalation.md            # Escalation rules
├── memory/
│   ├── MEMORY-PROTOCOL.md       # Memory operations
│   ├── TRIGGERS.md              # Auto-triggers
│   ├── QUERY.md                 # Query interface
│   ├── ENGINE.md                # Active learning + engine reference
│   ├── learnings/               # Learning schema
│   ├── short-term/              # Includes project-context.json
│   └── long-term/               # Includes user-profile.json
│   ├── global/                  # Global memories
│   ├── teams/                   # Team memories
│   ├── agents/                  # Agent memories
│   └── sessions/                # Session state
└── agents/
	    ├── development/ (6)
	    ├── security/ (6)
	    ├── infrastructure/ (6)
	    ├── qa/ (6)
	    └── registry/ (24)
```

---

## Version

```
HIVEMIND Version: 2.0
Enhanced: 2025-12-18
Features:
  - Silent operation (invisible agents)
  - Mandatory activation (always-on)
  - Inter-agent communication (message bus)
  - Cross-team coordination (team protocols)
  - Persistent memory (JSON-based)
```
