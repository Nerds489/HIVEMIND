# HIVEMIND CLI Subprocess Wrappers

Phase 3 implementation of async subprocess wrappers for Claude and Codex CLI tools.

## Overview

The CLI module provides async Python wrappers around the `claude` and `codex` command-line tools, enabling:

- Async subprocess execution with streaming output
- JSON output parsing (content, tool_use, tool_result, error, done)
- Model selection and configuration
- System prompt injection
- Timeout and cancellation support

## Components

### Base Classes

- **`CLIManager`** - Abstract base class for CLI subprocess managers
- **`CLIOutput`** - Structured output from CLI events
- **`OutputType`** - Enum for output event types (CONTENT, TOOL_USE, TOOL_RESULT, ERROR, DONE, METADATA)

### Implementations

- **`ClaudeCLI`** - Wrapper for Anthropic's Claude CLI
- **`CodexCLI`** - Wrapper for OpenAI's Codex CLI

## Usage Examples

### Basic Claude Execution

```python
import asyncio
from hivemind.cli import ClaudeCLI

async def main():
    cli = ClaudeCLI()

    # Stream output events
    async for output in cli.execute(
        prompt="Explain Python asyncio in 3 sentences",
        model="claude-sonnet-4-20250514",
    ):
        if output.type == "content":
            print(output.content, end="", flush=True)
        elif output.is_error:
            print(f"Error: {output.data}")
        elif output.is_done:
            print("\n[Done]")

asyncio.run(main())
```

### Collecting Complete Response

```python
import asyncio
from hivemind.cli import ClaudeCLI

async def main():
    cli = ClaudeCLI()

    # Collect all outputs
    outputs = await cli.generate(
        prompt="Write a hello world function in Python",
        system_prompt="You are a Python expert. Be concise.",
        max_tokens=500,
    )

    # Extract text content
    text = ClaudeCLI.extract_text_content(outputs)
    print(text)

    # Check for errors
    if ClaudeCLI.has_error(outputs):
        print("Execution had errors")

asyncio.run(main())
```

### Tool Use Detection

```python
import asyncio
from hivemind.cli import ClaudeCLI

async def main():
    cli = ClaudeCLI()

    outputs = await cli.generate(
        prompt="Read the file at /etc/hostname",
        tools=["Read", "Bash"],
    )

    # Extract tool uses
    tools = ClaudeCLI.extract_tool_uses(outputs)
    for tool in tools:
        print(f"Tool: {tool['name']}")
        print(f"Input: {tool['input']}")

asyncio.run(main())
```

### Codex with Reasoning

```python
import asyncio
from hivemind.cli import CodexCLI

async def main():
    cli = CodexCLI()

    outputs = await cli.generate(
        prompt="Optimize this algorithm for sorting",
        model="o4-mini",
        reasoning_effort="high",
    )

    # Extract reasoning tokens (o-series specific)
    reasoning = CodexCLI.extract_reasoning(outputs)
    for r in reasoning:
        print(f"Reasoning: {r}")

    # Extract response
    text = CodexCLI.extract_text_content(outputs)
    print(f"\nResponse: {text}")

asyncio.run(main())
```

### Timeout and Cancellation

```python
import asyncio
from hivemind.cli import ClaudeCLI

async def main():
    cli = ClaudeCLI(timeout=10.0)  # 10 second timeout

    try:
        async for output in cli.execute(prompt="Long task..."):
            print(output.content or output.data)
    except asyncio.TimeoutError:
        print("Execution timed out")
        await cli.cancel()

asyncio.run(main())
```

### Custom Configuration

```python
from hivemind.cli import ClaudeCLI
from hivemind.config import get_settings

# Use configuration from hivemind.config
settings = get_settings()
print(f"Claude model: {settings.claude.model}")
print(f"Timeout: {settings.claude.timeout_seconds}s")

# Override defaults
cli = ClaudeCLI(
    cli_path="/custom/path/to/claude",
    timeout=600.0,
)
```

## Output Structure

### CLIOutput

Each output event has:

```python
@dataclass
class CLIOutput:
    type: OutputType          # Event type
    data: dict[str, Any]      # Event data
    raw: str | None           # Raw JSON line

    # Properties
    is_error: bool            # True if type is ERROR
    is_done: bool             # True if type is DONE
    content: str | None       # Extracted text content
```

### OutputType Enum

```python
class OutputType(str, Enum):
    CONTENT = "content"           # Text content chunk
    TOOL_USE = "tool_use"         # Tool invocation
    TOOL_RESULT = "tool_result"   # Tool execution result
    ERROR = "error"               # Error event
    DONE = "done"                 # Completion signal
    METADATA = "metadata"         # Metadata (reasoning, etc)
```

## Configuration

CLI wrappers use settings from `hivemind.config`:

```python
class ClaudeConfig(BaseSettings):
    enabled: bool = True
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8192
    timeout_seconds: float = 300.0
    api_key: SecretStr | None = None
    cli_path: str = "claude"
    output_format: str = "stream-json"
    allowed_tools: list[str] = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]

class CodexConfig(BaseSettings):
    enabled: bool = True
    model: str = "o4-mini"
    max_tokens: int = 8192
    timeout_seconds: float = 300.0
    api_key: SecretStr | None = None
    cli_path: str = "codex"
```

Override via environment variables:

```bash
export HIVEMIND_CLAUDE_MODEL="claude-opus-4"
export HIVEMIND_CLAUDE_TIMEOUT_SECONDS=600
export ANTHROPIC_API_KEY="sk-..."

export HIVEMIND_CODEX_MODEL="o3-mini"
export OPENAI_API_KEY="sk-..."
```

## Error Handling

All methods raise exceptions on failure:

```python
try:
    outputs = await cli.generate(prompt="...")
except asyncio.TimeoutError:
    print("Execution timed out")
except RuntimeError as e:
    print(f"CLI execution failed: {e}")
```

Errors are also yielded as `CLIOutput` events:

```python
async for output in cli.execute(prompt="..."):
    if output.is_error:
        print(f"Error: {output.data['error']}")
        # stderr might be available
        if 'stderr' in output.data:
            print(f"Stderr: {output.data['stderr']}")
```

## Implementation Notes

- **Stream-first design**: All methods use `AsyncIterator` for memory efficiency
- **Engine-agnostic**: Works with any CLI tool that outputs stream-json format
- **Config-driven**: Uses HIVEMIND configuration system for defaults
- **Type-safe**: Full type hints for all public APIs
- **Cancellation-safe**: Proper cleanup with SIGTERM → SIGKILL escalation

## Testing

Manual testing (requires claude/codex CLI tools installed):

```python
import asyncio
from hivemind.cli import ClaudeCLI, CodexCLI

async def test_claude():
    cli = ClaudeCLI()
    outputs = await cli.generate("Say hello")
    print(ClaudeCLI.extract_text_content(outputs))

async def test_codex():
    cli = CodexCLI()
    outputs = await cli.generate("Say hello")
    print(CodexCLI.extract_text_content(outputs))

asyncio.run(test_claude())
asyncio.run(test_codex())
```

## Future Enhancements

Potential Phase 4+ additions:

- Response caching and memoization
- Retry logic with exponential backoff
- Multi-turn conversation support
- Token usage tracking and limits
- Rate limiting integration
- Parallel execution of multiple prompts
- Cost tracking per execution
