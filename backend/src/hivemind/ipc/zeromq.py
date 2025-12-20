"""
HIVEMIND ZeroMQ IPC Client

ZeroMQ DEALER/ROUTER implementation for request-reply patterns.
Provides async message passing with routing and load balancing.
"""

import asyncio
from typing import AsyncIterator, Optional

import zmq
import zmq.asyncio

from hivemind.config import get_settings
from hivemind.ipc.base import AgentMessage, MessageType
from hivemind.observability import get_logger

logger = get_logger(__name__)


class ZeroMQClient:
    """
    ZeroMQ client for inter-agent communication.

    Uses DEALER socket for clients and ROUTER socket for servers.
    Supports request-reply and publish-subscribe patterns.
    """

    def __init__(
        self,
        identity: str,
        mode: str = "dealer",
        endpoint: Optional[str] = None,
    ):
        """
        Initialize ZeroMQ client.

        Args:
            identity: Unique identity for this client
            mode: Socket mode ("dealer" or "router")
            endpoint: ZeroMQ endpoint (uses config default if None)
        """
        self.settings = get_settings()
        self.identity = identity.encode()
        self.mode = mode.lower()

        # Determine endpoint
        if endpoint:
            self.endpoint = endpoint
        elif self.mode == "dealer":
            self.endpoint = self.settings.zeromq.dealer_endpoint
        else:
            self.endpoint = self.settings.zeromq.router_endpoint

        # Initialize ZeroMQ context and socket
        self.context = zmq.asyncio.Context()
        self.socket: Optional[zmq.asyncio.Socket] = None
        self._running = False
        self._pending_replies: dict[str, asyncio.Future] = {}

        logger.info(
            f"ZeroMQ client initialized: identity={identity}, "
            f"mode={mode}, endpoint={self.endpoint}"
        )

    async def connect(self):
        """Connect to ZeroMQ endpoint."""
        if self.socket:
            logger.warning("Socket already connected")
            return

        # Create socket based on mode
        if self.mode == "dealer":
            self.socket = self.context.socket(zmq.DEALER)
        elif self.mode == "router":
            self.socket = self.context.socket(zmq.ROUTER)
        else:
            raise ValueError(f"Invalid mode: {self.mode}")

        # Set socket identity
        self.socket.setsockopt(zmq.IDENTITY, self.identity)

        # Configure socket options
        self.socket.setsockopt(zmq.SNDHWM, self.settings.zeromq.high_water_mark)
        self.socket.setsockopt(zmq.RCVHWM, self.settings.zeromq.high_water_mark)
        self.socket.setsockopt(zmq.LINGER, self.settings.zeromq.linger)
        self.socket.setsockopt(zmq.RCVTIMEO, self.settings.zeromq.recv_timeout)
        self.socket.setsockopt(zmq.SNDTIMEO, self.settings.zeromq.send_timeout)

        # Connect or bind based on mode
        if self.mode == "dealer":
            self.socket.connect(self.endpoint)
            logger.info(f"Connected DEALER socket to {self.endpoint}")
        else:
            self.socket.bind(self.endpoint)
            logger.info(f"Bound ROUTER socket to {self.endpoint}")

        self._running = True

    async def disconnect(self):
        """Disconnect from ZeroMQ endpoint."""
        self._running = False

        # Cancel pending replies
        for future in self._pending_replies.values():
            if not future.done():
                future.cancel()
        self._pending_replies.clear()

        # Close socket
        if self.socket:
            self.socket.close()
            self.socket = None

        logger.info(f"ZeroMQ client disconnected: identity={self.identity.decode()}")

    async def send(self, message: AgentMessage) -> None:
        """
        Send a message.

        Args:
            message: Message to send

        Raises:
            RuntimeError: If not connected
        """
        if not self.socket:
            raise RuntimeError("Not connected")

        # Serialize message
        data = message.to_bytes()

        # Send based on socket type
        if self.mode == "dealer":
            # DEALER sends directly
            await self.socket.send(data)
        else:
            # ROUTER sends to specific recipient
            if not message.recipient:
                raise ValueError("Recipient required for ROUTER socket")

            recipient = message.recipient.encode()
            await self.socket.send_multipart([recipient, data])

        logger.debug(f"Sent message: {message}")

    async def recv(self, timeout: Optional[float] = None) -> AgentMessage:
        """
        Receive a message.

        Args:
            timeout: Optional timeout in seconds

        Returns:
            Received message

        Raises:
            RuntimeError: If not connected
            asyncio.TimeoutError: If timeout exceeded
        """
        if not self.socket:
            raise RuntimeError("Not connected")

        try:
            # Receive based on socket type
            if self.mode == "dealer":
                # DEALER receives directly
                if timeout:
                    data = await asyncio.wait_for(
                        self.socket.recv(),
                        timeout=timeout
                    )
                else:
                    data = await self.socket.recv()

            else:
                # ROUTER receives with sender identity
                if timeout:
                    frames = await asyncio.wait_for(
                        self.socket.recv_multipart(),
                        timeout=timeout
                    )
                else:
                    frames = await self.socket.recv_multipart()

                # Extract data from frames (skip identity frame)
                data = frames[-1]

            # Deserialize message
            message = AgentMessage.from_bytes(data)
            logger.debug(f"Received message: {message}")

            return message

        except zmq.Again:
            raise asyncio.TimeoutError("Receive timeout")

    async def request(
        self,
        message: AgentMessage,
        timeout: float = 30.0,
    ) -> AgentMessage:
        """
        Send a request and wait for response.

        Args:
            message: Request message
            timeout: Response timeout in seconds

        Returns:
            Response message

        Raises:
            asyncio.TimeoutError: If response not received in time
        """
        if not self.socket:
            raise RuntimeError("Not connected")

        # Create future for response
        future = asyncio.Future()
        self._pending_replies[message.message_id] = future

        try:
            # Send request
            await self.send(message)

            # Wait for response
            response = await asyncio.wait_for(future, timeout=timeout)
            return response

        finally:
            # Cleanup
            if message.message_id in self._pending_replies:
                del self._pending_replies[message.message_id]

    async def reply(self, request: AgentMessage, response: AgentMessage):
        """
        Send a reply to a request.

        Args:
            request: Original request message
            response: Response message
        """
        # Ensure correlation
        response.correlation_id = request.message_id
        response.recipient = request.sender

        await self.send(response)

    async def listen(self) -> AsyncIterator[AgentMessage]:
        """
        Listen for incoming messages.

        Yields:
            Incoming messages
        """
        if not self.socket:
            raise RuntimeError("Not connected")

        while self._running:
            try:
                message = await self.recv(timeout=1.0)

                # Check if this is a reply to a pending request
                if message.correlation_id and message.correlation_id in self._pending_replies:
                    future = self._pending_replies[message.correlation_id]
                    if not future.done():
                        future.set_result(message)
                else:
                    # Yield message for processing
                    yield message

            except asyncio.TimeoutError:
                # Timeout is expected, continue listening
                continue
            except Exception as e:
                logger.exception(f"Error receiving message: {e}")
                if self._running:
                    await asyncio.sleep(1.0)

    async def send_heartbeat(self):
        """Send a heartbeat message."""
        heartbeat = AgentMessage(
            message_type=MessageType.HEARTBEAT,
            sender=self.identity.decode(),
            payload={"timestamp": asyncio.get_event_loop().time()},
        )
        await self.send(heartbeat)

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
