# HIVEMIND Agent Spawning Protocol

> On-demand agent activation. ALL INVISIBLE TO USER.

---

## Agent States

```
DORMANT ──spawn──> ACTIVE ──complete──> DORMANT
                     │
                     └──timeout──> DORMANT
```

| State | Description |
|-------|-------------|
| DORMANT | Definition exists, not loaded |
| ACTIVE | Loaded, processing requests |

---

## Spawn Triggers

### Keyword Detection

Agent spawns when task contains their keywords:

```yaml
DEV-001: [architecture, design, system, blueprint, api design]
DEV-002: [backend, api, server, endpoint, service, python, go]
DEV-003: [frontend, ui, ux, react, vue, component, css]
DEV-004: [review, code review, PR, quality, standards]
DEV-005: [document, docs, readme, guide, tutorial]
DEV-006: [deploy, ci/cd, pipeline, docker, kubernetes]

SEC-001: [security design, threat model, encryption, zero trust]
SEC-002: [pentest, hack, exploit, vulnerability, owasp]
SEC-003: [malware, reverse engineer, binary, ioc]
SEC-004: [wireless, wifi, bluetooth, rf, iot]
SEC-005: [compliance, audit, soc2, gdpr, pci, hipaa]
SEC-006: [incident, breach, emergency, forensics]

INF-001: [infrastructure, cloud, aws, gcp, azure, capacity]
INF-002: [sysadmin, server, linux, windows, hardening]
INF-003: [network, firewall, dns, routing, vpn]
INF-004: [database, sql, postgres, mysql, mongodb, dba]
INF-005: [sre, monitoring, slo, reliability, uptime]
INF-006: [automate, terraform, ansible, script, iac]

QA-001: [test strategy, qa plan, coverage, quality process]
QA-002: [automated test, selenium, playwright, pytest]
QA-003: [load test, performance, benchmark, stress test]
QA-004: [sast, dast, security scan, devsecops]
QA-005: [manual test, exploratory, usability]
QA-006: [test data, fixtures, test environment, mock]
```

### Message Receipt

Agent spawns when message bus routes message to them.

### Dependency Request

Active agent requests dormant agent → spawn dormant agent.

---

## Spawn Process

```
1. DETECT trigger (keyword/message/request)
2. LOAD agent definition from agents/registry/
3. INJECT context:
   - Task description
   - Relevant memories
   - Parent agent context (if spawned by another)
4. SET state to ACTIVE
5. PROCESS request
6. RETURN results
7. SET state to DORMANT (after timeout or completion)
```

---

## Context Injection

When spawning, provide:

```json
{
  "spawn_context": {
    "trigger": "keyword|message|dependency",
    "task": "description",
    "parent_agent": "ID or null",
    "priority": "P0-P3",
    "memories": ["relevant", "memories"],
    "deadline": "timestamp or null"
  }
}
```

---

## Agent Capabilities

### Can Request (who this agent can spawn)

```yaml
DEV-001: [DEV-002, DEV-003, DEV-004, DEV-005, DEV-006, SEC-001, INF-001, QA-001]
DEV-002: [DEV-001, DEV-004, INF-004, QA-002]
DEV-003: [DEV-001, DEV-002, DEV-004, QA-005]
DEV-004: [DEV-001, DEV-002, DEV-003, QA-004, SEC-002]
DEV-005: [all - for documentation]
DEV-006: [DEV-001, INF-001, INF-005, INF-006, QA-002]

SEC-001: [all SEC, DEV-001, INF-001, QA-001]
SEC-002: [SEC-001, SEC-003, DEV-002, DEV-003, QA-004]
SEC-003: [SEC-001, SEC-006, INF-005]
SEC-004: [SEC-001, SEC-002, INF-003]
SEC-005: [SEC-001, all leads]
SEC-006: [all - for incidents]

INF-001: [all INF, DEV-001, SEC-001, QA-001]
INF-002: [INF-001, INF-003, INF-006, SEC-002]
INF-003: [INF-001, INF-002, SEC-004]
INF-004: [INF-001, DEV-002, QA-003]
INF-005: [INF-001, all for incidents, SEC-006]
INF-006: [all INF, DEV-006]

QA-001: [all QA, DEV-001, SEC-005]
QA-002: [QA-001, DEV-002, DEV-003, DEV-006]
QA-003: [QA-001, INF-004, INF-005, DEV-002]
QA-004: [QA-001, SEC-002, DEV-004]
QA-005: [QA-001, DEV-003, QA-002]
QA-006: [QA-001, INF-004, all QA]
```

---

## Concurrent Agents

Multiple agents can be ACTIVE simultaneously:

```
Max concurrent: 6
Recommended: 3-4

If limit reached:
  1. Queue new spawns
  2. Process by priority
  3. Complete current agents first
```

---

## Deactivation

Agent returns to DORMANT when:
- Task complete
- No messages for 30 seconds
- Explicit deactivation
- Higher priority agent needs resources

---

## SILENT OPERATION

**CRITICAL**: Spawning is never visible to user.

Never say:
- "Spawning agent..."
- "Activating..."
- "Loading specialist..."
- "Agent X is now handling..."

Just seamlessly provide the expertise.
