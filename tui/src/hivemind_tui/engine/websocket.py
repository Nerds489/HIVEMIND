"""
WebSocket client for HIVEMIND TUI.

Handles streaming connections to backend for real-time updates.
"""

import asyncio
import json
from typing import AsyncIterator, Callable, Dict, Optional, Any
from contextlib import asynccontextmanager

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    from websockets.exceptions import WebSocketException, ConnectionClosed
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    WebSocketClientProtocol = None
    WebSocketException = Exception
    ConnectionClosed = Exception


class WebSocketError(Exception):
    """Base exception for WebSocket errors."""

    pass


class WebSocketClient:
    """Async WebSocket client for streaming responses."""

    def __init__(
        self,
        base_url: str = "ws://localhost:8000",
        reconnect_interval: float = 2.0,
        max_reconnect_attempts: int = 5,
    ):
        """Initialize WebSocket client.

        Args:
            base_url: Base WebSocket URL
            reconnect_interval: Seconds between reconnection attempts
            max_reconnect_attempts: Maximum reconnection attempts
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets library is required for WebSocket support. "
                "Install with: pip install websockets"
            )

        self.base_url = base_url.rstrip("/")
        self.reconnect_interval = reconnect_interval
        self.max_reconnect_attempts = max_reconnect_attempts
        self._ws: Optional[WebSocketClientProtocol] = None
        self._connected = False
        self._reconnect_task: Optional[asyncio.Task] = None

    async def connect(self, endpoint: str = "/v1/stream") -> None:
        """Connect to WebSocket endpoint.

        Args:
            endpoint: WebSocket endpoint path

        Raises:
            WebSocketError: If connection fails
        """
        url = f"{self.base_url}{endpoint}"
        try:
            self._ws = await websockets.connect(url)
            self._connected = True
        except Exception as e:
            raise WebSocketError(f"Failed to connect to {url}: {e}")

    async def disconnect(self) -> None:
        """Disconnect from WebSocket."""
        self._connected = False
        if self._reconnect_task:
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass
            self._reconnect_task = None

        if self._ws:
            await self._ws.close()
            self._ws = None

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._connected and self._ws is not None and self._ws.open

    async def _reconnect(self) -> bool:
        """Attempt to reconnect to WebSocket.

        Returns:
            True if reconnection successful, False otherwise
        """
        for attempt in range(self.max_reconnect_attempts):
            try:
                await asyncio.sleep(self.reconnect_interval * (attempt + 1))
                await self.connect()
                return True
            except Exception:
                continue
        return False

    async def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message through WebSocket.

        Args:
            message: Message dictionary to send

        Raises:
            WebSocketError: If send fails
        """
        if not self.is_connected:
            raise WebSocketError("WebSocket not connected")

        try:
            await self._ws.send(json.dumps(message))
        except Exception as e:
            raise WebSocketError(f"Failed to send message: {e}")

    async def receive_message(self) -> Dict[str, Any]:
        """Receive a message from WebSocket.

        Returns:
            Received message dictionary

        Raises:
            WebSocketError: If receive fails
        """
        if not self.is_connected:
            raise WebSocketError("WebSocket not connected")

        try:
            data = await self._ws.recv()
            return self._parse_message(data)
        except ConnectionClosed as e:
            self._connected = False
            raise WebSocketError(f"Connection closed: {e}")
        except Exception as e:
            raise WebSocketError(f"Failed to receive message: {e}")

    def _parse_message(self, data: str) -> Dict[str, Any]:
        """Parse WebSocket message.

        Args:
            data: Raw message data

        Returns:
            Parsed message dictionary

        Raises:
            WebSocketError: If parsing fails
        """
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise WebSocketError(f"Failed to parse message: {e}")

    async def stream_completion(
        self,
        messages: list,
        session_id: str,
        agent_id: Optional[str] = None,
        **kwargs,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream a completion request.

        Args:
            messages: List of message dictionaries
            session_id: Session ID
            agent_id: Optional agent ID
            **kwargs: Additional parameters

        Yields:
            Stream chunks as dictionaries

        Raises:
            WebSocketError: If streaming fails
        """
        if not self.is_connected:
            await self.connect()

        # Send completion request
        request = {
            "type": "completion",
            "messages": messages,
            "session_id": session_id,
            "stream": True,
            **kwargs,
        }

        if agent_id:
            request["agent_id"] = agent_id

        await self.send_message(request)

        # Receive streamed responses
        try:
            while True:
                message = await self.receive_message()

                # Check for end of stream
                if message.get("type") == "done":
                    break

                # Check for errors
                if message.get("type") == "error":
                    raise WebSocketError(f"Stream error: {message.get('error')}")

                yield message

        except WebSocketError:
            raise
        except Exception as e:
            raise WebSocketError(f"Stream interrupted: {e}")

    async def subscribe_to_events(
        self,
        event_types: list[str],
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """Subscribe to backend events.

        Args:
            event_types: List of event types to subscribe to
            callback: Callback function for events

        Raises:
            WebSocketError: If subscription fails
        """
        if not self.is_connected:
            await self.connect()

        # Send subscription request
        subscribe_msg = {
            "type": "subscribe",
            "events": event_types,
        }
        await self.send_message(subscribe_msg)

        # Listen for events
        try:
            async for message in self._event_listener():
                await callback(message)
        except Exception as e:
            raise WebSocketError(f"Event subscription failed: {e}")

    async def _event_listener(self) -> AsyncIterator[Dict[str, Any]]:
        """Listen for events from WebSocket.

        Yields:
            Event messages
        """
        while self.is_connected:
            try:
                message = await self.receive_message()
                if message.get("type") == "event":
                    yield message
            except WebSocketError as e:
                # Try to reconnect
                if await self._reconnect():
                    continue
                else:
                    raise

    @asynccontextmanager
    async def connected(self, endpoint: str = "/v1/stream"):
        """Context manager for WebSocket connection.

        Args:
            endpoint: WebSocket endpoint

        Yields:
            WebSocket client instance
        """
        try:
            await self.connect(endpoint)
            yield self
        finally:
            await self.disconnect()

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
