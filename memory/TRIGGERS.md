# Automatic Memory Triggers

> When and how memories are automatically created, loaded, and updated.

---

## Task-Based Triggers

These triggers fire based on task type and context.

| Event | Memory Action | Type | Scope | Priority |
|-------|---------------|------|-------|----------|
| User states preference | Create | factual | global/user-profile | high |
| User corrects agent | Create | procedural | agent | high |
| New project started | Create | factual | project | high |
| Architecture decision made | Create | semantic | team/project | critical |
| Bug discovered | Create | episodic | team:qa | high |
| Bug fixed | Create | procedural | team:qa | high |
| Test failed then passed | Create | procedural | team:qa | medium |
| Security finding | Create | factual | team:security | critical |
| Vulnerability found | Create | episodic | team:security | critical |
| Incident resolved | Create | episodic + procedural | team:security | critical |
| Deployment completed | Create | episodic | team:infrastructure | medium |
| Performance issue found | Create | factual | team:infrastructure | high |
| Code pattern identified | Create | semantic | team:development | medium |
| API endpoint documented | Create | factual | team:development | medium |
| Compliance requirement noted | Create | factual | team:security | critical |
| Error resolved | Create | procedural | agent | high |
| Successful workaround | Create | procedural | team | high |
| Configuration change | Create | factual | scope varies | medium |

---

## Keyword Triggers

These phrases trigger automatic memory operations.

### Memory Creation Triggers

| Keyword Pattern | Action | Type | Scope |
|-----------------|--------|------|-------|
| "remember that..." | Create memory | factual | global |
| "remember:" | Create memory | factual | global |
| "don't forget..." | Create memory (high priority) | factual | global |
| "important:" | Create memory (high priority) | factual | global |
| "we decided..." | Create decision | semantic | team/project |
| "the decision is..." | Create decision | semantic | team/project |
| "the fix was..." | Create procedure | procedural | team |
| "the solution is..." | Create procedure | procedural | team |
| "the problem was..." | Create incident | episodic | team |
| "the issue was..." | Create incident | episodic | team |
| "always do..." | Create procedure | procedural | global |
| "never do..." | Create anti-pattern | procedural | global |
| "I prefer..." | Update user profile | factual | global/user-profile |
| "I like..." | Update user profile | factual | global/user-profile |
| "going forward..." | Create procedure | procedural | scope varies |
| "lesson learned..." | Create learning | procedural | team |
| "note to self..." | Create note | working | session |
| "for future reference..." | Create memory | factual | global |
| "this is how..." | Create procedure | procedural | team |
| "[term] means..." | Create terminology | semantic | global |
| "[term] is defined as..." | Create terminology | semantic | global |

### Memory Query Triggers

| Keyword Pattern | Action |
|-----------------|--------|
| "what did we decide about..." | Query semantic/decisions |
| "how do we..." | Query procedural |
| "what's the process for..." | Query procedural |
| "what happened when..." | Query episodic |
| "what is [term]..." | Query semantic/terminology |
| "remind me..." | Query by keywords |
| "what do we know about..." | Query all types |
| "show me the..." | Query specific type |

### Memory Management Triggers

| Keyword Pattern | Action |
|-----------------|--------|
| "forget about..." | Archive memory |
| "delete memory..." | Archive memory |
| "update memory..." | Update existing |
| "correct that..." | Update existing |
| "that's wrong..." | Flag for review |
| "that's outdated..." | Archive or update |

---

## Context-Based Triggers

### Task Type Detection

| Detected Task Type | Auto-Load Memories |
|-------------------|-------------------|
| Code review | codebase-knowledge, test-patterns, architecture-decisions |
| Security task | threat-intelligence, vulnerability-history, compliance-requirements |
| Infrastructure task | system-inventory, network-topology, runbooks |
| Debugging task | known-bugs, relevant procedures, error memories |
| New feature | architecture-decisions, tech-debt, codebase-knowledge |
| Incident response | incident-learnings, runbooks, contacts |
| Documentation | terminology, codebase-knowledge, decisions |
| Testing | test-patterns, environment-configs, known-bugs |
| Deployment | runbooks, capacity-baselines, system-inventory |
| Performance | capacity-baselines, metrics, optimization procedures |

