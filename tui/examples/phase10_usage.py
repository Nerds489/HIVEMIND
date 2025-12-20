"""
Example usage of Phase 10 TUI Engine Integration.

Demonstrates how to use the engine, models, and handlers together.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hivemind_tui.engine.client import APIClient
from hivemind_tui.engine.state import AppState
from hivemind_tui.models.messages import MessageRole
from hivemind_tui.models.agents import Agent, AgentStatus
from hivemind_tui.handlers.commands import CommandHandler
from hivemind_tui.handlers.input import InputHandler


async def basic_state_example():
    """Demonstrate basic state management."""
    print("\n=== Basic State Management ===\n")

    # Create application state
    state = AppState()

    # Set up session
    state.set_session("example-session-001")
    print(f"Session created: {state.session_id}")

    # Add some messages
    state.add_message(MessageRole.USER, "Hello, HIVEMIND!")
    state.add_message(MessageRole.ASSISTANT, "Hello! How can I help you today?")
    state.add_message(MessageRole.USER, "Tell me about yourself.")

    print(f"Messages in conversation: {state.get_message_count()}")

    # Display messages
    print("\nConversation history:")
    for msg in state.conversation:
        print(f"  {msg}")

    # Add agents
    agents = [
        Agent(
            id="dev-001",
            name="Developer",
            description="Backend development specialist",
            status=AgentStatus.IDLE,
        ),
        Agent(
            id="sec-001",
            name="Security",
            description="Security architecture expert",
            status=AgentStatus.IDLE,
        ),
    ]
    state.set_agents(agents)
    print(f"\nAgents available: {len(state.agents)}")

    # Select an agent
    state.select_agent("dev-001")
    print(f"Selected agent: {state.selected_agent.name}")

    # Show state summary
    print(f"\nState summary: {state}")


async def command_handler_example():
    """Demonstrate command handling."""
    print("\n=== Command Handler ===\n")

    state = AppState()
    state.set_session("cmd-example-session")

    # Add some agents
    state.set_agents([
        Agent(id="agent-001", name="Agent 1", description="First agent"),
        Agent(id="agent-002", name="Agent 2", description="Second agent"),
    ])

    cmd_handler = CommandHandler(state)

    # Test various commands
    commands = [
        "/help",
        "/agents",
        "/select agent-001",
        "/status",
        "/session",
    ]

    for cmd in commands:
        print(f"Command: {cmd}")
        result = await cmd_handler.execute(cmd)
        print(f"Success: {result.success}")
        print(f"Response:\n{result.message}\n")


async def input_handler_example():
    """Demonstrate input handling."""
    print("\n=== Input Handler ===\n")

    state = AppState()
    state.set_session("input-example-session")

    input_handler = InputHandler(state)

    # Test different input types
    inputs = [
        "",  # Empty
        "/help",  # Command
        "Hello, how are you?",  # Message (no API client)
        "/clear",  # Command
        "/quit",  # Quit command
    ]

    for user_input in inputs:
        print(f"Input: '{user_input}'")
        result = await input_handler.process_input(user_input)
        print(f"Type: {result.input_type.value}")
        print(f"Processed: {result.processed}")
        if result.response:
            print(f"Response: {result.response}")
        if result.error:
            print(f"Error: {result.error}")
        if result.should_quit:
            print("Application should quit")
        print()


async def observer_pattern_example():
    """Demonstrate the observer pattern for reactive updates."""
    print("\n=== Observer Pattern ===\n")

    state = AppState()

    # Create observer callback
    def state_observer(field_name, value):
        print(f"State changed: {field_name} = {value}")

    # Register observer
    state.add_observer(state_observer)

    print("Adding session...")
    state.set_session("observer-session")

    print("\nAdding message...")
    state.add_message(MessageRole.USER, "Test message")

    print("\nSelecting agent...")
    agent = Agent(id="test-001", name="Test", description="Test agent")
    state.set_agents([agent])
    state.select_agent("test-001")

    print("\nUpdating connection status...")
    from hivemind_tui.engine.state import ConnectionStatus
    state.set_connection_status(ConnectionStatus.CONNECTED)


async def api_client_example():
    """Demonstrate API client (will fail without running backend)."""
    print("\n=== API Client (Demo - No Backend) ===\n")

    # Create client
    client = APIClient(base_url="http://localhost:8000", timeout=5.0)

    print("API Client created")
    print(f"Base URL: {client.base_url}")
    print(f"Connected: {client.is_connected}")

    # Note: This will fail without a running backend
    # In a real scenario, you would:
    # async with client:
    #     session_id = await client.create_session()
    #     agents = await client.get_agents()
    #     response = await client.send_completion(messages=[...])

    print("\nAPI client methods available:")
    print("  - connect() / close()")
    print("  - create_session()")
    print("  - send_completion()")
    print("  - get_agents()")
    print("  - get_status()")
    print("  - update_agent_status()")


async def integrated_example():
    """Demonstrate integrated usage of all components."""
    print("\n=== Integrated Example ===\n")

    # Initialize components
    state = AppState()
    cmd_handler = CommandHandler(state)
    input_handler = InputHandler(state)

    # Set up state observer
    def on_state_change(field, value):
        if field == "message_added":
            print(f"  [EVENT] New message: {value.role.value}")
        elif field == "session_id":
            print(f"  [EVENT] Session: {value}")

    state.add_observer(on_state_change)

    # Simulate session
    print("Starting session...")
    state.set_session("integrated-session-001")

    # Add agents
    agents = [
        Agent(id="dev-001", name="Developer", description="Code expert"),
        Agent(id="sec-001", name="Security", description="Security expert"),
    ]
    state.set_agents(agents)

    # Process various inputs
    test_inputs = [
        "/agents",
        "/select dev-001",
        "Write a Python function to calculate fibonacci",
        "/status",
        "/clear",
    ]

    print("\nProcessing inputs:\n")
    for user_input in test_inputs:
        print(f"User: {user_input}")
        result = await input_handler.process_input(user_input)

        if result.response:
            # Truncate long responses for display
            response = result.response
            if len(response) > 200:
                response = response[:200] + "..."
            print(f"System: {response}\n")

    print(f"Final message count: {state.get_message_count()}")
    print(f"Selected agent: {state.selected_agent.name if state.selected_agent else 'None'}")


async def main():
    """Run all examples."""
    print("=" * 70)
    print("Phase 10: TUI Engine Integration - Usage Examples")
    print("=" * 70)

    examples = [
        ("Basic State Management", basic_state_example),
        ("Command Handler", command_handler_example),
        ("Input Handler", input_handler_example),
        ("Observer Pattern", observer_pattern_example),
        ("API Client", api_client_example),
        ("Integrated Usage", integrated_example),
    ]

    for name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            print(f"\nExample '{name}' error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
