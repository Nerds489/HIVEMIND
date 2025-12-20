"""
Claude CLI Wrapper

Async subprocess execution of the official Claude CLI tool.
Provides streaming JSON output parsing and model configuration.
"""

from __future__ import annotations

import json
from typing import Any

from hivemind.cli.manager import CLIManager, CLIOutput, OutputType


class ClaudeCLI(CLIManager):
    """
    Claude CLI subprocess wrapper.

    Executes the Claude CLI tool asynchronously with support for:
    - Streaming JSON output (content, tool_use, tool_result, error, done)
    - Model selection and configuration
    - System prompt injection
    - Timeout and cancellation
    - Tool allowing/denying
    """

    def _default_cli_path(self) -> str:
        """Get default Claude CLI path from config."""
        return self.settings.claude.cli_path

    def _default_timeout(self) -> float:
        """Get default timeout from config."""
        return self.settings.claude.timeout_seconds

    def _build_command(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> list[str]:
        """
        Build Claude CLI command.

        Args:
            prompt: User message/prompt
            model: Model identifier (e.g., "claude-sonnet-4-20250514")
            system_prompt: System prompt to inject before user message
            **kwargs: Additional arguments:
                - max_tokens: Maximum tokens to generate
                - temperature: Sampling temperature
                - tools: List of allowed tool names
                - output_format: Output format (default: "stream-json")

        Returns:
            Command as list of strings
        """
        model = model or self.settings.claude.model
        max_tokens = kwargs.get("max_tokens", self.settings.claude.max_tokens)
        output_format = kwargs.get("output_format", self.settings.claude.output_format)
        temperature = kwargs.get("temperature")
        tools = kwargs.get("tools", self.settings.claude.allowed_tools)

        # Base command
        cmd = [
            self.cli_path,
            "--model", model,
            "--max-tokens", str(max_tokens),
            "--output", output_format,
        ]

        # Optional temperature
        if temperature is not None:
            cmd.extend(["--temperature", str(temperature)])

        # System prompt
        if system_prompt:
            cmd.extend(["--system", system_prompt])

        # Tool configuration
        if tools:
            for tool in tools:
                cmd.extend(["--allow-tool", tool])

        # User prompt (last argument)
        cmd.append(prompt)

        return cmd

    def _parse_output_line(self, line: str) -> CLIOutput:
        """
        Parse Claude CLI JSON output line.

        Claude CLI outputs stream-json format with events like:
        - {"type": "content", "content": "text...", "index": 0}
        - {"type": "tool_use", "name": "Read", "input": {...}, "id": "..."}
        - {"type": "tool_result", "tool_use_id": "...", "result": {...}}
        - {"type": "error", "error": "message"}
        - {"type": "done", "stop_reason": "end_turn"}

        Args:
            line: Raw JSON line from stdout

        Returns:
            Parsed CLIOutput
        """
        try:
            data = json.loads(line)

            # Determine output type
            event_type = data.get("type", "content")

            # Map event types to OutputType enum
            type_mapping = {
                "content": OutputType.CONTENT,
                "tool_use": OutputType.TOOL_USE,
                "tool_result": OutputType.TOOL_RESULT,
                "error": OutputType.ERROR,
                "done": OutputType.DONE,
                "message_start": OutputType.METADATA,
                "message_delta": OutputType.METADATA,
                "message_stop": OutputType.DONE,
                "content_block_start": OutputType.METADATA,
                "content_block_delta": OutputType.CONTENT,
                "content_block_stop": OutputType.METADATA,
            }

            output_type = type_mapping.get(event_type, OutputType.METADATA)

            # Handle content delta extraction
            if event_type == "content_block_delta":
                delta = data.get("delta", {})
                if "text" in delta:
                    # Text content delta
                    return CLIOutput(
                        type=OutputType.CONTENT,
                        data={"content": delta["text"], "index": data.get("index", 0)},
                        raw=line,
                    )
                elif "partial_json" in delta:
                    # Tool input delta
                    return CLIOutput(
                        type=OutputType.TOOL_USE,
                        data={
                            "partial_json": delta["partial_json"],
                            "index": data.get("index", 0),
                        },
                        raw=line,
                    )

            # Handle tool use start
            if event_type == "content_block_start":
                content_block = data.get("content_block", {})
                if content_block.get("type") == "tool_use":
                    return CLIOutput(
                        type=OutputType.TOOL_USE,
                        data={
                            "id": content_block.get("id"),
                            "name": content_block.get("name"),
                            "input": content_block.get("input", {}),
                        },
                        raw=line,
                    )

            return CLIOutput(type=output_type, data=data, raw=line)

        except (json.JSONDecodeError, ValueError) as e:
            # Return error output for unparseable lines
            return CLIOutput(
                type=OutputType.ERROR,
                data={"error": f"Failed to parse Claude CLI output: {e}", "raw_line": line},
                raw=line,
            )

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        tools: list[str] | None = None,
    ) -> list[CLIOutput]:
        """
        Generate a complete response (collect all streaming outputs).

        Convenience method that collects all streaming outputs into a list.
        For large responses, prefer using execute() directly to stream.

        Args:
            prompt: User message
            model: Model identifier
            system_prompt: System prompt
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            tools: Allowed tool names

        Returns:
            List of all CLIOutput events

        Raises:
            asyncio.TimeoutError: If execution exceeds timeout
            RuntimeError: If CLI execution fails
        """
        outputs = []
        async for output in self.execute(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            tools=tools,
        ):
            outputs.append(output)

            # Stop on error or done
            if output.is_error or output.is_done:
                break

        return outputs

    @staticmethod
    def extract_text_content(outputs: list[CLIOutput]) -> str:
        """
        Extract all text content from output list.

        Args:
            outputs: List of CLIOutput events

        Returns:
            Concatenated text content
        """
        parts = []
        for output in outputs:
            if output.type == OutputType.CONTENT and output.content:
                parts.append(output.content)
        return "".join(parts)

    @staticmethod
    def extract_tool_uses(outputs: list[CLIOutput]) -> list[dict[str, Any]]:
        """
        Extract all tool use events from output list.

        Args:
            outputs: List of CLIOutput events

        Returns:
            List of tool use dictionaries with name, input, id
        """
        tools = []
        for output in outputs:
            if output.type == OutputType.TOOL_USE:
                # Only include complete tool uses (with name and id)
                if "name" in output.data and "id" in output.data:
                    tools.append({
                        "id": output.data["id"],
                        "name": output.data["name"],
                        "input": output.data.get("input", {}),
                    })
        return tools

    @staticmethod
    def has_error(outputs: list[CLIOutput]) -> bool:
        """
        Check if any output contains an error.

        Args:
            outputs: List of CLIOutput events

        Returns:
            True if any error found
        """
        return any(output.is_error for output in outputs)
