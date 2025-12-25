# HIVEMIND v2.0 UPGRADE GUIDE

```
██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗ 
██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 
                  v2.0 MINIMAL OUTPUT EDITION
```

---

## What's New in v2.0

### Core Changes

| Feature | v1.x | v2.0 |
|---------|------|------|
| Agent Output | Verbose explanations | **2-4 words max** |
| Orchestrator | COORDINATOR | **HEAD_CODEX** |
| Reporting | Per-agent | **Consolidated final report** |
| Internal Comms | Visible | **Invisible** |
| User View | Everything | **Status + Report only** |

### Key Features

1. **Minimal Output Protocol** - All agents report in 2-4 words
2. **HEAD_CODEX** - Master orchestrator with consolidated reporting
3. **Invisible Orchestration** - Internal handoffs hidden from user
4. **Consolidated Reports** - One final report per task
5. **Quality Gates** - Visible gate status updates

---

## Quick Install

### Option 1: Automated Installer

```bash
# Extract upgrade package
unzip hivemind-upgrade-v2.0.zip
cd hivemind-upgrade-v2.0

# Run installer (default: ~/HIVEMIND)
./install.sh

# Or specify custom location
./install.sh /path/to/HIVEMIND
```

### Option 2: Manual Install

```bash
# Backup existing
cp -r ~/HIVEMIND ~/HIVEMIND.backup

# Extract and copy
unzip hivemind-upgrade-v2.0.zip
cp -r hivemind-upgrade-v2.0/* ~/HIVEMIND/

# Set permissions
chmod +x ~/HIVEMIND/bin/*
```

---

## Upgrade Steps

### Step 1: Backup

```bash
# Create timestamped backup
cp -r ~/HIVEMIND ~/HIVEMIND.backup.$(date +%Y%m%d)
```

### Step 2: Verify Package

```bash
cd hivemind-upgrade-v2.0
cat VERSION  # Should show 2.0.0
```

### Step 3: Run Installer

```bash
./install.sh ~/HIVEMIND
```

### Step 4: Verify Installation

```bash
~/HIVEMIND/bin/hivemind --version
# Output: HIVEMIND v2.0.0 (MINIMAL_OUTPUT)

~/HIVEMIND/bin/hivemind --status
```

### Step 5: Test

```bash
~/HIVEMIND/bin/hivemind "Test task"
```

---

## File Structure

```
HIVEMIND/
├── VERSION                      # 2.0.0
├── bin/
│   └── hivemind                 # Main CLI
├── core/
│   ├── HEAD_CODEX.md           # Master orchestrator
│   └── COORDINATOR.md          # Routing logic
├── config/
│   ├── settings.json           # System config
│   └── agents.json             # Agent registry
├── agents/
│   ├── dev/DEV_TEAM.md         # Development agents
│   ├── sec/SEC_TEAM.md         # Security agents
│   ├── infra/INF_TEAM.md       # Infrastructure agents
│   └── qa/QA_TEAM.md           # QA agents
├── protocols/
│   └── MINIMAL_OUTPUT.md       # Output protocol
├── reports/                     # Generated reports
├── memory/                      # Persistent memory
├── docs/
│   └── UPGRADE_GUIDE.md        # This file
└── .claude/commands/           # Slash commands
```

---

## Minimal Output Protocol

### Before (v1.x)
```
[DEV-001] I am now analyzing the requirements for your authentication system. 
First, I'll look at the OAuth 2.0 specification and determine the best flow 
for your use case. Based on my analysis of modern authentication patterns...
```

### After (v2.0)
```
[DEV-001] Analyzing requirements
```

### Rules

| Rule | Description |
|------|-------------|
| MAX_WORDS | 4 words maximum |
| FORMAT | `[AGENT_ID] status` |
| VERBS | Present tense, action-focused |
| NO_EXPLAIN | Never explain, just state |

### Valid Examples
```
[DEV-001] Designing architecture
[SEC-002] Scanning endpoints
[QA-003] Running tests
[INF-005] Deploying services
[DEV-004] Reviewing code
[SEC-006] Investigating incident
```

### Invalid Examples
```
[DEV-001] I am now starting to analyze the architecture requirements...
[SEC-002] Beginning the process of scanning all web application endpoints...
```

---

## HEAD_CODEX Reports

### Report Structure

