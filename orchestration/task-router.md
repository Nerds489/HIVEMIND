# HIVEMIND Task Router

## Overview

The Task Router is responsible for analyzing incoming requests and routing them to the appropriate agent(s) or workflow. It operates as the intelligent front-door to HIVEMIND, ensuring tasks reach the right expertise.

---

## Routing Decision Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INCOMING REQUEST                              │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │     KEYWORD EXTRACTION        │
                    │  (Identify domain signals)    │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │    COMPLEXITY ASSESSMENT      │
                    │  (Single vs Multi-Agent?)     │
                    └───────────────────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │  SINGLE AGENT   │   │   TEAM-LEVEL    │   │    WORKFLOW     │
    │    ROUTING      │   │    ROUTING      │   │    ROUTING      │
    └─────────────────┘   └─────────────────┘   └─────────────────┘
              │                     │                     │
              ▼                     ▼                     ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    LOAD AGENT CONTEXT                        │
    │              (Read agent .md files)                          │
    └─────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                       EXECUTE                                │
    └─────────────────────────────────────────────────────────────┘
```

---

## Keyword-to-Agent Mapping

### Development Keywords

| Keyword Pattern | Primary Agent | Confidence |
|-----------------|---------------|------------|
| `architect`, `design`, `system design`, `blueprint` | DEV-001 | High |
| `backend`, `api`, `server`, `endpoint`, `rest`, `graphql` | DEV-002 | High |
| `frontend`, `ui`, `ux`, `react`, `vue`, `css`, `component` | DEV-003 | High |
| `review`, `pr`, `pull request`, `code quality` | DEV-004 | High |
| `document`, `docs`, `readme`, `api docs`, `guide` | DEV-005 | High |
| `ci`, `cd`, `pipeline`, `deploy`, `build`, `release` | DEV-006 | High |
| `python`, `node`, `java`, `go` (general code) | DEV-002 | Medium |
| `html`, `javascript`, `typescript` (general) | DEV-003 | Medium |

### Security Keywords

| Keyword Pattern | Primary Agent | Confidence |
|-----------------|---------------|------------|
| `security architecture`, `threat model`, `security design` | SEC-001 | High |
| `pentest`, `penetration`, `exploit`, `hack`, `vulnerability` | SEC-002 | High |
| `malware`, `reverse engineer`, `binary`, `disassemble` | SEC-003 | High |
| `wireless`, `wifi`, `bluetooth`, `rf`, `wpa` | SEC-004 | High |
| `compliance`, `audit`, `gdpr`, `soc2`, `pci`, `hipaa` | SEC-005 | High |
| `incident`, `breach`, `forensics`, `compromise` | SEC-006 | High |
| `security scan`, `sast`, `dast` | QA-004 | High |
| `secure`, `security` (general) | SEC-001 | Medium |

### Infrastructure Keywords

| Keyword Pattern | Primary Agent | Confidence |
|-----------------|---------------|------------|
| `infrastructure`, `cloud`, `aws`, `azure`, `gcp`, `capacity` | INF-001 | High |
| `sysadmin`, `linux`, `windows`, `server`, `configuration` | INF-002 | High |
| `network`, `firewall`, `dns`, `routing`, `vpn`, `load balancer` | INF-003 | High |
| `database`, `sql`, `postgresql`, `mysql`, `mongodb`, `query` | INF-004 | High |
| `sre`, `reliability`, `monitoring`, `alerting`, `slo`, `oncall` | INF-005 | High |
| `terraform`, `ansible`, `automation`, `iac` | INF-006 | High |
| `kubernetes`, `docker`, `container` | INF-001 | Medium |

### QA Keywords

| Keyword Pattern | Primary Agent | Confidence |
|-----------------|---------------|------------|
| `test strategy`, `qa process`, `quality`, `coverage` | QA-001 | High |
| `test automation`, `selenium`, `playwright`, `cypress` | QA-002 | High |
| `performance`, `load test`, `stress test`, `benchmark` | QA-003 | High |
| `security testing`, `vulnerability scan` | QA-004 | High |
| `manual testing`, `exploratory`, `uat`, `acceptance` | QA-005 | High |
| `test data`, `fixtures`, `mock`, `environment` | QA-006 | High |
| `test`, `testing` (general) | QA-001 | Medium |
| `bug`, `defect` | QA-005 | Medium |

---

## Complexity Scoring Algorithm

```python
def calculate_complexity(request: str) -> int:
    """
    Returns complexity score 0-10
    0-3: Simple (single agent)
    4-6: Moderate (primary + consultation)
    7-10: Complex (multi-agent workflow)
    """
    score = 0

    # Multi-team indicators (+2 each)
    if mentions_multiple_teams(request):
        score += 2

    # Security implications (+2)
    if has_security_implications(request):
        score += 2

    # Production impact (+3)
    if affects_production(request):
        score += 3

    # Architectural changes (+2)
    if requires_architecture_changes(request):
        score += 2

    # Compliance/regulatory (+2)
    if has_compliance_requirements(request):
        score += 2

    # Time-sensitive (+1)
    if is_urgent(request):
        score += 1

    return min(score, 10)
