"""
Input handler for HIVEMIND TUI.

Processes user input and routes to appropriate handlers.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, Any, List

from ..engine.state import AppState
from ..engine.client import APIClient
from ..models.messages import MessageRole
from .commands import CommandHandler, CommandResult


class InputType(str, Enum):
    """Input type classification."""

    COMMAND = "command"
    MESSAGE = "message"
    SPECIAL_KEY = "special_key"
    EMPTY = "empty"


@dataclass
class InputResult:
    """Result of input processing."""

    input_type: InputType
    processed: bool
    response: Optional[str] = None
    error: Optional[str] = None
    should_quit: bool = False
    command_result: Optional[CommandResult] = None


class InputHandler:
    """Handles user input processing and routing."""

    def __init__(
        self,
        state: AppState,
        api_client: Optional[APIClient] = None,
    ):
        """Initialize input handler.

        Args:
            state: Application state
            api_client: Optional API client for message handling
        """
        self.state = state
        self.api_client = api_client
        self.command_handler = CommandHandler(state)
        self._special_key_handlers: dict[str, Callable] = {}

    def register_special_key(self, key: str, handler: Callable) -> None:
        """Register a handler for special key.

        Args:
            key: Key identifier
            handler: Handler function
        """
        self._special_key_handlers[key] = handler

    def unregister_special_key(self, key: str) -> None:
        """Unregister a special key handler.

        Args:
            key: Key identifier
        """
        if key in self._special_key_handlers:
            del self._special_key_handlers[key]

    async def process_input(self, input_text: str) -> InputResult:
        """Process user input.

        Args:
            input_text: User input string

        Returns:
            Input processing result
        """
        # Check for empty input
        if not input_text or not input_text.strip():
            return InputResult(
                input_type=InputType.EMPTY,
                processed=False,
            )

        # Check for command
        if self.command_handler.is_command(input_text):
            return await self._process_command(input_text)

        # Process as message
        return await self._process_message(input_text)

    async def _process_command(self, input_text: str) -> InputResult:
        """Process command input.

        Args:
            input_text: Command input

        Returns:
            Input result
        """
        try:
            result = await self.command_handler.execute(input_text)

            return InputResult(
                input_type=InputType.COMMAND,
                processed=result.success,
                response=result.message,
                error=None if result.success else result.message,
                should_quit=result.should_quit,
                command_result=result,
            )
        except Exception as e:
            return InputResult(
                input_type=InputType.COMMAND,
                processed=False,
                error=f"Command processing error: {str(e)}",
            )

    async def _process_message(self, input_text: str) -> InputResult:
        """Process message input.

        Args:
            input_text: Message input

        Returns:
            Input result
        """
        # Add user message to state
        self.state.add_message(MessageRole.USER, input_text)

        # If no API client, just store the message
        if not self.api_client:
            return InputResult(
                input_type=InputType.MESSAGE,
                processed=True,
                response="Message stored (no API client connected)",
            )

        # Check connection
        if not self.state.is_connected():
            return InputResult(
                input_type=InputType.MESSAGE,
                processed=False,
                error="Not connected to backend. Messages are stored locally.",
            )

        # Send to API
        try:
            return await self._send_to_api(input_text)
        except Exception as e:
            error_msg = f"Failed to send message: {str(e)}"
            self.state.add_message(MessageRole.ERROR, error_msg)
            return InputResult(
                input_type=InputType.MESSAGE,
                processed=False,
                error=error_msg,
            )

    async def _send_to_api(self, message: str) -> InputResult:
        """Send message to API and get response.

        Args:
            message: User message

        Returns:
            Input result
        """
        if not self.api_client:
            return InputResult(
                input_type=InputType.MESSAGE,
                processed=False,
                error="No API client available",
            )

        # Set processing state
        self.state.set_processing(True, "Sending message...")

        try:
            # Ensure we have a session
            if not self.state.has_session():
                session_id = await self.api_client.create_session()
                self.state.set_session(session_id)

            # Get conversation in API format
            messages = self.state.conversation.to_api_format()

            # Get selected agent if any
            agent_id = self.state.selected_agent.id if self.state.selected_agent else None

            # Send completion request
            response = await self.api_client.send_completion(
                messages=messages,
                agent_id=agent_id,
            )

            # Extract response content
            response_text = self._extract_response_text(response)

            # Add assistant response to state
            self.state.add_message(
                MessageRole.ASSISTANT,
                response_text,
                agent_id=agent_id,
            )

            return InputResult(
                input_type=InputType.MESSAGE,
                processed=True,
                response=response_text,
            )

        except Exception as e:
            error_msg = f"API error: {str(e)}"
            return InputResult(
                input_type=InputType.MESSAGE,
                processed=False,
                error=error_msg,
            )
        finally:
            self.state.set_processing(False)

    def _extract_response_text(self, response: dict) -> str:
        """Extract response text from API response.

        Args:
            response: API response dictionary

        Returns:
            Response text
        """
        # Handle different response formats
        if "content" in response:
            return response["content"]
        elif "choices" in response and response["choices"]:
            choice = response["choices"][0]
            if "message" in choice:
                return choice["message"].get("content", "")
            elif "text" in choice:
                return choice["text"]
        elif "message" in response:
            if isinstance(response["message"], dict):
                return response["message"].get("content", "")
            return str(response["message"])

        # Fallback
        return str(response)

    async def process_special_key(self, key: str) -> InputResult:
        """Process special key input.

        Args:
            key: Key identifier

        Returns:
            Input result
        """
        handler = self._special_key_handlers.get(key)
        if not handler:
            return InputResult(
                input_type=InputType.SPECIAL_KEY,
                processed=False,
                error=f"No handler for special key: {key}",
            )

        try:
            result = await handler()
            return InputResult(
                input_type=InputType.SPECIAL_KEY,
                processed=True,
                response=str(result) if result else None,
            )
        except Exception as e:
            return InputResult(
                input_type=InputType.SPECIAL_KEY,
                processed=False,
                error=f"Special key handler error: {str(e)}",
            )

    def validate_input(self, input_text: str, max_length: int = 10000) -> tuple[bool, Optional[str]]:
        """Validate user input.

        Args:
            input_text: Input to validate
            max_length: Maximum allowed length

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not input_text:
            return True, None

        if len(input_text) > max_length:
            return False, f"Input too long (max {max_length} characters)"

        # Check for null characters
        if "\x00" in input_text:
            return False, "Input contains null characters"

        return True, None

    def get_completion_suggestions(self, partial_input: str) -> List[str]:
        """Get command completion suggestions.

        Args:
            partial_input: Partial input text

        Returns:
            List of completion suggestions
        """
        suggestions = []

        if not partial_input.startswith("/"):
            return suggestions

        # Get command portion
        command_part = partial_input[1:].lower()

        # Get all available commands
        commands = self.command_handler.get_available_commands()

        # Find matches
        for cmd in commands:
            if cmd.startswith(command_part):
                suggestions.append(f"/{cmd}")

        return suggestions

    def format_error(self, error: str) -> str:
        """Format error message for display.

        Args:
            error: Error message

        Returns:
            Formatted error message
        """
        return f"Error: {error}"

    def format_response(self, response: str) -> str:
        """Format response message for display.

        Args:
            response: Response message

        Returns:
            Formatted response
        """
        return response

    async def handle_interrupt(self) -> InputResult:
        """Handle user interrupt (Ctrl+C).

        Returns:
            Input result
        """
        # Stop any ongoing processing
        if self.state.is_processing:
            self.state.set_processing(False)
            return InputResult(
                input_type=InputType.SPECIAL_KEY,
                processed=True,
                response="Processing interrupted.",
            )

        # Otherwise, treat as quit
        return InputResult(
            input_type=InputType.SPECIAL_KEY,
            processed=True,
            response="Interrupted. Use /quit to exit.",
        )

    async def handle_eof(self) -> InputResult:
        """Handle end-of-file (Ctrl+D).

        Returns:
            Input result indicating quit
        """
        return InputResult(
            input_type=InputType.SPECIAL_KEY,
            processed=True,
            response="EOF received. Quitting...",
            should_quit=True,
        )
