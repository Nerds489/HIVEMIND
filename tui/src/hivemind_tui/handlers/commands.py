"""
Command handler for HIVEMIND TUI.

Processes slash commands and returns formatted responses.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Callable, Any, List

from ..models.agents import Agent
from ..engine.state import AppState


class CommandType(str, Enum):
    """Available command types."""

    HELP = "help"
    CLEAR = "clear"
    AGENTS = "agents"
    SELECT = "select"
    STATUS = "status"
    SESSION = "session"
    QUIT = "quit"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass
class CommandResult:
    """Result of command execution."""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    should_quit: bool = False


class CommandHandler:
    """Handles parsing and execution of TUI commands."""

    COMMAND_PREFIX = "/"

    def __init__(self, state: AppState):
        """Initialize command handler.

        Args:
            state: Application state
        """
        self.state = state
        self._commands: Dict[str, Callable] = {
            "help": self._help_command,
            "clear": self._clear_command,
            "agents": self._agents_command,
            "select": self._select_command,
            "status": self._status_command,
            "session": self._session_command,
            "quit": self._quit_command,
            "exit": self._quit_command,
        }

    def is_command(self, input_text: str) -> bool:
        """Check if input is a command.

        Args:
            input_text: User input

        Returns:
            True if input starts with command prefix
        """
        return input_text.strip().startswith(self.COMMAND_PREFIX)

    def parse_command(self, input_text: str) -> tuple[CommandType, List[str]]:
        """Parse command from input.

        Args:
            input_text: User input

        Returns:
            Tuple of (command_type, arguments)
        """
        text = input_text.strip()
        if not text.startswith(self.COMMAND_PREFIX):
            return CommandType.UNKNOWN, []

        # Remove prefix and split
        parts = text[1:].split()
        if not parts:
            return CommandType.UNKNOWN, []

        command_name = parts[0].lower()
        args = parts[1:]

        # Map to command type
        try:
            command_type = CommandType(command_name)
        except ValueError:
            command_type = CommandType.UNKNOWN

        return command_type, args

    async def execute(self, input_text: str) -> CommandResult:
        """Execute a command.

        Args:
            input_text: User input

        Returns:
            Command execution result
        """
        command_type, args = self.parse_command(input_text)

        if command_type == CommandType.UNKNOWN:
            return CommandResult(
                success=False,
                message=f"Unknown command. Type {self.COMMAND_PREFIX}help for available commands.",
            )

        # Get handler
        handler = self._commands.get(command_type.value)
        if not handler:
            return CommandResult(
                success=False,
                message=f"Command '{command_type.value}' not implemented.",
            )

        # Execute handler
        try:
            return await handler(args)
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Command error: {str(e)}",
            )

    async def _help_command(self, args: List[str]) -> CommandResult:
        """Show help information.

        Args:
            args: Command arguments

        Returns:
            Command result
        """
        help_text = """
Available Commands:
  /help              - Show this help message
  /clear             - Clear conversation history
  /agents            - List available agents
  /select <agent_id> - Select an agent to use
  /status            - Show connection and session status
  /session           - Show current session information
  /quit, /exit       - Exit the application

