"""
Dead Letter Queue Management

Handles failed tasks by routing them to a dead letter queue for later
inspection, retry, or manual intervention.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import aio_pika

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)


class DLQManager:
    """
    Dead Letter Queue manager for failed tasks.

    Routes failed messages to a separate queue for manual inspection
    and potential reprocessing.
    """

    def __init__(self):
        """Initialize DLQ manager."""
        self.settings = get_settings()
        self._connection: aio_pika.Connection | None = None
        self._channel: aio_pika.Channel | None = None
        self._dlq_queue: aio_pika.Queue | None = None

    async def connect(self) -> None:
        """Connect to RabbitMQ and set up DLQ."""
        if self._connection and not self._connection.is_closed:
            return

        rabbitmq = self.settings.rabbitmq

        try:
            self._connection = await aio_pika.connect_robust(
                rabbitmq.url,
                timeout=rabbitmq.connection_timeout,
            )

            self._channel = await self._connection.channel()

            # Declare DLQ with persistence
            self._dlq_queue = await self._channel.declare_queue(
                rabbitmq.dlq_queue,
                durable=True,
                arguments={
                    "x-message-ttl": rabbitmq.message_ttl,
                    "x-max-length": 10000,  # Limit queue size
                },
            )

            logger.info(
                f"DLQ manager connected to queue '{rabbitmq.dlq_queue}'",
                extra={"dlq_queue": rabbitmq.dlq_queue},
            )

        except Exception as e:
            logger.error(
                f"Failed to connect to DLQ: {e}",
                extra={"error": str(e)},
            )
            raise

    async def disconnect(self) -> None:
        """Disconnect from RabbitMQ."""
        if self._channel:
            await self._channel.close()
            self._channel = None

        if self._connection:
            await self._connection.close()
            self._connection = None

        logger.info("DLQ manager disconnected")

    async def send_to_dlq(
        self,
        message_body: dict[str, Any],
        original_queue: str,
        error: Exception,
        retry_count: int = 0,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Send failed message to dead letter queue.

        Args:
            message_body: Original message content
            original_queue: Queue where message originally failed
            error: Exception that caused the failure
            retry_count: Number of retry attempts made
            metadata: Additional metadata to attach
        """
        if not self._channel or not self._dlq_queue:
            await self.connect()

        # Build DLQ message with failure metadata
        dlq_message = {
            "original_message": message_body,
            "original_queue": original_queue,
            "error": {
                "type": type(error).__name__,
                "message": str(error),
            },
            "retry_count": retry_count,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }

        try:
            # Publish to DLQ
            message = aio_pika.Message(
                body=json.dumps(dlq_message).encode("utf-8"),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={
                    "x-original-queue": original_queue,
                    "x-error-type": type(error).__name__,
                    "x-retry-count": retry_count,
                },
            )

            await self._channel.default_exchange.publish(
                message,
                routing_key=self._dlq_queue.name,
            )

            logger.warning(
                f"Message sent to DLQ from queue '{original_queue}'",
                extra={
                    "original_queue": original_queue,
                    "error_type": type(error).__name__,
                    "retry_count": retry_count,
                    "message_preview": str(message_body)[:100],
                },
            )

        except Exception as e:
            logger.error(
                f"Failed to send message to DLQ: {e}",
                extra={
                    "error": str(e),
                    "original_queue": original_queue,
                },
            )
            raise

    async def get_dlq_messages(self, limit: int = 100) -> list[dict[str, Any]]:
        """
        Retrieve messages from DLQ without removing them.

        Args:
            limit: Maximum number of messages to retrieve

        Returns:
            List of DLQ messages
        """
        if not self._channel or not self._dlq_queue:
            await self.connect()

        messages = []
        count = 0

        try:
            async for message in self._dlq_queue.iterator():
                async with message.process(requeue=True):
                    # Parse message body
                    try:
                        msg_data = json.loads(message.body.decode("utf-8"))
                        messages.append(msg_data)
                        count += 1

                        if count >= limit:
                            break

                    except json.JSONDecodeError as e:
                        logger.error(
                            f"Failed to parse DLQ message: {e}",
                            extra={"error": str(e)},
                        )

        except Exception as e:
            logger.error(
                f"Failed to retrieve DLQ messages: {e}",
                extra={"error": str(e)},
            )

        return messages

    async def requeue_message(self, message_id: str, target_queue: str) -> None:
        """
        Requeue a message from DLQ to original or different queue.

        Args:
            message_id: ID of message to requeue
            target_queue: Queue to send message to
        """
        if not self._channel:
            await self.connect()

        # This is simplified - in production you'd need message ID tracking
        logger.warning(
            f"Requeue operation not fully implemented for message {message_id}",
            extra={"message_id": message_id, "target_queue": target_queue},
        )

    async def purge_dlq(self) -> int:
        """
        Remove all messages from DLQ.

        Returns:
            Number of messages purged
        """
        if not self._dlq_queue:
            await self.connect()

        try:
            result = await self._dlq_queue.purge()
            logger.warning(
                f"Purged {result} messages from DLQ",
                extra={"purged_count": result},
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to purge DLQ: {e}",
                extra={"error": str(e)},
            )
            raise


# Global DLQ manager instance
_dlq_manager: DLQManager | None = None


async def get_dlq_manager() -> DLQManager:
    """
    Get or create global DLQ manager instance.

    Returns:
        DLQ manager instance
    """
    global _dlq_manager

    if _dlq_manager is None:
        _dlq_manager = DLQManager()
        await _dlq_manager.connect()

    return _dlq_manager


async def send_to_dlq(
    message_body: dict[str, Any],
    original_queue: str,
    error: Exception,
    retry_count: int = 0,
    metadata: dict[str, Any] | None = None,
) -> None:
    """
    Convenience function to send message to DLQ.

    Args:
        message_body: Original message content
        original_queue: Queue where message originally failed
        error: Exception that caused the failure
        retry_count: Number of retry attempts made
        metadata: Additional metadata to attach
    """
    manager = await get_dlq_manager()
    await manager.send_to_dlq(
        message_body=message_body,
        original_queue=original_queue,
        error=error,
        retry_count=retry_count,
        metadata=metadata,
    )
