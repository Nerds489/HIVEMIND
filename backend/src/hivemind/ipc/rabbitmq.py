"""
HIVEMIND RabbitMQ Client

RabbitMQ client with Dead Letter Queue (DLQ) support for reliable message queuing.
Provides async publishing, consuming, and automatic retry with DLQ fallback.
"""

import asyncio
from typing import AsyncIterator, Callable, Optional

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.abc import AbstractIncomingMessage

from hivemind.config import get_settings
from hivemind.ipc.base import AgentMessage, MessagePriority
from hivemind.observability import get_logger

logger = get_logger(__name__)


class RabbitMQClient:
    """
    RabbitMQ client for reliable message queuing.

    Features:
    - Persistent message delivery
    - Dead Letter Queue (DLQ) for failed messages
    - Priority queues
    - Automatic retries
    - Message acknowledgment
    """

    def __init__(self):
        """Initialize RabbitMQ client."""
        self.settings = get_settings()
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None
        self.task_queue: Optional[aio_pika.Queue] = None
        self.dlq_queue: Optional[aio_pika.Queue] = None
        self.event_exchange: Optional[aio_pika.Exchange] = None
        self._consuming = False

        logger.info("RabbitMQ client initialized")

    async def connect(self):
        """Connect to RabbitMQ server and set up queues."""
        if self.connection:
            logger.warning("Already connected to RabbitMQ")
            return

        # Establish connection
        self.connection = await aio_pika.connect_robust(
            self.settings.rabbitmq.url,
            timeout=self.settings.rabbitmq.connection_timeout,
            heartbeat=self.settings.rabbitmq.heartbeat,
        )

        # Create channel
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

        # Declare Dead Letter Queue
        self.dlq_queue = await self.channel.declare_queue(
            self.settings.rabbitmq.dlq_queue,
            durable=True,
        )

        # Declare main task queue with DLQ configuration
        self.task_queue = await self.channel.declare_queue(
            self.settings.rabbitmq.task_queue,
            durable=True,
            arguments={
                "x-dead-letter-exchange": "",
                "x-dead-letter-routing-key": self.settings.rabbitmq.dlq_queue,
                "x-message-ttl": self.settings.rabbitmq.message_ttl,
                "x-max-priority": MessagePriority.CRITICAL.value,
            },
        )

        # Declare event exchange
        self.event_exchange = await self.channel.declare_exchange(
            self.settings.rabbitmq.event_exchange,
            ExchangeType.TOPIC,
            durable=True,
        )

        logger.info(
            f"Connected to RabbitMQ at {self.settings.rabbitmq.host}:{self.settings.rabbitmq.port}"
        )

    async def disconnect(self):
        """Disconnect from RabbitMQ server."""
        self._consuming = False

        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.task_queue = None
            self.dlq_queue = None
            self.event_exchange = None

        logger.info("Disconnected from RabbitMQ")

    async def publish_task(
        self,
        message: AgentMessage,
        routing_key: Optional[str] = None,
    ) -> None:
        """
        Publish a task message to the task queue.

        Args:
            message: Message to publish
            routing_key: Optional routing key (uses default queue if None)

        Raises:
            RuntimeError: If not connected
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        # Serialize message
        body = message.to_bytes()

        # Create AMQP message with priority and persistence
        amqp_message = Message(
            body,
            delivery_mode=DeliveryMode.PERSISTENT,
            priority=message.priority.value,
            message_id=message.message_id,
            correlation_id=message.correlation_id,
            timestamp=int(message.timestamp.timestamp()),
            headers={
                "sender": message.sender,
                "recipient": message.recipient,
                "message_type": message.message_type.value,
                "retry_count": message.retry_count,
                **message.headers,
            },
        )

        # Publish to queue
        if routing_key:
            await self.channel.default_exchange.publish(
                amqp_message,
                routing_key=routing_key,
            )
        else:
            await self.channel.default_exchange.publish(
                amqp_message,
                routing_key=self.settings.rabbitmq.task_queue,
            )

        logger.debug(f"Published task message: {message}")

    async def publish_event(
        self,
        message: AgentMessage,
        routing_key: str,
    ) -> None:
        """
        Publish an event message to the event exchange.

        Args:
            message: Event message to publish
            routing_key: Routing key for topic exchange (e.g., "agent.started")

        Raises:
            RuntimeError: If not connected
        """
        if not self.event_exchange:
            raise RuntimeError("Not connected to RabbitMQ")

        # Serialize message
        body = message.to_bytes()

        # Create AMQP message
        amqp_message = Message(
            body,
            delivery_mode=DeliveryMode.PERSISTENT,
            message_id=message.message_id,
            timestamp=int(message.timestamp.timestamp()),
            headers={
                "sender": message.sender,
                "message_type": message.message_type.value,
                **message.headers,
            },
        )

        # Publish to exchange
        await self.event_exchange.publish(
            amqp_message,
            routing_key=routing_key,
        )

        logger.debug(f"Published event to {routing_key}: {message}")

    async def consume_tasks(
        self,
        callback: Callable[[AgentMessage], asyncio.coroutine],
        auto_ack: bool = False,
    ) -> None:
        """
        Consume tasks from the task queue.

        Args:
            callback: Async callback function to process messages
            auto_ack: Whether to automatically acknowledge messages

        Raises:
            RuntimeError: If not connected
        """
        if not self.task_queue:
            raise RuntimeError("Not connected to RabbitMQ")

        self._consuming = True

        async def process_message(raw_message: AbstractIncomingMessage):
            """Process incoming message with retry and DLQ logic."""
            try:
                # Deserialize message
                message = AgentMessage.from_bytes(raw_message.body)

                logger.debug(f"Processing task message: {message}")

                # Call user callback
                await callback(message)

                # Acknowledge message if not auto-ack
                if not auto_ack:
                    await raw_message.ack()

            except Exception as e:
                logger.exception(f"Error processing message: {e}")

                # Check if we should retry
                retry_count = raw_message.headers.get("retry_count", 0)

                if retry_count < self.settings.rabbitmq.max_retries:
                    # Reject and requeue for retry
                    logger.info(f"Requeuing message (retry {retry_count + 1})")
                    await raw_message.reject(requeue=True)
                else:
                    # Max retries exceeded, send to DLQ
                    logger.error(f"Max retries exceeded, sending to DLQ: {message}")
                    await raw_message.reject(requeue=False)

        # Start consuming
        await self.task_queue.consume(process_message, no_ack=auto_ack)

        logger.info(f"Started consuming tasks from {self.settings.rabbitmq.task_queue}")

    async def consume_events(
        self,
        callback: Callable[[str, AgentMessage], asyncio.coroutine],
        routing_keys: list[str],
        queue_name: Optional[str] = None,
    ) -> None:
        """
        Consume events from the event exchange.

        Args:
            callback: Async callback function (routing_key, message)
            routing_keys: List of routing key patterns to subscribe to
            queue_name: Optional queue name (auto-generated if None)

        Raises:
            RuntimeError: If not connected
        """
        if not self.event_exchange or not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        # Declare temporary queue for events
        queue = await self.channel.declare_queue(
            queue_name or "",
            durable=False,
            exclusive=not bool(queue_name),
            auto_delete=not bool(queue_name),
        )

        # Bind queue to exchange with routing keys
        for routing_key in routing_keys:
            await queue.bind(self.event_exchange, routing_key=routing_key)

        async def process_event(raw_message: AbstractIncomingMessage):
            """Process incoming event."""
            try:
                # Deserialize message
                message = AgentMessage.from_bytes(raw_message.body)

                # Extract routing key
                routing_key = raw_message.routing_key or ""

                logger.debug(f"Processing event {routing_key}: {message}")

                # Call user callback
                await callback(routing_key, message)

                # Acknowledge
                await raw_message.ack()

            except Exception as e:
                logger.exception(f"Error processing event: {e}")
                await raw_message.reject(requeue=False)

        # Start consuming
        await queue.consume(process_event)

        logger.info(f"Started consuming events with routing keys: {routing_keys}")

    async def listen_tasks(self) -> AsyncIterator[AgentMessage]:
        """
        Listen for task messages.

        Yields:
            Task messages from the queue
        """
        if not self.task_queue:
            raise RuntimeError("Not connected to RabbitMQ")

        self._consuming = True

        async with self.task_queue.iterator() as queue_iter:
            async for raw_message in queue_iter:
                if not self._consuming:
                    break

                try:
                    # Deserialize message
                    message = AgentMessage.from_bytes(raw_message.body)

                    logger.debug(f"Received task message: {message}")

                    # Yield message for processing
                    yield message

                    # Acknowledge
                    await raw_message.ack()

                except Exception as e:
                    logger.exception(f"Error processing message: {e}")
                    await raw_message.reject(requeue=False)

    async def get_queue_stats(self) -> dict:
        """
        Get statistics about queues.

        Returns:
            Dictionary with queue statistics
        """
        if not self.task_queue or not self.dlq_queue:
            raise RuntimeError("Not connected to RabbitMQ")

        # Declare queues passively to get stats
        task_queue_info = await self.channel.declare_queue(
            self.settings.rabbitmq.task_queue,
            passive=True,
        )

        dlq_queue_info = await self.channel.declare_queue(
            self.settings.rabbitmq.dlq_queue,
            passive=True,
        )

        return {
            "task_queue": {
                "name": self.settings.rabbitmq.task_queue,
                "message_count": task_queue_info.declaration_result.message_count,
                "consumer_count": task_queue_info.declaration_result.consumer_count,
            },
            "dlq_queue": {
                "name": self.settings.rabbitmq.dlq_queue,
                "message_count": dlq_queue_info.declaration_result.message_count,
                "consumer_count": dlq_queue_info.declaration_result.consumer_count,
            },
        }

    async def purge_queue(self, queue_name: Optional[str] = None):
        """
        Purge all messages from a queue.

        Args:
            queue_name: Queue to purge (task_queue if None)
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        target_queue = queue_name or self.settings.rabbitmq.task_queue

        queue = await self.channel.declare_queue(target_queue, passive=True)
        await queue.purge()

        logger.info(f"Purged queue: {target_queue}")

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