```
╔══════════════════════════════════════════════════════════════╗
║                    HIVEMIND EXECUTION REPORT                  ║
╠══════════════════════════════════════════════════════════════╣
║ Task: [Task Summary]                                          ║
║ Status: COMPLETE | IN_PROGRESS | BLOCKED                      ║
╠══════════════════════════════════════════════════════════════╣
║ AGENTS ENGAGED:                                               ║
║ • DEV-001 Architect ............ Complete                     ║
║ • SEC-002 Penetration Tester ... Complete                     ║
║ • QA-002 Test Automation ....... Complete                     ║
╠══════════════════════════════════════════════════════════════╣
║ DELIVERABLES:                                                 ║
║ • [Output 1]                                                  ║
║ • [Output 2]                                                  ║
╠══════════════════════════════════════════════════════════════╣
║ SUMMARY:                                                      ║
║ [Brief summary of what was accomplished]                      ║
╚══════════════════════════════════════════════════════════════╝
```

### When Reports Generate

- All agents complete successfully
- Blocking error occurs
- User requests `/report`
- Task timeout

---

## Quality Gates

### Gate Definitions

| Gate | Name | Required Agent |
|------|------|----------------|
| G1 | Design Gate | DEV-001 |
| G2 | Security Gate | SEC-001/002 |
| G3 | Code Review Gate | DEV-004 |
| G4 | Testing Gate | QA-001/002 |
| G5 | Deployment Gate | INF-005 |

### Gate Output
```
[GATE] G1-DESIGN: PASSED
[GATE] G2-SECURITY: PASSED
[GATE] G3-CODE: PASSED
[GATE] G4-TEST: BLOCKED - Test failures
```

---

## CLI Usage

### Basic Commands

```bash
# Interactive mode
hivemind

# Direct task
hivemind "Design a REST API"

# Shorthand
hm "Design a REST API"
```

### Options

```bash
hivemind --help      # Show help
hivemind --version   # Show version
hivemind --status    # Show status
hivemind --agents    # List agents
hivemind --config    # Show config
```

### Team Commands

```bash
hivemind /dev "Build authentication"
hivemind /sec "Security assessment"
hivemind /infra "Deploy to production"
hivemind /qa "Run test suite"
```

---

## Configuration

### settings.json Key Changes

```json
{
  "version": "2.0.0",
  "output_rules": {
    "max_words_per_status": 4,
    "enforce_truncation": true,
    "show_agent_reasoning": false,
    "final_report_only": true
  },
  "head_codex": {
    "generate_report_on_complete": true
  }
}
```

### Agent Registry Changes

Each agent now has `status_templates`:

```json
{
  "id": "DEV-001",
  "status_templates": [
    "Designing architecture",
    "Creating ADR",
    "Review complete",
    "Architecture ready"
  ]
}
```

---

## Migration Notes

### Breaking Changes

1. **Output Format** - Agents no longer produce verbose output
2. **Report Structure** - Reports are now consolidated
3. **Orchestrator** - HEAD_CODEX replaces verbose COORDINATOR
4. **Handoffs** - Internal handoffs are invisible

### Compatibility

- v1.x agent definitions still work (output will be truncated)
- v1.x workflows are compatible
- v1.x slash commands work unchanged

### Recommended Actions

1. Update any custom agent definitions to include `status_templates`
2. Review any automation that parses agent output
3. Update documentation references

---

## Troubleshooting

### Issue: Verbose Output Still Appearing

**Cause**: Old agent definition not updated

**Fix**: 
```bash
# Replace old agent definitions
cp -r hivemind-upgrade-v2.0/agents/* ~/HIVEMIND/agents/
```

### Issue: HEAD_CODEX Not Generating Reports

**Cause**: Missing core files

**Fix**:
```bash
cp -r hivemind-upgrade-v2.0/core/* ~/HIVEMIND/core/
```

### Issue: CLI Not Found

**Cause**: PATH not configured

**Fix**:
```bash
export PATH="$PATH:$HOME/.local/bin"
# Add to ~/.bashrc or ~/.zshrc
```

### Issue: Permission Denied

**Fix**:
```bash
chmod +x ~/HIVEMIND/bin/hivemind
```

---

## Rollback

If you need to rollback to v1.x:

```bash
# Remove v2.0
rm -rf ~/HIVEMIND

# Restore backup
mv ~/HIVEMIND.backup ~/HIVEMIND
```

---

## Support

### Files
- `UPGRADE_GUIDE.md` - This file
- `core/HEAD_CODEX.md` - Orchestrator documentation
- `protocols/MINIMAL_OUTPUT.md` - Output protocol

### GitHub
- Issues: Report bugs or request features
- Discussions: Ask questions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024 | Minimal Output Edition |
| 1.x | 2024 | Original release |

---

*HIVEMIND v2.0 — Say More With Less*
