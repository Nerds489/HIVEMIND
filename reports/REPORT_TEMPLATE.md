# HEAD_CODEX Report Template

## Standard Report Format

```
╔══════════════════════════════════════════════════════════════╗
║                    HIVEMIND EXECUTION REPORT                  ║
╠══════════════════════════════════════════════════════════════╣
║ Task: {TASK_SUMMARY}                                          ║
║ Status: {STATUS}                                              ║
║ Duration: {DURATION}                                          ║
╠══════════════════════════════════════════════════════════════╣
║ AGENTS ENGAGED:                                               ║
║ • {AGENT_ID} {AGENT_ROLE} ............ {FINAL_STATUS}         ║
╠══════════════════════════════════════════════════════════════╣
║ QUALITY GATES:                                                ║
║ • G1-DESIGN: {GATE_STATUS}                                    ║
║ • G2-SECURITY: {GATE_STATUS}                                  ║
║ • G3-CODE: {GATE_STATUS}                                      ║
║ • G4-TEST: {GATE_STATUS}                                      ║
║ • G5-DEPLOY: {GATE_STATUS}                                    ║
╠══════════════════════════════════════════════════════════════╣
║ DELIVERABLES:                                                 ║
║ • {DELIVERABLE_1}                                             ║
║ • {DELIVERABLE_2}                                             ║
╠══════════════════════════════════════════════════════════════╣
║ SUMMARY:                                                      ║
║ {SUMMARY_TEXT}                                                ║
╚══════════════════════════════════════════════════════════════╝
```

## Status Values

| Status | Description |
|--------|-------------|
| COMPLETE | All agents finished successfully |
| IN_PROGRESS | Execution ongoing |
| BLOCKED | Blocked by error or gate |
| CANCELLED | User cancelled |

## Gate Status Values

| Status | Description |
|--------|-------------|
| PASSED | Gate requirements met |
| BLOCKED | Gate requirements not met |
| PENDING | Awaiting evaluation |
| SKIPPED | Gate not applicable |

## Compact Report (For Simple Tasks)

```
╔═══════════════════════════════════════════╗
║ HIVEMIND: {TASK} - {STATUS}               ║
╠═══════════════════════════════════════════╣
║ Agents: {COUNT} | Gates: {PASSED}/{TOTAL} ║
╚═══════════════════════════════════════════╝
```

## Error Report

```
╔══════════════════════════════════════════════════════════════╗
║                    HIVEMIND ERROR REPORT                      ║
╠══════════════════════════════════════════════════════════════╣
║ Task: {TASK_SUMMARY}                                          ║
║ Status: BLOCKED                                               ║
╠══════════════════════════════════════════════════════════════╣
║ ERROR:                                                        ║
║ Agent: {AGENT_ID}                                             ║
║ Issue: {ERROR_DESCRIPTION}                                    ║
║ Gate: {BLOCKED_GATE}                                          ║
╠══════════════════════════════════════════════════════════════╣
║ RECOMMENDATION:                                               ║
║ {RECOMMENDATION}                                              ║
╚══════════════════════════════════════════════════════════════╝
```
