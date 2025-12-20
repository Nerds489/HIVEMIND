"""
HIVEMIND Redis Pub/Sub

Redis Pub/Sub wrapper for broadcasting messages to multiple agents.
Supports channel subscriptions and pattern-based subscriptions.
"""

import asyncio
from typing import AsyncIterator, Optional, Set

import redis.asyncio as aioredis

from hivemind.config import get_settings
from hivemind.ipc.base import AgentMessage
from hivemind.observability import get_logger

logger = get_logger(__name__)


class RedisPubSub:
    """
    Redis Pub/Sub client for agent broadcasting.

    Supports:
    - Publishing messages to channels
    - Subscribing to specific channels
    - Pattern-based subscriptions
    - Message serialization with msgpack
    """

    def __init__(self):
        """Initialize Redis Pub/Sub client."""
        self.settings = get_settings()
        self.redis: Optional[aioredis.Redis] = None
        self.pubsub: Optional[aioredis.client.PubSub] = None
        self._running = False
        self._subscribed_channels: Set[str] = set()
        self._subscribed_patterns: Set[str] = set()

        logger.info("Redis Pub/Sub client initialized")

    async def connect(self):
        """Connect to Redis server."""
        if self.redis:
            logger.warning("Already connected to Redis")
            return

        # Create Redis connection
        self.redis = await aioredis.from_url(
            self.settings.redis.url,
            max_connections=self.settings.redis.max_connections,
            socket_timeout=self.settings.redis.socket_timeout,
            socket_connect_timeout=self.settings.redis.socket_connect_timeout,
            retry_on_timeout=self.settings.redis.retry_on_timeout,
            decode_responses=False,  # We handle msgpack ourselves
        )

        # Create pubsub instance
        self.pubsub = self.redis.pubsub()

        logger.info(f"Connected to Redis at {self.settings.redis.host}:{self.settings.redis.port}")

    async def disconnect(self):
        """Disconnect from Redis server."""
        self._running = False

        # Unsubscribe from all channels
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.punsubscribe()
            await self.pubsub.close()
            self.pubsub = None

        # Close Redis connection
        if self.redis:
            await self.redis.close()
            self.redis = None

        self._subscribed_channels.clear()
        self._subscribed_patterns.clear()

        logger.info("Disconnected from Redis")

    async def publish(self, channel: str, message: AgentMessage) -> int:
        """
        Publish a message to a channel.

        Args:
            channel: Channel name
            message: Message to publish

        Returns:
            Number of subscribers that received the message

        Raises:
            RuntimeError: If not connected
        """
        if not self.redis:
            raise RuntimeError("Not connected to Redis")

        # Add key prefix
        full_channel = f"{self.settings.redis.key_prefix}{channel}"

        # Serialize message
        data = message.to_bytes()

        # Publish to channel
        subscribers = await self.redis.publish(full_channel, data)

        logger.debug(f"Published message to {full_channel}: {message} ({subscribers} subscribers)")

        return subscribers

    async def subscribe(self, *channels: str):
        """
        Subscribe to specific channels.

        Args:
            *channels: Channel names to subscribe to

        Raises:
            RuntimeError: If not connected
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")

        # Add key prefix to channels
        full_channels = [
            f"{self.settings.redis.key_prefix}{channel}"
            for channel in channels
        ]

        # Subscribe
        await self.pubsub.subscribe(*full_channels)
        self._subscribed_channels.update(channels)

        logger.info(f"Subscribed to channels: {', '.join(channels)}")

    async def psubscribe(self, *patterns: str):
        """
        Subscribe to channel patterns.

        Args:
            *patterns: Channel patterns to subscribe to (e.g., "agent.*")

        Raises:
            RuntimeError: If not connected
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")

        # Add key prefix to patterns
        full_patterns = [
            f"{self.settings.redis.key_prefix}{pattern}"
            for pattern in patterns
        ]

        # Subscribe to patterns
        await self.pubsub.psubscribe(*full_patterns)
        self._subscribed_patterns.update(patterns)

        logger.info(f"Subscribed to patterns: {', '.join(patterns)}")

    async def unsubscribe(self, *channels: str):
        """
        Unsubscribe from specific channels.

        Args:
            *channels: Channel names to unsubscribe from
        """
        if not self.pubsub:
            return

        # Add key prefix to channels
        full_channels = [
            f"{self.settings.redis.key_prefix}{channel}"
            for channel in channels
        ]

        await self.pubsub.unsubscribe(*full_channels)
        self._subscribed_channels.difference_update(channels)

        logger.info(f"Unsubscribed from channels: {', '.join(channels)}")

    async def punsubscribe(self, *patterns: str):
        """
        Unsubscribe from channel patterns.

        Args:
            *patterns: Channel patterns to unsubscribe from
        """
        if not self.pubsub:
            return

        # Add key prefix to patterns
        full_patterns = [
            f"{self.settings.redis.key_prefix}{pattern}"
            for pattern in patterns
        ]

        await self.pubsub.punsubscribe(*full_patterns)
        self._subscribed_patterns.difference_update(patterns)

        logger.info(f"Unsubscribed from patterns: {', '.join(patterns)}")

    async def listen(self) -> AsyncIterator[tuple[str, AgentMessage]]:
        """
        Listen for messages on subscribed channels.

        Yields:
            Tuple of (channel, message)

        Raises:
            RuntimeError: If not connected
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")

        self._running = True

        while self._running:
            try:
                # Get next message with timeout
                raw_message = await asyncio.wait_for(
                    self.pubsub.get_message(ignore_subscribe_messages=True),
                    timeout=1.0
                )

                if raw_message is None:
                    # No message available, continue
                    await asyncio.sleep(0.01)
                    continue

                # Extract channel and data
                channel = raw_message["channel"].decode()
                data = raw_message["data"]

                # Remove key prefix
                if channel.startswith(self.settings.redis.key_prefix):
                    channel = channel[len(self.settings.redis.key_prefix):]

                # Deserialize message
                try:
                    message = AgentMessage.from_bytes(data)
                    logger.debug(f"Received message from {channel}: {message}")
                    yield (channel, message)

                except Exception as e:
                    logger.error(f"Failed to deserialize message from {channel}: {e}")
                    continue

            except asyncio.TimeoutError:
                # Timeout is expected, continue listening
                continue

            except Exception as e:
                logger.exception(f"Error receiving message: {e}")
                if self._running:
                    await asyncio.sleep(1.0)

    async def broadcast(
        self,
        pattern: str,
        message: AgentMessage,
    ) -> int:
        """
        Broadcast a message to all matching channels.

        Note: Redis Pub/Sub doesn't directly support pattern publishing.
        This publishes to a single channel that subscribers should pattern-match.

        Args:
            pattern: Channel pattern
            message: Message to broadcast

        Returns:
            Number of subscribers
        """
        return await self.publish(pattern, message)

    def is_subscribed(self, channel: str) -> bool:
        """
        Check if subscribed to a channel.

        Args:
            channel: Channel name

        Returns:
            True if subscribed, False otherwise
        """
        return channel in self._subscribed_channels

    def is_pattern_subscribed(self, pattern: str) -> bool:
        """
        Check if subscribed to a pattern.

        Args:
            pattern: Pattern name

        Returns:
            True if subscribed, False otherwise
        """
        return pattern in self._subscribed_patterns

    @property
    def subscriptions(self) -> Set[str]:
        """Get all subscribed channels."""
        return self._subscribed_channels.copy()

    @property
    def pattern_subscriptions(self) -> Set[str]:
        """Get all subscribed patterns."""
        return self._subscribed_patterns.copy()

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
