# HIVEMIND Setup Guide: Codex as Orchestrator + Claude Code as Agents

This guide walks you through setting up HIVEMIND with **OpenAI Codex CLI** as the main orchestrator (the "brain") and **Claude Code CLI** as the sub-agents (the specialized workers).

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR TERMINAL                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CODEX CLI (HIVEMIND)                         │
│         Main Orchestrator - Receives tasks, routes them         │
│              Authenticated via OpenAI Account                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Spawns sub-agents
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CLAUDE CODE CLI (Agents)                       │
│         24 Specialized Agents running in background             │
│             Authenticated via Anthropic Account                 │
│                                                                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │   DEV   │ │   SEC   │ │   INF   │ │   QA    │              │
│  │ 6 agents│ │ 6 agents│ │ 6 agents│ │ 6 agents│              │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Install the CLI Tools

### 1.1 Install OpenAI Codex CLI

```bash
# Using npm (requires Node.js 18+)
npm install -g @openai/codex

# Verify installation
codex --version
```

**Alternative installation methods:**
```bash
# Using bun
bun install -g @openai/codex

# Using volta
volta install @openai/codex
```

### 1.2 Install Claude Code CLI

```bash
# Using npm
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

---

## Part 2: Authentication

### 2.1 Authenticate Codex CLI (OpenAI)

You have **two options** for authenticating Codex:

#### Option A: Browser-Based Login (Recommended)
```bash
codex login --device-auth
```
This will:
1. Display a URL and device code
2. Open your browser to login.openai.com
3. Ask you to enter the device code
4. Authenticate using your OpenAI account (ChatGPT account works)

#### Option B: API Key
```bash
# Set environment variable
export OPENAI_API_KEY="sk-your-api-key-here"

# Or login with key directly
codex login --with-api-key
# Then paste your API key when prompted
```

**Get your API key from:** https://platform.openai.com/api-keys

#### Verify Codex Authentication
```bash
codex login status
# Should show: "Logged in as: your-email@example.com"
```

### 2.2 Authenticate Claude Code CLI (Anthropic)

You have **three options** for authenticating Claude:

#### Option A: Browser-Based Token Setup (Recommended)
```bash
claude setup-token
```
This will guide you through getting a session token from claude.ai.

#### Option B: API Key via Environment
```bash
# Set one of these environment variables
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
# OR
export CLAUDE_API_KEY="sk-ant-your-key-here"
```

**Get your API key from:** https://console.anthropic.com/settings/keys

#### Option C: OAuth Login (if available)
```bash
claude login
```

#### Verify Claude Authentication
```bash
# Check if credentials exist
ls -la ~/.claude/.credentials.json

# Or test with a simple command
claude --print "Hello, are you working?"
```

---

## Part 3: Configure HIVEMIND

### 3.1 Navigate to HIVEMIND Directory

```bash
cd /path/to/HIVEMIND
```

### 3.2 Verify Engine Configuration

The configuration is already set correctly in `config/engines.yaml`:

```yaml
# Active configuration (this is what matters)
active:
  hivemind: codex           # Engine for HIVEMIND orchestrator
  agents: claude            # Engine for sub-agents
```

If you need to change this:
```bash
# Edit manually
nano config/engines.yaml

# OR use the CLI
./hivemind --set-hivemind codex
./hivemind --set-agents claude
```

### 3.3 Run the Installer

```bash
chmod +x install.sh
./install.sh
```

This will:
- Set up all required directories
- Initialize memory files
- Create symlinks in `~/.local/bin/`
- Add HIVEMIND to your PATH

---

## Part 4: First Run & Setup Verification

### 4.1 Interactive Setup Wizard

```bash
./hivemind --setup
```

This will show you:
```
Engine Setup

Detected:
  Codex:  /home/user/.local/bin/codex  (ready)
  Claude: /home/user/.local/bin/claude  (ready)

Choose an action:
  1) Codex: login via browser (device auth)
  2) Codex: login via API key
  3) Claude: setup-token (browser/token)
  q) Quit
```

### 4.2 Verify Configuration

```bash
./hivemind --config
```

Should output:
```
═══════════════════════════════════════════
         HIVEMIND CONFIGURATION            
═══════════════════════════════════════════

Engines:
  HIVEMIND runs on:  codex
  Agents run on:     claude
  Model override:    (default)

Available Presets:
  recommended   - codex + claude (default)
  full-codex    - codex + codex
  full-claude   - claude + claude
  inverse       - claude + codex
```

### 4.3 Check System Status

```bash
./hivemind --status
```

---

## Part 5: Using HIVEMIND

### 5.1 Interactive Mode

```bash
./hivemind
# or just
hm
```

You'll see:
```
HIVEMIND ready. All teams standing by.
Type your request, 'setup' for auth, 'config' for settings, or 'exit' to quit.

HIVEMIND>
```

### 5.2 Direct Task Execution

```bash
./hivemind "Design a REST API for user authentication"
```

### 5.3 Example Commands

```bash
# Architecture task - routes to DEV-001 (Architect)
./hivemind "Design a microservices architecture for an e-commerce platform"

