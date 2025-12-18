# HIVEMIND

Engine-agnostic orchestration for specialist LLM runs (Codex CLI / Claude Code).  
Includes a working CLI (`./hivemind`), 24 specialist prompt profiles, disk-backed memory, and playbooks for common workflows.

## Start Here

- `BOOTSTRAP.md` — single entry point and load order
- `QUICKSTART.md` — command examples and usage patterns
- `HIVEMIND.md` — full documentation
- `INDEX.md` — complete file map

## Requirements

- `bash`
- `jq` (required for `bin/orchestrate` and `bin/memory-ops`)
- At least one engine installed and authenticated: `codex` and/or `claude`

## Install

```bash
cd /path/to/HIVEMIND
./install.sh
```

What `./install.sh` does:
- Makes scripts executable and initializes memory files (non-destructive)
- Installs `hivemind` and `hm` into `~/.local/bin`
- Ensures `~/.local/bin` is on your `PATH`

Disable GUI terminal auto-launch:
```bash
./install.sh --no-launch
```

## Quickstart (CLI)

Verify:
```bash
./hivemind --help
./hivemind --config
./bin/test-hivemind
```

Run (interactive):
```bash
./hivemind
```

Run (one-shot task):
```bash
./hivemind "Design a secure authentication system"
```

Run multi-specialist orchestration:
```bash
./bin/orchestrate "Audit our auth flow" security-architect reviewer qa-architect
```

Use memory tooling:
```bash
./bin/memory-ops store fact "We use snake_case for Python" python style
./bin/memory-ops recall "snake_case"
```

## Engine Configuration

HIVEMIND can run the orchestrator and specialists on different engines. The active selection lives in `config/engines.yaml`.

Show current configuration:
```bash
./hivemind --config
```

Guided setup (recommended for first-time auth/config):
```bash
./hivemind --setup
```

## Specialist Types

Use these identifiers with `bin/spawn-agent` / `bin/orchestrate`:

| Type | Focus |
|---|---|
| `architect` | system and API design |
| `backend` | services, APIs, data handling |
| `frontend` | UI/UX, components, accessibility |
| `reviewer` | code review, quality and safety checks |
| `writer` | documentation and guides |
| `devops` | CI/CD, release, automation |
| `security-architect` | security design, threat modeling |
| `pentester` | vulnerability assessment (defensive intent) |
| `malware` | reverse engineering and IOCs |
| `wireless` | WiFi/Bluetooth/RF security |
| `compliance` | audit and compliance mapping |
| `incident` | incident response and forensics workflow |
| `infra-architect` | cloud and infrastructure architecture |
| `sysadmin` | server hardening and ops |
| `network` | DNS, firewalls, routing, VPNs |
| `dba` | database design and performance |
| `sre` | reliability, monitoring, SLOs |
| `automation` | scripting, IaC, repeatability |
| `qa-architect` | test strategy and quality gates |
| `test-auto` | automated testing frameworks |
| `performance` | load and stress testing |
| `security-test` | SAST/DAST and security automation |
| `manual-qa` | exploratory testing and UAT |
| `test-data` | fixtures, test data management |

## Project Layout (Short)

For the full tree, see `INDEX.md`. Key directories:

- `bin/` — runnable utilities (orchestrate, memory ops, smoke tests)
- `agents/` — specialist prompt definitions
- `config/` — engine selection, routing, settings
- `memory/` — persistent memory store
- `workflows/` — multi-step playbooks
- `protocols/` and `templates/` — standards and output formats

## Using In Another Project

Options:
- Reference this folder by path in your prompt/tooling
- Copy the docs/policy layer into your project
- Symlink the whole folder into your repo

Example symlink:
```bash
ln -s /path/to/HIVEMIND /path/to/your/project/HIVEMIND
```

For deeper docs, start at `BOOTSTRAP.md` and `QUICKSTART.md`.
