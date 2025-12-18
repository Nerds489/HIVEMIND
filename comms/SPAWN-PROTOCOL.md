# HIVEMIND Spawn Protocol

> Agent lifecycle management and on-demand activation.
> **ALL SPAWNING IS INVISIBLE TO USER** - See runtime/OUTPUT-FILTER.md

---

## Agent Lifecycle States

```
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT LIFECYCLE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   DORMANT ──spawn──> WARMING ──ready──> ACTIVE ──cool──> COOLING │
│      ▲                                              │            │
│      │                                              │            │
│      └──────────────────────────────────────────────┘            │
│                         timeout                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### State Definitions

| State | Description | Duration |
|-------|-------------|----------|
| **DORMANT** | Agent definition exists but not loaded | Indefinite |
| **WARMING** | Loading context, memories, preparing | 1-5 seconds |
| **ACTIVE** | Ready to process requests | While in use |
| **COOLING** | Completing final tasks, saving state | 5-15 seconds |

---

## Spawn Triggers

### Automatic Triggers

Agents spawn automatically when:

1. **Keyword Detection** - Task contains agent's trigger keywords
2. **Message Received** - Message bus routes to dormant agent
3. **Workflow Phase** - Workflow enters phase requiring agent
4. **Dependency Request** - Active agent requests dormant agent
5. **Escalation** - Lower-level resolution failed

### Trigger Keywords by Agent

```yaml
DEV-001 (Architect):
  - design, architect, architecture, blueprint, system design
  - api design, data model, microservices, patterns

DEV-002 (Backend):
  - backend, api, server, endpoint, database code
  - python, go, java, service implementation

DEV-003 (Frontend):
  - frontend, ui, ux, react, vue, component
  - css, responsive, accessibility, client-side

DEV-004 (Code Reviewer):
  - review, code review, PR, pull request
  - code quality, standards, best practices

DEV-005 (Technical Writer):
  - document, docs, readme, guide, tutorial
  - api documentation, write docs

DEV-006 (DevOps):
  - deploy, release, ci/cd, pipeline
  - docker, kubernetes, github actions

SEC-001 (Security Architect):
  - security design, threat model, security architecture
  - zero trust, encryption strategy

SEC-002 (Penetration Tester):
  - pentest, hack, exploit, vulnerability
  - owasp, security testing, attack

SEC-003 (Malware Analyst):
  - malware, reverse engineer, binary analysis
  - ioc, threat intelligence

SEC-004 (Wireless Security):
  - wireless, wifi, bluetooth, rf
  - iot security, radio frequency

SEC-005 (Compliance):
  - compliance, audit, soc2, gdpr, pci
  - hipaa, nist, regulatory

SEC-006 (Incident Responder):
  - incident, breach, emergency, forensics
  - containment, recovery, crisis

INF-001 (Infrastructure Architect):
  - infrastructure, cloud design, capacity
  - aws, gcp, azure, scaling

INF-002 (Sysadmin):
  - sysadmin, server, linux, windows server
  - hardening, patching, configuration

INF-003 (Network Engineer):
  - network, firewall, dns, routing
  - vpn, load balancer, subnet

INF-004 (DBA):
  - dba, database, sql, postgres, mongodb
  - query optimization, replication

INF-005 (SRE):
  - sre, monitoring, slo, reliability
  - uptime, on-call, observability

INF-006 (Automation):
  - automate, terraform, ansible, script
  - infrastructure as code, gitops

QA-001 (QA Architect):
  - test strategy, qa plan, coverage
  - quality process, test design

QA-002 (Test Automation):
  - automated test, selenium, playwright
  - pytest, jest, test framework

QA-003 (Performance Tester):
  - load test, performance, benchmark
  - stress test, bottleneck, k6, jmeter

QA-004 (Security Tester):
  - sast, dast, security scan, devsecops
  - vulnerability scanning

QA-005 (Manual QA):
  - manual test, exploratory, usability
  - user acceptance, bug hunting

QA-006 (Test Data):
  - test data, fixtures, test environment
  - data generation, mocking
```

---

## Spawn Process

### Step 1: Trigger Detection

```
INPUT: User request or internal message
         │
         ▼
┌─────────────────────────────────────┐
│ Scan for trigger keywords           │
│ Check message routing               │
│ Check workflow requirements         │
└─────────────────┬───────────────────┘
                  │
                  ▼
         [Identify required agents]
```

### Step 2: Agent Activation

```
FOR EACH required agent:
  │
  ├── If ACTIVE: Route message directly
  │
  └── If DORMANT:
      │
      ▼
┌─────────────────────────────────────┐
│ 1. Set state to WARMING             │
│ 2. Load agent definition            │
│ 3. Load agent-specific memories     │
│ 4. Load relevant context            │
│ 5. Initialize working memory        │
│ 6. Set state to ACTIVE              │
└─────────────────────────────────────┘
```

### Step 3: Context Injection

When spawning, inject:

```json
{
  "spawn_context": {
    "trigger_source": "keyword|message|workflow|dependency",
    "triggering_task": "description of task",
    "parent_agent": "agent that requested spawn (if any)",
    "priority": "P0-P4",
    "memories_to_load": [
      "agent-specific memories",
      "relevant team memories",
      "task-related memories"
    ],
    "handoff_context": "if spawned for handoff, include package",
    "deadline": "if time-constrained"
  }
}
```

### Step 4: Ready Confirmation

```
Agent confirms ready:
{
  "agent_id": "SEC-002",
  "state": "ACTIVE",
  "context_loaded": true,
  "memories_loaded": ["mem_001", "mem_002"],
  "ready_at": "2025-12-18T10:00:05Z"
}
```

---

## Agent Capabilities Matrix

### Can Request (who can this agent call)

```yaml
DEV-001:
  can_request: [DEV-002, DEV-003, DEV-004, DEV-005, DEV-006, SEC-001, INF-001, QA-001]

