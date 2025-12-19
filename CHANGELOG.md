# Changelog

All notable changes to HIVEMIND will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Web UI dashboard for monitoring agents
- Custom agent creation wizard
- Memory export/import functionality
- Docker containerization support

---

## [1.0.0] - 2024-12-19

### Added

#### Core System
- Multi-agent orchestration system with 24 specialized AI agents
- Dual-engine architecture: Codex (orchestrator) + Claude (agents)
- Intelligent task routing based on keywords and context
- Unified voice output - all agents speak as one coherent response

#### Agent Teams (24 Total)
- **Development Team** (6 agents): Architect, Backend Developer, Frontend Developer, Code Reviewer, Technical Writer, DevOps Liaison
- **Security Team** (6 agents): Security Architect, Penetration Tester, Malware Analyst, Wireless Security Expert, Compliance Auditor, Incident Responder
- **Infrastructure Team** (6 agents): Infrastructure Architect, Systems Administrator, Network Engineer, Database Administrator, Site Reliability Engineer, Automation Engineer
- **QA Team** (6 agents): QA Architect, Test Automation Engineer, Performance Tester, Security Tester, Manual QA Tester, Test Data Manager

#### Installation & Setup
- `setup.sh` - Complete one-command installer
- `bootstrap.sh` - Quick bootstrap wrapper
- Automatic Node.js installation (if needed)
- Automatic Codex CLI installation
- Automatic Claude Code CLI installation
- Interactive authentication wizard (browser OAuth or API key)
- Cross-platform support (Linux, macOS)

#### Configuration
- `config/engines.yaml` - Engine configuration with presets
- `config/hivemind.yaml` - System-wide settings
- `config/routing.yaml` - Task routing rules
- `config/agents.yaml` - Agent definitions
- Environment variable support via `.env` files
- Four engine presets: recommended, full-codex, full-claude, inverse

#### Memory System
- Persistent long-term memory (learnings, decisions, preferences)
- Short-term working memory for sessions
- Episodic memory for event tracking
- Per-agent memory isolation
- Team-shared memory pools
- Automatic memory triggers ("remember that...", "we decided...")

#### CLI Interface
- Interactive mode with REPL
- Direct task execution mode
- `--config` flag for viewing configuration
- `--status` flag for system status
- `--setup` flag for authentication wizard
- `--preset` flag for quick engine switching
- `hm` shorthand command

#### Workflows
- Full SDLC workflow
- Security assessment workflow
- Incident response workflow
- Code review workflow
- Infrastructure deployment workflow
- Compliance audit workflow

#### Documentation
- Comprehensive README with quick start
- Detailed setup guide
- Agent reference documentation
- Workflow documentation
- Template library for outputs

### Security
- No credentials stored in repository
- `.gitignore` configured for security
- `.env.example` template provided
- API keys stored locally only
- Session data excluded from version control

---

## [0.1.0] - 2024-12-17

### Added
- Initial project structure
- Basic agent definitions
- Proof of concept orchestration
- Memory system prototype

---

## Version History Notes

### Versioning Scheme
- **Major (X.0.0)**: Breaking changes, major architecture updates
- **Minor (0.X.0)**: New features, new agents, new workflows
- **Patch (0.0.X)**: Bug fixes, documentation updates, minor improvements

### Upgrade Guide
When upgrading between versions:
1. Backup your `memory/` directory
2. Backup your `.env` file
3. Pull the new version
4. Run `./setup.sh` to update dependencies
5. Restore your `.env` file
6. Memory files are forward-compatible

---

[Unreleased]: https://github.com/USERNAME/HIVEMIND/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/USERNAME/HIVEMIND/releases/tag/v1.0.0
[0.1.0]: https://github.com/USERNAME/HIVEMIND/releases/tag/v0.1.0
