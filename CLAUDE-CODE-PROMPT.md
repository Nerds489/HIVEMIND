# HIVEMIND Setup Prompt for Claude Code

Copy and paste this entire prompt into Claude Code CLI:

---

```
I need you to set up HIVEMIND - a multi-agent orchestration system that uses Codex as the main orchestrator and Claude Code as the sub-agents.

## Files Location
The new setup scripts are in: ~/Downloads/NEW-VOIDWAVESTUFF-GOESTO-VOIDWAVE/

This folder contains:
- setup.sh - Main installer script
- bootstrap.sh - Simple wrapper
- HIVEMIND-SETUP-GUIDE.md - Documentation

## My HIVEMIND Project Location
My HIVEMIND project is at: ~/Desktop/HIVEMIND/

## What I Need You To Do

1. Copy the new scripts from ~/Downloads/NEW-VOIDWAVESTUFF-GOESTO-VOIDWAVE/ into ~/Desktop/HIVEMIND/

2. Make the scripts executable:
   - chmod +x setup.sh
   - chmod +x bootstrap.sh

3. Run the setup script and walk me through:
   - Installing Codex CLI (if not installed)
   - Installing Claude Code CLI (if not installed)
   - Authenticating Codex (I'll choose browser or API key)
   - Authenticating Claude (I'll choose browser or API key)

4. Verify the installation works by running:
   - ./hivemind --config
   - ./hivemind --status

## Architecture Reminder
- Codex (OpenAI) = HIVEMIND orchestrator (the brain)
- Claude (Anthropic) = 24 sub-agents (the workers)

Start by copying the files and making them executable, then run ./setup.sh
```

---

## Alternative: Shorter Version

```
Copy setup.sh and bootstrap.sh from ~/Downloads/NEW-VOIDWAVESTUFF-GOESTO-VOIDWAVE/ to ~/Desktop/HIVEMIND/, make them executable, then run ./setup.sh to install and authenticate both Codex CLI and Claude Code CLI for HIVEMIND.
```

---

## If You Want Claude Code to Do It All Automatically

```
cd ~/Desktop/HIVEMIND && cp ~/Downloads/NEW-VOIDWAVESTUFF-GOESTO-VOIDWAVE/setup.sh ~/Downloads/NEW-VOIDWAVESTUFF-GOESTO-VOIDWAVE/bootstrap.sh . && chmod +x setup.sh bootstrap.sh && ./setup.sh
```