### Agent Activation

| Agent ID | Auto-Load Memories |
|----------|-------------------|
| DEV-001 | architecture-decisions, codebase-knowledge, patterns |
| DEV-002 | codebase-knowledge, api conventions, tech-debt |
| DEV-003 | ui patterns, accessibility, frontend conventions |
| DEV-004 | code standards, test-patterns, anti-patterns |
| DEV-005 | terminology, documentation standards, templates |
| DEV-006 | deployment procedures, ci/cd, runbooks |
| SEC-001 | threat-intelligence, compliance, security decisions |
| SEC-002 | vulnerability-history, exploits, findings |
| SEC-003 | malware analysis history, iocs, tools |
| SEC-004 | wireless procedures, rf findings, protocols |
| SEC-005 | compliance-requirements, audit history, frameworks |
| SEC-006 | incident-learnings, playbooks, contacts |
| INF-001 | system-inventory, architecture, capacity |
| INF-002 | server configs, hardening, maintenance |
| INF-003 | network-topology, firewall rules, dns |
| INF-004 | database configs, query patterns, optimization |
| INF-005 | slo/sli, runbooks, incident history |
| INF-006 | automation scripts, terraform, ansible |
| QA-001 | test-patterns, coverage standards, quality metrics |
| QA-002 | automation frameworks, test utilities, patterns |
| QA-003 | performance baselines, load test history |
| QA-004 | security test patterns, scanning configs |
| QA-005 | bug patterns, exploratory findings |
| QA-006 | environment-configs, test data, fixtures |

---

## Session Lifecycle Triggers

### Session Start

```
AUTOMATIC ACTIONS:
1. Load user-profile.json
2. Load system-config.json
3. Load terminology.json
4. Check for active project context
5. Initialize session state
6. Load any pending handoff memories
```

### Session End

```
AUTOMATIC ACTIONS:
1. Review working memory for promotable items
2. Create session summary episodic memory
3. Archive session state
4. Update user profile statistics
5. Run lightweight consolidation
```

---

## Agent Handoff Triggers

### Sending Agent

```
AUTOMATIC ACTIONS:
1. Package current working memory
2. List memories loaded during task
3. List memories created during task
4. Generate recommended memories for receiver
5. Create handoff summary
```

### Receiving Agent

```
AUTOMATIC ACTIONS:
1. Load all handoff memories
2. Load agent-specific memories
3. Apply working memory context
4. Acknowledge receipt
```

---

## Error Triggers

### On Error Occurrence

```
AUTOMATIC ACTIONS:
1. Capture error context
2. Query similar past errors
3. If similar error found:
   - Load resolution procedure
   - Apply fix
4. If no similar error:
   - Create new episodic memory
   - Tag for pattern detection
```

### On Error Resolution

```
AUTOMATIC ACTIONS:
1. Create procedural memory with fix
2. Link to error episodic memory
3. Update error frequency count
4. If frequent error: promote procedure
```

---

## Integration Points

### CLAUDE.md
- All triggers wired in "AUTOMATIC MEMORY OPERATIONS" section
- Trigger detection runs on EVERY message

### Agent Files
- Each agent has trigger-specific memory loading in "Memory Integration" section
- Agent-specific triggers defined

### Workflow Files
- Workflow triggers in "Memory Integration" section
- Per-phase memory operations

### Protocol Files
- Handoff protocol includes memory triggers
- All handoffs include memory context

---

## Trigger Priority

When multiple triggers match:

1. **Explicit commands** (highest): /remember, /recall
2. **Keyword triggers**: "remember that", "we decided"
3. **Context triggers**: Task type detection
4. **Agent triggers**: Agent-specific loading
5. **Session triggers** (lowest): Lifecycle events

Higher priority triggers take precedence.
