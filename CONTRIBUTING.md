# Contributing to HIVEMIND

Thank you for your interest in contributing to HIVEMIND! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Adding New Agents](#adding-new-agents)
- [Testing](#testing)
- [Documentation](#documentation)

---

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- No harassment or discrimination
- Assume good intentions

### Unacceptable Behavior

- Trolling or insulting comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Conduct inappropriate in a professional setting

---

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** if available
3. **Include**:
   - OS and version
   - Node.js version (`node --version`)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs
   - Output of `./hivemind --config`

### Suggesting Features

1. Check existing feature requests
2. Describe the use case clearly
3. Explain the expected behavior
4. Consider implementation complexity
5. Be open to discussion and alternatives

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and create a Pull Request

---

## Development Setup

### Prerequisites

- Node.js 18.0+
- Bash 4.0+
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/HIVEMIND.git
cd HIVEMIND

# Install dependencies (skip auth for development if needed)
./setup.sh

# Or minimal setup
chmod +x hivemind setup.sh bootstrap.sh install.sh
chmod +x engines/*.sh core/*.sh bin/*

# Run tests to verify setup
./test-installation.sh
```

### Development Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature

# Make changes...

# Test your changes
./test-installation.sh
./bin/test-hivemind

# Commit
git add .
git commit -m "feat: add your feature description"

# Push and create PR
git push origin feature/your-feature
```

---

## Pull Request Process

### Branch Naming

| Prefix | Purpose |
|--------|---------|
| `feature/` | New features |
| `bugfix/` | Bug fixes |
| `docs/` | Documentation only |
| `refactor/` | Code refactoring |
| `test/` | Test additions/improvements |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(agents): add new database optimization agent
fix(memory): resolve JSON parsing error in long-term storage
docs(readme): update installation instructions
```

### PR Checklist

Before submitting:

- [ ] Code follows project style guidelines
- [ ] All tests pass (`./test-installation.sh`)
- [ ] Documentation updated if needed
- [ ] No sensitive data committed
- [ ] Changelog updated (for features/fixes)
- [ ] Branch is up to date with main

### Review Process

1. Submit PR with clear description
2. Automated tests run
3. Maintainer reviews code
4. Address feedback
5. Approval and merge

---

## Style Guidelines

### Bash Scripts

```bash
#!/bin/bash
# Description of what this script does

set -euo pipefail  # Always start with this

# Use uppercase for constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use lowercase for variables
local my_variable="value"

# Quote all variables
echo "$my_variable"

# Use $() instead of backticks
result=$(some_command)

# Use meaningful function names
do_something_specific() {
    local param="$1"
    # Implementation
}

# Add comments for complex logic
# This loop handles edge cases where...
for item in "${items[@]}"; do
    process "$item"
done
```

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- One sentence per line (for better diffs)
- Use fenced code blocks with language tags
- Keep lines under 100 characters when possible
- Use reference-style links for repeated URLs

### YAML

```yaml
# Use 2-space indentation
key:
  nested_key: value

# Quote strings with special characters
description: "This has: colons and other 'special' chars"

# Add comments for non-obvious values
timeout: 300  # 5 minutes, matches API rate limit window
```

### JSON

```json
{
  "key": "value",
  "nested": {
    "item": "value"
  }
}
```

- 2-space indentation
- No trailing commas
- Use double quotes

---

## Adding New Agents

### Step 1: Create Agent Definition

Create `agents/<team>/<agent-name>.md`:

```markdown
# Agent Name

## Role

Brief description of the agent's role and purpose.

## Expertise

- Primary skill area
- Secondary skill area
- Supporting knowledge

## Responsibilities

- Main responsibility
- Secondary responsibility
- Quality checks

## Tools & Technologies

- Tool 1
- Tool 2

## Interaction Patterns

When to invoke this agent:
- Scenario 1
- Scenario 2

## Output Format

Expected output structure and format.
```

### Step 2: Add Routing Keywords

Update `config/routing.yaml`:

```yaml
your-agent:
  keywords:
    - keyword1
    - keyword2
  primary: YOUR-AGENT-ID
  support: []
```

### Step 3: Update spawn-agent

Add mapping in `bin/spawn-agent`:

```bash
get_agent_prompt_file() {
    local type="$1"
    case "$type" in
        # ... existing mappings ...
        your-agent) echo "team/your-agent.md" ;;
    esac
}
```

### Step 4: Create Memory Directory

```bash
mkdir -p memory/agents/YOUR-AGENT-ID
echo '{"entries":[]}' > memory/agents/YOUR-AGENT-ID/_memory.json
```

### Step 5: Test

```bash
# Verify agent is recognized
./bin/list-agents | grep your-agent

# Test spawning
./bin/spawn-agent your-agent "test task"
```

---

## Testing

### Running Tests

```bash
# Full installation test
./test-installation.sh

# HIVEMIND smoke test
./bin/test-hivemind

# Test specific agent
./bin/spawn-agent architect "test task"
```

### Writing Tests

When adding features, consider:

1. Does it work with both engines?
2. What happens with missing dependencies?
3. What happens with invalid input?
4. Does it handle edge cases?

### Test Checklist

- [ ] Core functionality works
- [ ] Error handling is graceful
- [ ] Output is correct format
- [ ] No regressions in existing features

---

## Documentation

### When to Update Docs

- Adding new features
- Changing existing behavior
- Fixing confusing documentation
- Adding examples

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, quick start |
| `docs/SETUP-GUIDE.md` | Detailed installation |
| `QUICKSTART.md` | Usage examples |
| `CHANGELOG.md` | Version history |
| `CONTRIBUTING.md` | This file |

### Documentation Style

- Write for beginners
- Include examples
- Keep it up to date
- Use consistent formatting

---

## Questions?

- Open an issue for questions
- Start a discussion for ideas
- Check existing issues first

---

## Recognition

Contributors are recognized in:

- The CHANGELOG for their contributions
- The README acknowledgments section
- Release notes when applicable

---

Thank you for helping make HIVEMIND better!
