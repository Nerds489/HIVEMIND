"""
HIVEMIND CLI Manager

Async subprocess manager for executing Claude/Codex CLI commands with streaming
JSON parsing and real-time output handling.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Optional

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)


class ExecutionStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ExecutionResult:
    """Result of CLI execution."""
    agent_id: str
    task: str
    status: ExecutionStatus
    output: str = ""
    error: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "task": self.task,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "metadata": self.metadata,
        }


class CLIManager:
    """
    Async subprocess manager for Claude/Codex CLI execution.

    Handles:
    - Subprocess lifecycle management
    - Streaming JSON parsing
    - Real-time output capture
    - Timeout handling
    - Error recovery
    """

    def __init__(self):
        self.settings = get_settings()
        self._active_processes: dict[str, asyncio.subprocess.Process] = {}
        self._execution_results: dict[str, ExecutionResult] = {}

    async def execute_task(
        self,
        agent_id: str,
        task: str,
        model: Optional[str] = None,
        timeout: float = 300.0,
        stream_callback: Optional[callable] = None,
    ) -> dict[str, Any]:
        """
        Execute a task using Claude or Codex CLI.

        Args:
            agent_id: Agent identifier
            task: Task description
            model: Optional model override
            timeout: Execution timeout in seconds
            stream_callback: Optional callback for streaming output

        Returns:
            Execution result dictionary

        Raises:
            TimeoutError: If execution exceeds timeout
            RuntimeError: If execution fails
        """
        logger.info(f"Executing task for agent {agent_id}: {task[:100]}")

        result = ExecutionResult(
            agent_id=agent_id,
            task=task,
            status=ExecutionStatus.PENDING,
        )

        try:
            # Determine which CLI to use based on agent configuration
            cli_type = self._get_cli_type(agent_id)
            cmd = self._build_command(cli_type, task, model)

            result.status = ExecutionStatus.RUNNING
            result.metadata["cli_type"] = cli_type
            result.metadata["command"] = " ".join(cmd)

            # Execute subprocess with streaming
            output_lines = []
            async for chunk in self._execute_subprocess(cmd, timeout):
                if stream_callback:
                    await stream_callback(chunk)
                output_lines.append(chunk)

            result.output = "\n".join(output_lines)
            result.status = ExecutionStatus.COMPLETED

        except asyncio.TimeoutError:
            result.status = ExecutionStatus.TIMEOUT
            result.error = f"Execution exceeded timeout of {timeout}s"
            logger.error(f"Task timeout for agent {agent_id}")

        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
            logger.exception(f"Task execution failed for agent {agent_id}")

        finally:
            result.end_time = datetime.utcnow()
            result.duration_seconds = (
                result.end_time - result.start_time
            ).total_seconds()

            self._execution_results[agent_id] = result

        return result.to_dict()

    async def _execute_subprocess(
        self,
        cmd: list[str],
        timeout: float,
    ) -> AsyncIterator[str]:
        """
        Execute subprocess and yield output lines.

        Args:
            cmd: Command and arguments
            timeout: Execution timeout in seconds

        Yields:
            Output lines from subprocess
        """
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        task_id = f"{cmd[0]}_{process.pid}"
        self._active_processes[task_id] = process

        try:
            # Read stdout and stderr concurrently
            async with asyncio.timeout(timeout):
                async for line in self._stream_output(process):
                    yield line

                # Wait for process to complete
                await process.wait()

                if process.returncode != 0:
                    stderr = await process.stderr.read()
                    error_msg = stderr.decode() if stderr else "Unknown error"
                    raise RuntimeError(f"Process failed: {error_msg}")

        finally:
            # Cleanup
            if task_id in self._active_processes:
                del self._active_processes[task_id]

            # Ensure process is terminated
            if process.returncode is None:
                try:
                    process.terminate()
                    await asyncio.wait_for(process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()

    async def _stream_output(
        self,
        process: asyncio.subprocess.Process,
    ) -> AsyncIterator[str]:
        """
        Stream and parse output from subprocess.

        Handles both regular text and streaming JSON formats.

        Args:
            process: Running subprocess

        Yields:
            Parsed output lines
        """
        buffer = ""

        while True:
            chunk = await process.stdout.read(1024)
            if not chunk:
                break

            buffer += chunk.decode()

            # Process complete lines
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                # Try to parse as JSON (for streaming-json format)
                parsed = self._parse_json_line(line)
                if parsed:
                    # Extract content from JSON structure
                    content = self._extract_content(parsed)
                    if content:
                        yield content
                else:
                    # Yield as plain text
                    if line.strip():
                        yield line

        # Yield remaining buffer
        if buffer.strip():
            yield buffer

    def _parse_json_line(self, line: str) -> Optional[dict]:
        """
        Parse a line as JSON.

        Args:
            line: Input line

        Returns:
            Parsed JSON object or None
        """
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

    def _extract_content(self, json_obj: dict) -> Optional[str]:
        """
        Extract content from streaming JSON object.

        Handles various JSON structures from Claude/Codex CLI.

        Args:
            json_obj: Parsed JSON object

        Returns:
            Extracted content or None
        """
        # Handle different JSON structures
        if "type" in json_obj:
            event_type = json_obj["type"]

            if event_type == "content_block_delta":
                # Claude streaming format
                delta = json_obj.get("delta", {})
                return delta.get("text", "")

            elif event_type == "message_delta":
                # Message updates
                delta = json_obj.get("delta", {})
                return delta.get("text", "")

            elif event_type == "tool_use":
                # Tool execution
                tool_name = json_obj.get("name", "unknown")
                return f"[Tool: {tool_name}]"

        # Fallback: look for common content fields
        for field in ["content", "text", "output", "message"]:
            if field in json_obj:
                content = json_obj[field]
                if isinstance(content, str):
                    return content
                elif isinstance(content, list):
                    # Extract text from content blocks
                    texts = [
                        block.get("text", "")
                        for block in content
                        if isinstance(block, dict) and "text" in block
                    ]
                    return "\n".join(texts)

        return None

    def _get_cli_type(self, agent_id: str) -> str:
        """
        Determine which CLI to use for an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            CLI type ("claude" or "codex")
        """
        # Default mapping: Use Claude for most agents
        # Can be customized based on agent configuration
        if self.settings.claude.enabled:
            return "claude"
        elif self.settings.codex.enabled:
            return "codex"
        else:
            raise RuntimeError("No CLI engines enabled")

    def _build_command(
        self,
        cli_type: str,
        task: str,
        model: Optional[str] = None,
    ) -> list[str]:
        """
        Build CLI command.

        Args:
            cli_type: Type of CLI ("claude" or "codex")
            task: Task description
            model: Optional model override

        Returns:
            Command list
        """
        if cli_type == "claude":
            cmd = [
                self.settings.claude.cli_path,
                "--format", self.settings.claude.output_format,
            ]

            if model:
                cmd.extend(["--model", model])
            else:
                cmd.extend(["--model", self.settings.claude.model])

            cmd.extend(["--max-tokens", str(self.settings.claude.max_tokens)])
            cmd.append(task)

        elif cli_type == "codex":
            cmd = [
                self.settings.codex.cli_path,
            ]

            if model:
                cmd.extend(["--model", model])
            else:
                cmd.extend(["--model", self.settings.codex.model])

            cmd.extend(["--max-tokens", str(self.settings.codex.max_tokens)])
            cmd.append(task)

        else:
            raise ValueError(f"Unknown CLI type: {cli_type}")

        return cmd

    async def get_status(self, agent_id: Optional[str] = None) -> dict[str, Any]:
        """
        Get status of agents and executions.

        Args:
            agent_id: Optional specific agent to check

        Returns:
            Status information dictionary
        """
        status = {
            "system": {
                "healthy": True,
                "active_processes": len(self._active_processes),
            },
            "agents": {},
            "services": {
                "claude": {
                    "connected": self.settings.claude.enabled,
                    "model": self.settings.claude.model,
                },
                "codex": {
                    "connected": self.settings.codex.enabled,
                    "model": self.settings.codex.model,
                },
            },
        }

        # Add execution results
        if agent_id:
            if agent_id in self._execution_results:
                result = self._execution_results[agent_id]
                status["agents"][agent_id] = {
                    "available": True,
                    "last_status": result.status.value,
                    "last_execution": result.end_time.isoformat() if result.end_time else None,
                }
        else:
            for aid, result in self._execution_results.items():
                status["agents"][aid] = {
                    "available": True,
                    "last_status": result.status.value,
                    "task_count": 1,
                }

        return status

    async def cancel_task(self, agent_id: str) -> bool:
        """
        Cancel running task for an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            True if cancelled, False otherwise
        """
        for task_id, process in self._active_processes.items():
            if agent_id in task_id:
                logger.info(f"Cancelling task for agent {agent_id}")
                process.terminate()

                try:
                    await asyncio.wait_for(process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()

                return True

        return False

    async def cleanup(self):
        """Cleanup all active processes."""
        logger.info("Cleaning up CLI manager")

        for task_id, process in list(self._active_processes.items()):
            if process.returncode is None:
                try:
                    process.terminate()
                    await asyncio.wait_for(process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()

        self._active_processes.clear()
