# HIVEMIND Upgrade Package - Implementation Guide

## Package Contents

```
hivemind-upgrade/
├── memory/agents/          # 20 missing agent memory profiles
│   ├── DEV-002/_memory.json
│   ├── DEV-003/_memory.json
│   ├── DEV-004/_memory.json
│   ├── DEV-005/_memory.json
│   ├── DEV-006/_memory.json
│   ├── SEC-002/_memory.json
│   ├── SEC-003/_memory.json
│   ├── SEC-004/_memory.json
│   ├── SEC-005/_memory.json
│   ├── SEC-006/_memory.json
│   ├── INF-002/_memory.json
│   ├── INF-003/_memory.json
│   ├── INF-004/_memory.json
│   ├── INF-005/_memory.json
│   ├── INF-006/_memory.json
│   ├── QA-002/_memory.json
│   ├── QA-003/_memory.json
│   ├── QA-004/_memory.json
│   ├── QA-005/_memory.json
│   └── QA-006/_memory.json
├── commands/               # New slash commands
│   ├── debug.md
│   ├── status.md
│   └── recall.md
├── scripts/
│   └── health-check.sh    # Diagnostic script
├── docs/
│   ├── QUICK-REFERENCE.md # Cheat sheet
│   └── IMPLEMENTATION.md  # This file
└── extras/
    └── example-prompts.md # Usage examples
```

---

## Installation Steps

### Step 1: Navigate to HIVEMIND

```bash
cd /path/to/HIVEMIND
```

### Step 2: Copy Memory Profiles

```bash
# Copy all agent memory profiles
cp -r /path/to/hivemind-upgrade/memory/agents/* memory/agents/
```

### Step 3: Copy New Commands

```bash
# Copy new slash commands
cp /path/to/hivemind-upgrade/commands/*.md .claude/commands/
```

### Step 4: Copy Scripts

```bash
# Copy health check script
cp /path/to/hivemind-upgrade/scripts/health-check.sh scripts/
chmod +x scripts/health-check.sh
```

### Step 5: Copy Documentation

```bash
# Copy docs
cp /path/to/hivemind-upgrade/docs/*.md docs/
```

### Step 6: Verify Installation

```bash
./scripts/health-check.sh --verbose
```

---

## One-Liner Installation

```bash
# From HIVEMIND root directory
unzip hivemind-upgrade.zip && \
cp -r hivemind-upgrade/memory/agents/* memory/agents/ && \
cp hivemind-upgrade/commands/*.md .claude/commands/ && \
cp hivemind-upgrade/scripts/* scripts/ && \
chmod +x scripts/*.sh && \
cp hivemind-upgrade/docs/*.md docs/ && \
rm -rf hivemind-upgrade && \
./scripts/health-check.sh
```

---

## What Gets Added

### 1. Complete Agent Memory Profiles (20 files)

Each profile contains:
- **expertise**: Primary and secondary skills, tools
- **coding_patterns**: Preferred approaches and standards
- **learned_preferences**: User-specific customizations
- **collaboration**: Team relationships, handoff triggers
- **quality_gates**: Standards the agent enforces
- **common_tasks**: Typical work items

### 2. New Slash Commands (3 files)

| Command | Purpose |
|---------|---------|
| `/debug` | Troubleshoot routing, memory, engine issues |
| `/status` | Show system status and agent activity |
| `/recall` | Query the memory system |

### 3. Health Check Script

Run diagnostics:
```bash
./scripts/health-check.sh           # Quick check
./scripts/health-check.sh --verbose # Detailed output
./scripts/health-check.sh --fix     # Auto-repair issues
```

Checks:
- Directory structure
- All 24 agents present
- Memory profiles complete
- Configuration valid
- Engine availability
- Memory system health

### 4. Quick Reference Card

One-page cheat sheet with:
- All commands
- All agents with roles
- Common workflows
- Troubleshooting tips

---

## Post-Installation Verification

### Check Agent Count
```bash
ls memory/agents/*/\_memory.json | wc -l
# Should output: 24
```

### Check Commands
```bash
ls .claude/commands/*.md | wc -l
# Should include: debug.md, status.md, recall.md
```

### Run Health Check
```bash
./scripts/health-check.sh
# Should show all green checkmarks
```

### Test HIVEMIND
```bash
claude
# In Claude: Say "HIVEMIND"
# Should respond: "HIVEMIND active."
```

---

## Customization

### Add Agent Expertise

Edit `memory/agents/[AGENT-ID]/_memory.json`:

```json
{
  "expertise": {
    "primary": [
      "Your custom skill 1",
      "Your custom skill 2"
    ]
  }
}
```

### Add User Preferences

Edit `memory/global/user-profile.json`:

```json
{
  "preferences": {
    "coding_style": "Your style",
    "tech_stack": ["Your", "Stack"],
    "naming_conventions": "Your conventions"
  }
}
```

### Add Team Knowledge

Create files in `memory/teams/[team]/`:

```json
{
  "topic": "Your topic",
  "knowledge": "What the team knows",
  "learned_from": "How it was learned"
}
```

---

## Troubleshooting

### "Command not found"

Commands must be in `.claude/commands/`:
```bash
cp commands/*.md .claude/commands/
```

### "Memory not loading"

Check permissions:
```bash
chmod -R 755 memory/
```

### "Agent routing wrong"

Update `config/routing.json` with correct keywords.

### "Health check failing"

Run with fix mode:
```bash
./scripts/health-check.sh --fix
```

---

## What's Next

After installation, HIVEMIND has:
- ✅ 24 complete agent profiles
- ✅ Full memory system
- ✅ Extended command set
- ✅ Diagnostic tooling
- ✅ Complete documentation

The system is production-ready for:
- Full-stack development
- Security assessments
- Infrastructure automation
- Quality assurance workflows

---

*HIVEMIND Upgrade Package v1.0*