DEV-002:
  can_request: [DEV-001, DEV-004, INF-004, QA-002]

DEV-003:
  can_request: [DEV-001, DEV-002, DEV-004, QA-005]

DEV-004:
  can_request: [DEV-001, DEV-002, DEV-003, QA-004, SEC-002]

DEV-005:
  can_request: [all agents for documentation needs]

DEV-006:
  can_request: [DEV-001, INF-001, INF-005, INF-006, QA-002]

SEC-001:
  can_request: [all SEC agents, DEV-001, INF-001, QA-001]

SEC-002:
  can_request: [SEC-001, SEC-003, DEV-002, DEV-003, QA-004]

SEC-003:
  can_request: [SEC-001, SEC-006, INF-005]

SEC-004:
  can_request: [SEC-001, SEC-002, INF-003]

SEC-005:
  can_request: [SEC-001, all team leads, QA-001]

SEC-006:
  can_request: [all agents for incident response]

INF-001:
  can_request: [all INF agents, DEV-001, SEC-001, QA-001]

INF-002:
  can_request: [INF-001, INF-003, INF-006, SEC-002]

INF-003:
  can_request: [INF-001, INF-002, SEC-004]

INF-004:
  can_request: [INF-001, DEV-002, QA-003]

INF-005:
  can_request: [INF-001, all agents for incidents, SEC-006]

INF-006:
  can_request: [all INF agents, DEV-006]

QA-001:
  can_request: [all QA agents, DEV-001, SEC-005]

QA-002:
  can_request: [QA-001, DEV-002, DEV-003, DEV-006]

QA-003:
  can_request: [QA-001, INF-004, INF-005, DEV-002]

QA-004:
  can_request: [QA-001, SEC-002, DEV-004]

QA-005:
  can_request: [QA-001, DEV-003, QA-002]

QA-006:
  can_request: [QA-001, INF-004, all QA agents]
```

### Provides To (who might call this agent)

```yaml
DEV-001:
  provides_to: [all DEV agents, SEC-001, INF-001, QA-001]

DEV-002:
  provides_to: [DEV-001, DEV-003, DEV-004, INF-004, QA-002, QA-003]

DEV-003:
  provides_to: [DEV-001, DEV-002, DEV-004, QA-005]

DEV-004:
  provides_to: [all DEV agents, QA-004]

DEV-005:
  provides_to: [all agents for documentation]

DEV-006:
  provides_to: [DEV-001, INF-001, INF-005, QA-002]

# Similar for SEC, INF, QA teams...
```

---

## Cooling Process

When agent work completes:

```
ACTIVE → COOLING
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Complete any pending responses   │
│ 2. Save working memory state        │
│ 3. Create task completion memory    │
│ 4. Update agent memory index        │
│ 5. Release resources                │
│ 6. Set state to DORMANT             │
└─────────────────────────────────────┘
```

### Cooling Timeout

If no new messages within **30 seconds** of task completion:
- Agent automatically cools down
- State transitions to DORMANT
- Context saved for quick re-spawn

---

## Parallel Spawning

For multi-agent tasks, spawn in parallel:

```
Task requires: DEV-001, SEC-001, INF-001
         │
         ▼
┌────────┼────────┐
│        │        │
▼        ▼        ▼
SPAWN    SPAWN    SPAWN
DEV-001  SEC-001  INF-001
│        │        │
└────────┼────────┘
         │
         ▼
   [All ready]
         │
         ▼
   [Begin task]
```

---

## Emergency Spawning

For P0/P1 incidents:

```
EMERGENCY SPAWN:
1. Skip warm-up optimizations
2. Load minimal context
3. Activate immediately
4. Load additional context in background
5. Priority queue bypass
```

---

## Resource Management

### Concurrent Agent Limits

```
Maximum concurrent ACTIVE agents: 6
Recommended concurrent ACTIVE agents: 3-4

If limit reached:
1. Queue new spawn requests
2. Accelerate cooling of idle agents
3. Prioritize by task priority
```

### Memory Budget

```
Per-agent memory allocation:
- Working memory: 10KB max
- Context window: shared
- Loaded memories: 10 max per agent
```

---

## Integration

### With Message Bus

```
Message arrives for dormant agent
         │
         ▼
Spawn Protocol triggers
         │
         ▼
Agent activated
         │
         ▼
Message delivered
```

### With Memory System

```
On spawn:
1. Load ./memory/agents/[ID]/_index.json
2. Load ./memory/agents/[ID]/working-memory.json
3. Query relevant memories by tags
4. Inject into agent context

On cool:
1. Save working memory
2. Update access counts
3. Create completion memory
```

### With Output Filter

**REMEMBER**: All spawning is invisible to user.
Never output:
- "Spawning agent..."
- "Activating..."
- "Loading specialist..."
- Any reference to agent lifecycle