# Security task - routes to SEC-002 (Penetration Tester)
./hivemind "Perform security assessment on my Node.js API"

# Infrastructure task - routes to INF-001 (Infrastructure Architect)
./hivemind "Design Kubernetes deployment for high availability"

# Full SDLC workflow
./hivemind "Full SDLC for implementing OAuth authentication"
```

---

## Part 6: Environment Variables Reference

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# HIVEMIND Root (auto-detected, but can be set manually)
export HIVEMIND_ROOT="/path/to/HIVEMIND"

# OpenAI Authentication (Option B)
export OPENAI_API_KEY="sk-your-openai-key"

# Anthropic Authentication (Option B)
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"

# Optional: Override default model
export HIVEMIND_MODEL="claude-sonnet-4-20250514"

# Optional: Disable auto-launching terminals on install
export HIVEMIND_NO_LAUNCH=1
```

---

## Part 7: How It Actually Works

When you run a task:

1. **HIVEMIND (Codex)** receives your request
2. It analyzes the task and determines what agents are needed
3. It calls `bin/spawn-agent <agent-type> "<task>"` for each needed agent
4. **spawn-agent** uses `run_engine "claude"` to spawn Claude Code processes
5. Each Claude agent runs with a specialized system prompt from `agents/`
6. Results are saved to `workspace/<agent>/<task-id>/result.md`
7. **HIVEMIND** reads and synthesizes results into one unified response

### The Flow in Code

```
./hivemind "task"
    │
    ├── build_hivemind_prompt() → loads IDENTITY.md + memory context
    │
    ├── run_engine "codex" "$prompt" "$task"
    │       │
    │       └── Codex receives: system prompt + task
    │           Codex can execute: bin/spawn-agent architect "subtask"
    │               │
    │               └── spawn-agent runs:
    │                   run_engine "claude" "$agent_prompt" "$subtask" "print"
    │                       │
    │                       └── Claude agent executes task
    │                           Writes to: workspace/architect/<id>/result.md
    │
    └── Codex reads results, synthesizes, outputs to user
```

---

## Part 8: Troubleshooting

### Issue: "codex not found"
```bash
# Check if installed
npm list -g @openai/codex

# Reinstall
npm install -g @openai/codex

# Check PATH
echo $PATH | tr ':' '\n' | grep -E "(npm|node|local)"
```

### Issue: "claude not found"
```bash
# Check if installed
npm list -g @anthropic-ai/claude-code

# Reinstall
npm install -g @anthropic-ai/claude-code
```

### Issue: "Codex is not authenticated"
```bash
# Re-authenticate
codex login --device-auth
# OR
export OPENAI_API_KEY="sk-your-key"
```

### Issue: "Claude is not authenticated"
```bash
# Re-authenticate
claude setup-token
# OR
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### Issue: Agents not spawning
```bash
# Check if agent engine is configured
./hivemind --config

# Test spawn manually
./bin/spawn-agent architect "test task"

# Check workspace for output
ls -la workspace/architect/
```

---

## Part 9: Advanced Configuration

### Switch to Full Codex Mode (both orchestrator and agents use Codex)
```bash
./hivemind --preset full-codex
```

### Switch to Full Claude Mode
```bash
./hivemind --preset full-claude
```

### Use Specific Model
```bash
export HIVEMIND_MODEL="gpt-4o"
./hivemind "your task"
```

### Enable Auto-Orchestration for Direct Tasks
```bash
./hivemind --auto "complex multi-agent task"
```

---

## Part 10: File Locations Summary

```
HIVEMIND/
├── hivemind              # Main entry point
├── install.sh            # Installation script
├── config/
│   ├── engines.yaml      # Engine configuration (EDIT THIS)
│   └── hivemind.yaml     # System configuration
├── engines/
│   ├── engine.sh         # Engine abstraction layer
│   ├── codex.sh          # Codex adapter
│   └── claude-code.sh    # Claude adapter
├── bin/
│   ├── spawn-agent       # Spawns sub-agents
│   ├── orchestrate       # Multi-agent orchestration
│   ├── memory-ops        # Memory operations
│   └── hm                # Shorthand command
├── agents/               # Agent definitions (system prompts)
├── memory/               # Persistent memory storage
└── workspace/            # Agent output directory
```

---

## Quick Start Checklist

- [ ] Install Codex CLI: `npm install -g @openai/codex`
- [ ] Install Claude CLI: `npm install -g @anthropic-ai/claude-code`
- [ ] Authenticate Codex: `codex login --device-auth`
- [ ] Authenticate Claude: `claude setup-token`
- [ ] Run installer: `./install.sh`
- [ ] Verify setup: `./hivemind --setup`
- [ ] Test run: `./hivemind "Hello, are you ready?"`

---

*HIVEMIND - Neural Multi-Agent Orchestration System*
*Codex as brain. Claude as muscle.*