Examples:
  /agents
  /select agent-001
  /clear
        """.strip()

        return CommandResult(
            success=True,
            message=help_text,
        )

    async def _clear_command(self, args: List[str]) -> CommandResult:
        """Clear conversation history.

        Args:
            args: Command arguments

        Returns:
            Command result
        """
        message_count = len(self.state.conversation)
        self.state.clear_messages()

        return CommandResult(
            success=True,
            message=f"Cleared {message_count} message(s) from conversation history.",
            data={"cleared_count": message_count},
        )

    async def _agents_command(self, args: List[str]) -> CommandResult:
        """List available agents.

        Args:
            args: Command arguments

        Returns:
            Command result
        """
        if not self.state.agents:
            return CommandResult(
                success=True,
                message="No agents available. Connect to backend to see agents.",
            )

        # Format agent list
        lines = ["Available Agents:"]
        for i, agent in enumerate(self.state.agents, 1):
            selected = " [SELECTED]" if self.state.selected_agent and agent.id == self.state.selected_agent.id else ""
            lines.append(f"  {i}. {agent.name} ({agent.id}) - {agent.status.value}{selected}")
            if agent.description:
                lines.append(f"     {agent.description}")

        message = "\n".join(lines)

        return CommandResult(
            success=True,
            message=message,
            data={"agents": [agent.to_dict() for agent in self.state.agents]},
        )

    async def _select_command(self, args: List[str]) -> CommandResult:
        """Select an agent.

        Args:
            args: Command arguments (agent_id)

        Returns:
            Command result
        """
        if not args:
            # Deselect current agent
            if self.state.selected_agent:
                self.state.select_agent(None)
                return CommandResult(
                    success=True,
                    message="Deselected agent. Using default routing.",
                )
            else:
                return CommandResult(
                    success=True,
                    message="No agent selected. Provide agent ID to select.",
                )

        agent_id = args[0]

        # Try to select agent
        if self.state.select_agent(agent_id):
            agent = self.state.selected_agent
            return CommandResult(
                success=True,
                message=f"Selected agent: {agent.name} ({agent.id})",
                data={"agent": agent.to_dict()},
            )
        else:
            return CommandResult(
                success=False,
                message=f"Agent '{agent_id}' not found. Use /agents to see available agents.",
            )

    async def _status_command(self, args: List[str]) -> CommandResult:
        """Show connection and session status.

        Args:
            args: Command arguments

        Returns:
            Command result
        """
        lines = [
            "System Status:",
            f"  Connection: {self.state.connection_status.value}",
            f"  Session: {self.state.session_id or 'None'}",
            f"  Messages: {len(self.state.conversation)}",
            f"  Agents: {len(self.state.agents)} available",
            f"  Selected Agent: {self.state.selected_agent.name if self.state.selected_agent else 'None'}",
            f"  Processing: {'Yes' if self.state.is_processing else 'No'}",
        ]

        if self.state.last_error:
            lines.append(f"  Last Error: {self.state.last_error}")

        message = "\n".join(lines)

        return CommandResult(
            success=True,
            message=message,
            data=self.state.to_dict(),
        )

    async def _session_command(self, args: List[str]) -> CommandResult:
        """Show session information.

        Args:
            args: Command arguments

        Returns:
            Command result
        """
        if not self.state.has_session():
            return CommandResult(
                success=True,
                message="No active session.",
            )

        lines = [
            "Session Information:",
            f"  ID: {self.state.session_id}",
            f"  Created: {self.state.session_created_at.strftime('%Y-%m-%d %H:%M:%S') if self.state.session_created_at else 'Unknown'}",
            f"  Messages: {len(self.state.conversation)}",
        ]

        message = "\n".join(lines)

        return CommandResult(
            success=True,
            message=message,
            data={
                "session_id": self.state.session_id,
                "created_at": self.state.session_created_at.isoformat() if self.state.session_created_at else None,
                "message_count": len(self.state.conversation),
            },
        )

    async def _quit_command(self, args: List[str]) -> CommandResult:
        """Quit the application.

        Args:
            args: Command arguments

        Returns:
            Command result with should_quit=True
        """
        return CommandResult(
            success=True,
            message="Goodbye!",
            should_quit=True,
        )

    def get_available_commands(self) -> List[str]:
        """Get list of available commands.

        Returns:
            List of command names
        """
        return list(self._commands.keys())

    def get_command_help(self, command: str) -> Optional[str]:
        """Get help text for a specific command.

        Args:
            command: Command name

        Returns:
            Help text or None if command not found
        """
        help_texts = {
            "help": "Show available commands and usage information",
            "clear": "Clear the conversation history",
            "agents": "List all available agents",
            "select": "Select an agent to use (provide agent ID or leave empty to deselect)",
            "status": "Show connection and session status",
            "session": "Show current session information",
            "quit": "Exit the application",
            "exit": "Exit the application",
        }
        return help_texts.get(command)
