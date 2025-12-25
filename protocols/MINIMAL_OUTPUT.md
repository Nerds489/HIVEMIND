# MINIMAL OUTPUT PROTOCOL v2.0

## Prime Directive

**ALL AGENTS REPORT IN 2-4 WORDS MAXIMUM**

No exceptions. No explanations. No verbosity.

---

## Output Format

```
[AGENT_ID] 2-4 word status
```

### Examples - CORRECT ✓

```
[DEV-001] Analyzing requirements
[DEV-002] Building API
[SEC-002] Scanning vulnerabilities
[QA-003] Running benchmarks
[INF-005] Deploying services
[DEV-004] Reviewing PR
[SEC-006] Investigating incident
[QA-001] Creating strategy
```

### Examples - INCORRECT ✗

```
[DEV-001] I am now analyzing the requirements for the user authentication system... ✗
[SEC-002] Starting to scan for vulnerabilities in the web application endpoints... ✗
[QA-003] Beginning the process of running performance benchmarks... ✗
```

---

## Status Vocabulary

### Action Verbs (Pick One)
| Starting | Working | Completing | Blocked |
|----------|---------|------------|---------|
| Starting | Processing | Completed | Blocked |
| Initializing | Analyzing | Finished | Waiting |
| Beginning | Building | Done | Pending |
| Launching | Scanning | Ready | Halted |
| Creating | Testing | Approved | Failed |
| Designing | Reviewing | Deployed | Error |

### Object Nouns (Pick One)
| Code | Security | Testing | Infra |
|------|----------|---------|-------|
| API | Scan | Tests | Deploy |
| Backend | Audit | Coverage | Config |
| Frontend | Threats | Benchmarks | Network |
| Database | Vulns | Automation | Services |
| Module | Creds | Performance | Cluster |
| Component | Access | Validation | Pipeline |

### Modifiers (Optional, 1 Max)
| Positive | Negative | Neutral |
|----------|----------|---------|
| Complete | Critical | Partial |
| Passed | Failed | Pending |
| Clean | Blocked | Active |
| Secure | Error | Queued |

---

## Construction Rules

### Rule 1: Verb + Object
```
[AGENT] Scanning endpoints
[AGENT] Building API
[AGENT] Testing components
```

### Rule 2: Verb + Modifier + Object
```
[AGENT] Running full scan
[AGENT] Deploying production services
[AGENT] Creating unit tests
```

### Rule 3: Object + Status
```
[AGENT] Scan complete
[AGENT] Tests passing
[AGENT] Deploy ready
```

### Rule 4: Status Only (End State)
```
[AGENT] Complete
[AGENT] Blocked
[AGENT] Ready
```

---

## Agent-Specific Templates

### DEV Team
| Agent | Common Outputs |
|-------|----------------|
| DEV-001 | `Designing architecture`, `Creating ADR`, `Review complete` |
| DEV-002 | `Building backend`, `API complete`, `Database ready` |
| DEV-003 | `Building UI`, `Components ready`, `Styling complete` |
| DEV-004 | `Reviewing code`, `Issues found`, `Approved` |
| DEV-005 | `Writing docs`, `API docs ready`, `Guide complete` |
| DEV-006 | `Pipeline setup`, `CI configured`, `Deploy ready` |

### SEC Team
| Agent | Common Outputs |
|-------|----------------|
| SEC-001 | `Threat modeling`, `Security design`, `Architecture review` |
| SEC-002 | `Penetration testing`, `Vulnerabilities found`, `Scan complete` |
| SEC-003 | `Analyzing malware`, `IOCs extracted`, `Report ready` |
| SEC-004 | `Testing wireless`, `WiFi audit`, `RF analysis` |
| SEC-005 | `Compliance audit`, `Gaps identified`, `Report ready` |
| SEC-006 | `Incident response`, `Containment active`, `Recovery complete` |

### INF Team
| Agent | Common Outputs |
|-------|----------------|
| INF-001 | `Architecture design`, `Cloud planning`, `Infrastructure ready` |
| INF-002 | `System config`, `Servers ready`, `Patches applied` |
| INF-003 | `Network setup`, `Firewall configured`, `Routes active` |
| INF-004 | `Database setup`, `Optimization complete`, `Backup ready` |
| INF-005 | `Monitoring setup`, `SLOs defined`, `Alerts active` |
| INF-006 | `Automation scripts`, `IaC ready`, `Pipeline complete` |

### QA Team
| Agent | Common Outputs |
|-------|----------------|
| QA-001 | `Strategy planning`, `Test plan ready`, `Coverage analyzed` |
| QA-002 | `Writing automation`, `Framework ready`, `Scripts complete` |
| QA-003 | `Load testing`, `Performance baseline`, `Benchmarks complete` |
| QA-004 | `Security testing`, `DAST running`, `Vulnerabilities logged` |
| QA-005 | `Manual testing`, `UAT complete`, `Bugs logged` |
| QA-006 | `Data setup`, `Environments ready`, `Fixtures loaded` |

---

## Progress Indicators

### Sequential Progress
```
[DEV-002] Building API (1/4)
[DEV-002] Building API (2/4)
[DEV-002] Building API (3/4)
[DEV-002] API complete
```

### Percentage (Only for Long Tasks)
```
[QA-003] Load test 25%
[QA-003] Load test 50%
[QA-003] Load test 75%
[QA-003] Load test complete
```

---

## Error Output

### Format
```
[AGENT] ERROR: 2-3 word description
```

### Examples
```
[SEC-002] ERROR: Critical vuln
[DEV-002] ERROR: Build failed
[INF-005] ERROR: Deploy blocked
[QA-003] ERROR: Test timeout
```

---

## Handoff Format

```
[AGENT_FROM] → [AGENT_TO]: 2-4 word context
```

### Examples
```
[DEV-002] → [DEV-004]: Backend ready review
[DEV-004] → [QA-002]: Approved for testing
[QA-002] → [INF-005]: Tests passed deploy
```

---

## Parallel Execution Display

```
╔═══════════════════════════════════╗
║ PARALLEL EXECUTION                 ║
╠═══════════════════════════════════╣
║ [DEV-001] Designing architecture   ║
║ [SEC-001] Threat modeling          ║
║ [QA-001] Planning strategy         ║
║ [INF-001] Capacity planning        ║
╚═══════════════════════════════════╝
```

---

## Sequential Pipeline Display

```
[DEV-002] Building backend
    ↓
[DEV-004] Reviewing code
    ↓
[QA-002] Running tests
    ↓
[INF-005] Deploying
```

---

## Enforcement

### In Agent Definitions
Every agent definition MUST include:
```markdown
## Output Rules
- Maximum 4 words per status
- Format: [ID] status
- No explanations
- Action-focused language
```

### In HEAD_CODEX
HEAD_CODEX truncates any verbose output:
```python
def enforce_minimal(status: str, agent_id: str) -> str:
    words = status.split()
    if len(words) > 4:
        return f"[{agent_id}] {' '.join(words[:4])}"
    return f"[{agent_id}] {status}"
```

---

## Summary

| Rule | Description |
|------|-------------|
| **MAX_WORDS** | 4 words maximum per status |
| **FORMAT** | `[AGENT_ID] status` |
| **VERBS** | Action-focused present tense |
| **NO_EXPLAIN** | Never explain, just state |
| **ERRORS** | `ERROR:` prefix, 3 words max |
| **HANDOFFS** | Arrow notation with context |

---

*Minimal Output Protocol — Say More With Less*
