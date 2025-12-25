# HIVEMIND v2.0 Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                   HIVEMIND v2.0 QUICK REFERENCE                 │
├─────────────────────────────────────────────────────────────────┤
│ COMMANDS                                                        │
│   hivemind "task"        Direct execution                       │
│   hivemind               Interactive mode                       │
│   hm "task"              Shorthand                              │
│   hivemind --status      System status                          │
│   hivemind --agents      List agents                            │
├─────────────────────────────────────────────────────────────────┤
│ TEAM COMMANDS                                                   │
│   /dev [task]            Development team                       │
│   /sec [task]            Security team                          │
│   /infra [task]          Infrastructure team                    │
│   /qa [task]             QA team                                │
├─────────────────────────────────────────────────────────────────┤
│ OUTPUT PROTOCOL                                                 │
│   Format: [AGENT_ID] 2-4 word status                            │
│   Example: [DEV-001] Designing architecture                     │
├─────────────────────────────────────────────────────────────────┤
│ AGENTS (24 Total)                                               │
│   DEV: 001-006 (Architect, Backend, Frontend, Reviewer...)      │
│   SEC: 001-006 (SecArch, Pentester, Malware, Wireless...)       │
│   INF: 001-006 (InfraArch, SysAdmin, Network, DBA, SRE...)      │
│   QA:  001-006 (QAArch, Automation, Perf, Security...)          │
├─────────────────────────────────────────────────────────────────┤
│ QUALITY GATES                                                   │
│   G1-DESIGN    Design approval (DEV-001)                        │
│   G2-SECURITY  Security clearance (SEC-001/002)                 │
│   G3-CODE      Code review (DEV-004)                            │
│   G4-TEST      Test pass (QA-001/002)                           │
│   G5-DEPLOY    Deploy ready (INF-005)                           │
├─────────────────────────────────────────────────────────────────┤
│ STATUS VALUES                                                   │
│   Starting:  Starting, Initializing, Beginning, Creating        │
│   Working:   Processing, Analyzing, Building, Scanning          │
│   Complete:  Complete, Finished, Done, Ready, Approved          │
│   Blocked:   Blocked, Waiting, Pending, Failed, Error           │
└─────────────────────────────────────────────────────────────────┘
```

## One-Liners

```bash
# Install
./install.sh

# Run
hivemind "Design a REST API"

# Teams
hivemind /dev "Build auth"
hivemind /sec "Security scan"

# Status
hivemind --status
```

## Key Files

| File | Purpose |
|------|---------|
| `core/HEAD_CODEX.md` | Master orchestrator |
| `core/COORDINATOR.md` | Routing logic |
| `protocols/MINIMAL_OUTPUT.md` | Output rules |
| `config/agents.json` | Agent registry |
| `config/settings.json` | System config |
