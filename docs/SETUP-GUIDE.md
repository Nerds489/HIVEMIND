# HIVEMIND Complete Setup Guide

This guide covers every aspect of installing, configuring, and troubleshooting HIVEMIND.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Install (Recommended)](#quick-install-recommended)
3. [Manual Installation](#manual-installation)
4. [Authentication Methods](#authentication-methods)
5. [Configuration Options](#configuration-options)
6. [Engine Presets](#engine-presets)
7. [Environment Variables](#environment-variables)
8. [Verifying Installation](#verifying-installation)
9. [Troubleshooting](#troubleshooting)
10. [Uninstallation](#uninstallation)

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Linux (Ubuntu 20.04+, Debian 11+, Fedora 35+, Arch) or macOS 12+ |
| RAM | 4 GB |
| Disk | 500 MB free space |
| Network | Internet connection for API calls |

### Software Dependencies

| Software | Version | Required | Notes |
|----------|---------|----------|-------|
| Node.js | 18.0+ | Yes | Installer will install if missing |
| npm | 8.0+ | Yes | Comes with Node.js |
| Bash | 4.0+ | Yes | Pre-installed on Linux/macOS |
| curl | Any | Yes | For downloading dependencies |
| jq | Any | Yes | For JSON processing in scripts |

### Accounts Required

| Service | Required For | Free Tier Available |
|---------|--------------|---------------------|
| OpenAI | Codex CLI (orchestrator) | Yes (with usage limits) |
| Anthropic | Claude CLI (agents) | Yes (with usage limits) |

---

## Quick Install (Recommended)

The fastest way to get HIVEMIND running:

```bash
# Clone the repository
git clone https://github.com/USERNAME/HIVEMIND.git
cd HIVEMIND

# Run the installer
./setup.sh
```

The installer will:
1. Check your system for dependencies
2. Install Node.js if missing
3. Install Codex CLI and Claude Code CLI
4. Walk you through authentication
5. Configure all directories and permissions
6. Add HIVEMIND to your PATH

**Time required**: 5-10 minutes (depending on internet speed)

---

## Manual Installation

If you prefer manual control, follow these steps:

### Step 1: Install Node.js

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Fedora/RHEL:**
```bash
sudo dnf install nodejs npm
```

**Arch Linux:**
```bash
sudo pacman -S nodejs npm
```

**macOS (with Homebrew):**
```bash
brew install node
```

**Verify installation:**
```bash
node --version  # Should show v18.x.x or higher
npm --version   # Should show 8.x.x or higher
```

### Step 2: Configure npm for User Installs

Avoid permission issues by configuring npm to use a user directory:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Install Codex CLI

```bash
npm install -g @openai/codex
```

**Verify:**
```bash
codex --version
```

### Step 4: Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

**Verify:**
```bash
claude --version
```

### Step 5: Set Up HIVEMIND

```bash
cd /path/to/HIVEMIND

# Make scripts executable
chmod +x hivemind setup.sh bootstrap.sh install.sh
chmod +x engines/*.sh core/*.sh bin/*

# Create required directories
mkdir -p memory/{global,long-term,short-term,episodic,sessions,agents,teams,projects}
mkdir -p workspace logs

# Initialize memory files
echo '{}' > memory/global/context.json
echo '{"entries":[]}' > memory/global/learnings.json
echo '{"version":"1.0","entries":[]}' > memory/long-term/learnings.json
```

### Step 6: Add to PATH

```bash
# Create symlink
mkdir -p ~/.local/bin
ln -sf "$(pwd)/hivemind" ~/.local/bin/hivemind
ln -sf "$(pwd)/bin/hm" ~/.local/bin/hm

# Add to PATH (if not already)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Authentication Methods

### Codex CLI (OpenAI)

You need an OpenAI account. A free ChatGPT account works for browser login.

#### Method 1: Browser OAuth (Recommended)

```bash
codex login --device-auth
```

1. A URL and code will be displayed
2. Open the URL in your browser
3. Log in with your OpenAI/ChatGPT account
4. Enter the code when prompted
5. Authorization completes automatically

**Pros**: No API key needed, uses your existing account
**Cons**: Token may expire, requiring re-login

#### Method 2: API Key

```bash
# Set environment variable
export OPENAI_API_KEY="sk-your-key-here"

# Or login with key
codex login --with-api-key
# Paste your key when prompted
```

**Get your API key**: https://platform.openai.com/api-keys

**Pros**: Persistent, no expiration
**Cons**: Requires API account with credits

#### Verify Codex Authentication

```bash
codex login status
# Should show: "Logged in as: your-email@example.com"
```

---

### Claude Code CLI (Anthropic)

You need an Anthropic account.

#### Method 1: Browser Token (Recommended)

```bash
claude setup-token
```

Follow the prompts to get a session token from claude.ai.

#### Method 2: API Key

```bash
# Set environment variable
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Get your API key**: https://console.anthropic.com/settings/keys

#### Verify Claude Authentication

```bash
# Test with a simple command
claude --print "Hello"

# Or check for credentials file
ls -la ~/.claude/.credentials.json
```

---

## Configuration Options

### Engine Configuration

Edit `config/engines.yaml`:

```yaml
# Which engine runs the HIVEMIND orchestrator
active:
  hivemind: codex    # Options: codex, claude
  agents: claude     # Options: codex, claude
```

### Change Engines via CLI

```bash
# Permanently change HIVEMIND engine
./hivemind --set-hivemind codex

# Permanently change agent engine
./hivemind --set-agents claude

# View current configuration
./hivemind --config
```

---

## Engine Presets

HIVEMIND includes four pre-configured engine combinations:

| Preset | HIVEMIND Engine | Agent Engine | Use Case |
|--------|-----------------|--------------|----------|
| `recommended` | Codex | Claude | Best balance of speed and quality |
| `full-codex` | Codex | Codex | All OpenAI, consistent behavior |
| `full-claude` | Claude | Claude | All Anthropic, maximum quality |
| `inverse` | Claude | Codex | Alternative configuration |

### Apply a Preset

```bash
# Apply preset for current session
./hivemind --preset full-claude

# Or edit config/engines.yaml directly
```

---

## Environment Variables

Create a `.env` file in the HIVEMIND directory:

```bash
cp .env.example .env
nano .env  # Edit with your values
```

### Available Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for Codex | If using API key auth |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | If using API key auth |
| `HIVEMIND_MODEL` | Override default model | No |
| `HIVEMIND_NO_LAUNCH` | Set to `1` to disable auto-launch | No |
| `HIVEMIND_ROOT` | Custom HIVEMIND location | No (auto-detected) |

### Example .env File

```bash
# Authentication (choose one method per engine)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Optional overrides
HIVEMIND_MODEL=claude-sonnet-4-20250514
```

---

## Verifying Installation

### Quick Test

```bash
./hivemind --status
```

Expected output:
```
═══════════════════════════════════════════
           HIVEMIND SYSTEM STATUS
═══════════════════════════════════════════

Engines:
  HIVEMIND: codex
  Agents:   claude
```

### Run Test Script

```bash
./test-installation.sh
```

### Manual Verification Checklist

```bash
# 1. Codex CLI works
codex --version

# 2. Claude CLI works
claude --version

# 3. HIVEMIND recognizes engines
./hivemind --config

# 4. Interactive mode starts
./hivemind
# Type 'exit' to quit

# 5. Direct task works
./hivemind "Hello, are you ready?"
```

---

## Troubleshooting

### Problem: "codex: command not found"

**Cause**: npm global bin not in PATH

**Solution**:
```bash
export PATH="$HOME/.npm-global/bin:$PATH"
# Add to ~/.bashrc for persistence
```

### Problem: "claude: command not found"

**Cause**: npm global bin not in PATH

**Solution**: Same as above

### Problem: "Codex is not authenticated"

**Cause**: No login or API key

**Solution**:
```bash
# Re-run authentication
codex login --device-auth
# Or set API key
export OPENAI_API_KEY="sk-your-key"
```

### Problem: "Claude is not authenticated"

**Cause**: No credentials

**Solution**:
```bash
# Re-run authentication
claude setup-token
# Or set API key
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### Problem: "Permission denied" when running scripts

**Cause**: Scripts not executable

**Solution**:
```bash
chmod +x hivemind setup.sh bootstrap.sh install.sh
chmod +x engines/*.sh core/*.sh bin/*
```

### Problem: "HIVEMIND_ROOT not set"

**Cause**: Running from wrong directory or symlink issue

**Solution**:
```bash
cd /path/to/HIVEMIND
./hivemind  # Run from HIVEMIND directory
```

### Problem: npm install fails with permission errors

**Cause**: npm trying to write to system directories

**Solution**:
```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH="$HOME/.npm-global/bin:$PATH"
npm install -g @openai/codex
```

### Problem: Node.js version too old

**Cause**: System has old Node.js

**Solution**:
```bash
# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Problem: YAML parse errors in config

**Cause**: Invalid YAML syntax

**Solution**:
```bash
# Validate YAML (install yq first: sudo apt install yq)
yq eval '.' config/engines.yaml

# Common issues:
# - Wrong indentation (use 2 spaces, not tabs)
# - Missing quotes around special characters
# - Incorrect nesting
```

### Getting Help

If none of these solutions work:

1. Run the diagnostic script:
```bash
./test-installation.sh
```

2. Check the logs:
```bash
ls -la logs/
cat logs/*.log
```

3. Open an issue on GitHub with:
   - Your OS and version
   - Node.js version (`node --version`)
   - The exact error message
   - Output of `./hivemind --config`

---

## Uninstallation

### Remove HIVEMIND Commands

```bash
rm -f ~/.local/bin/hivemind
rm -f ~/.local/bin/hm
```

### Remove CLI Tools

```bash
npm uninstall -g @openai/codex
npm uninstall -g @anthropic-ai/claude-code
```

### Remove Credentials

```bash
# Codex credentials
rm -rf ~/.codex

# Claude credentials
rm -rf ~/.claude
```

### Remove HIVEMIND Directory

```bash
rm -rf /path/to/HIVEMIND
```

### Clean Up Shell Config

Remove these lines from `~/.bashrc` or `~/.zshrc`:

```bash
# HIVEMIND PATH entries
export PATH="$HOME/.npm-global/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```

---

## Next Steps

After installation:

1. **Read the Quick Start**: See `QUICKSTART.md` for usage examples
2. **Explore Agents**: Check `agents/` directory for agent capabilities
3. **Try Workflows**: Look at `workflows/` for complex task pipelines
4. **Customize**: Edit `config/engines.yaml` to tune behavior

---

**HIVEMIND** - Route intelligently. Execute completely.