```

### Complexity Response

| Score | Classification | Routing Action |
|-------|---------------|----------------|
| 0-3 | Simple | Route to single best-match agent |
| 4-6 | Moderate | Route to primary agent, identify consultants |
| 7-10 | Complex | Activate workflow or multi-agent coordination |

---

## Workflow Triggers

Certain patterns automatically trigger pre-defined workflows:

| Request Pattern | Workflow | Lead Agent |
|-----------------|----------|------------|
| "full sdlc", "end to end development", "complete feature" | `full-sdlc.md` | DEV-001 |
| "security assessment", "pentest", "vulnerability assessment" | `security-assessment.md` | SEC-001 |
| "incident", "breach", "emergency", "outage" | `incident-response.md` | SEC-006 |
| "code review", "review pr", "review pipeline" | `code-review.md` | DEV-004 |
| "deploy to production", "release", "go live" | `infrastructure-deploy.md` | INF-005 |
| "compliance audit", "regulatory assessment" | `compliance-audit.md` | SEC-005 |

---

## Routing Examples

### Example 1: Simple Request
```
Input: "Write a Python function to parse CSV files"
Analysis:
  - Keywords: "Python", "function"
  - Complexity: 1 (simple code task)
  - Routing: DEV-002 (Backend Developer)
```

### Example 2: Moderate Request
```
Input: "Review this authentication code for security issues"
Analysis:
  - Keywords: "review", "authentication", "security"
  - Complexity: 5 (code + security)
  - Routing: DEV-004 (primary) + QA-004 (security consultation)
```

### Example 3: Complex Request
```
Input: "We need to design and implement a new microservices
        authentication system with proper security, testing,
        and deployment to production"
Analysis:
  - Keywords: "design", "implement", "authentication", "security",
             "testing", "deployment", "production"
  - Complexity: 9 (multi-team, production, security)
  - Routing: Activate full-sdlc.md workflow
```

### Example 4: Emergency Request
```
Input: "Production is down, possible security breach"
Analysis:
  - Keywords: "production", "down", "security breach"
  - Complexity: 10 (emergency)
  - Routing: Activate incident-response.md workflow (immediate)
```

---

## Ambiguity Resolution

When routing is unclear:

### Strategy 1: Request Clarification
```json
{
  "routing_status": "ambiguous",
  "possible_routes": [
    {"agent": "DEV-002", "confidence": 0.4, "reason": "Code-related keywords"},
    {"agent": "INF-004", "confidence": 0.4, "reason": "Database keywords"}
  ],
  "clarification_needed": "Is this about application code or database administration?"
}
```

### Strategy 2: Default to Team Lead
If ambiguous within a domain, route to team architect:
- Development ambiguity → DEV-001 (Architect)
- Security ambiguity → SEC-001 (Security Architect)
- Infrastructure ambiguity → INF-001 (Infrastructure Architect)
- QA ambiguity → QA-001 (QA Architect)

### Strategy 3: Coordinator Decision
For cross-domain ambiguity, escalate to COORDINATOR for decomposition.

---

## Agent Availability Check

Before routing, verify agent is appropriate:

```yaml
availability_check:
  steps:
    - Verify agent exists in registry
    - Check agent capabilities match task
    - Verify no conflicts (e.g., can't review own code)
    - Check security gates (e.g., production access)

  on_unavailable:
    - Try secondary agent
    - Escalate to team lead
    - Request human decision
```

---

## Routing Audit Trail

All routing decisions are logged:

```json
{
  "routing_decision": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "REQ-20240115-001",
    "request_summary": "Review authentication code",
    "keywords_extracted": ["review", "authentication", "code"],
    "complexity_score": 5,
    "routing_type": "moderate",
    "primary_agent": "DEV-004",
    "secondary_agents": ["QA-004"],
    "workflow_triggered": null,
    "confidence": 0.85,
    "decision_rationale": "Code review with security implications"
  }
}
```

---

## Integration Points

The Task Router integrates with:

1. **COORDINATOR** - Receives decomposed sub-tasks
2. **Context Manager** - Retrieves relevant prior context
3. **Agent Registry** - Validates agent capabilities
4. **Workflow Engine** - Triggers multi-agent pipelines
5. **Security Gates** - Validates routing permissions
