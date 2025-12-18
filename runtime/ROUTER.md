# HIVEMIND Router

> Intelligent task routing. ALL INVISIBLE TO USER.

---

## Routing Algorithm

```
INPUT: User message
  │
  ▼
EXTRACT keywords
  │
  ▼
MATCH against agent triggers
  │
  ▼
SCORE matches by:
  - Keyword match count
  - Keyword specificity
  - Agent availability
  │
  ▼
SELECT primary agent (highest score)
  │
  ▼
IDENTIFY support agents (if complex task)
  │
  ▼
SPAWN selected agents
  │
  ▼
ROUTE task to agents
  │
  ▼
COLLECT outputs
  │
  ▼
SYNTHESIZE into unified response
```

---

## Keyword Mapping

### Development Team

| Keywords | Primary | Support |
|----------|---------|---------|
| architecture, design, system, blueprint, patterns, api design, data model, microservices | DEV-001 | SEC-001, INF-001 |
| backend, api, server, endpoint, python, go, java, service, rest, graphql | DEV-002 | INF-004 |
| frontend, ui, ux, react, vue, angular, css, component, responsive, accessibility | DEV-003 | QA-005 |
| review, code review, PR, pull request, quality, standards, best practices | DEV-004 | QA-004 |
| document, docs, readme, guide, tutorial, api docs, specification | DEV-005 | - |
| deploy, release, ci/cd, pipeline, docker, kubernetes, github actions, gitlab | DEV-006 | INF-001, INF-005 |

### Security Team

| Keywords | Primary | Support |
|----------|---------|---------|
| security design, threat model, security architecture, zero trust, encryption strategy | SEC-001 | SEC-002 |
| pentest, penetration test, hack, exploit, vulnerability, owasp, attack, red team | SEC-002 | QA-004 |
| malware, reverse engineer, binary analysis, ioc, threat intel, ransomware | SEC-003 | - |
| wireless, wifi, bluetooth, rf, radio, iot security, zigbee | SEC-004 | - |
| compliance, audit, soc2, gdpr, pci, hipaa, nist, iso27001 | SEC-005 | - |
| incident, breach, emergency, forensics, containment, recovery | SEC-006 | INF-005 |

### Infrastructure Team

| Keywords | Primary | Support |
|----------|---------|---------|
| infrastructure, cloud, aws, gcp, azure, capacity, scaling, architecture | INF-001 | INF-002, INF-006 |
| sysadmin, server, linux, windows, hardening, patching, configuration | INF-002 | - |
| network, firewall, dns, routing, vpn, load balancer, cdn, subnet | INF-003 | - |
| database, sql, postgres, mysql, mongodb, redis, query, schema, dba, optimization | INF-004 | DEV-002 |
| sre, monitoring, slo, sli, reliability, uptime, observability, prometheus, grafana | INF-005 | QA-003 |
| automate, terraform, ansible, puppet, script, iac, gitops | INF-006 | - |

### QA Team

| Keywords | Primary | Support |
|----------|---------|---------|
| test strategy, qa plan, coverage, quality process, test design | QA-001 | - |
| automated test, selenium, playwright, cypress, pytest, jest, test framework | QA-002 | - |
| load test, performance, benchmark, stress test, k6, jmeter, gatling | QA-003 | INF-005 |
| sast, dast, security scan, devsecops, vulnerability scan, snyk | QA-004 | SEC-002 |
| manual test, exploratory, usability, acceptance, regression | QA-005 | - |
| test data, fixtures, test environment, mock, faker, factory | QA-006 | - |

---

## Complexity Detection

### Simple Task (1 agent)

```
Indicators:
- Single domain keywords
- Specific question
- Clear scope

Example: "How do I sort a list in Python?"
  → DEV-002 only
```

### Medium Task (2-3 agents)

```
Indicators:
- Multiple domain keywords
- Implementation request
- Some breadth

Example: "Create a REST endpoint with database"
  → DEV-002 (primary), INF-004 (support)
```

### Complex Task (4+ agents)

```
Indicators:
- Many domain keywords
- Full feature request
- Security/compliance mentioned
- Performance requirements

Example: "Build secure user authentication with tests"
  → DEV-001, DEV-002, SEC-001, SEC-002, QA-002, QA-004
```

---

## Multi-Agent Decomposition

For complex tasks, decompose and assign:

```
"Build a secure REST API"

Decomposition:
1. Architecture design → DEV-001
2. Security requirements → SEC-001
3. Implementation → DEV-002
4. Security review → SEC-002
5. Test automation → QA-002
6. Security testing → QA-004

Execution:
- Phase 1 (parallel): DEV-001 + SEC-001
- Phase 2: DEV-002 (uses phase 1 output)
- Phase 3 (parallel): SEC-002 + QA-002 + QA-004

Synthesis:
- Merge all outputs into single response
- Apply output filter
- Deliver unified result
```

---

## Routing Priorities

When multiple agents match:

1. **Specificity** - More specific keyword wins
2. **Primary over Support** - Primary agents handle core work
3. **Availability** - Prefer non-busy agents
4. **Recency** - Prefer agent that just handled related work

---

## Fallback Routing

If no keywords match:

```
1. Check context for implicit domain
2. Default to DEV-001 (architect) for technical
3. Default to general capability
4. Never say "I don't know which agent"
```

---

## SILENT OPERATION

**CRITICAL**: Routing is invisible.

Never say:
- "Routing to..."
- "This is a job for..."
- "Let me get the expert in..."
- "I'll need to consult..."

Just provide the answer from the appropriate expertise.
