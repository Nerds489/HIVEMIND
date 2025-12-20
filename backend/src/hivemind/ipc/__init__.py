"""
HIVEMIND IPC Module

Inter-process communication layer supporting multiple transport mechanisms:
- ZeroMQ (DEALER/ROUTER) for request-reply patterns
- Redis Pub/Sub for broadcasting
- RabbitMQ for reliable message queuing with DLQ
"""

from hivemind.ipc.base import AgentMessage, MessageType, MessagePriority
from hivemind.ipc.zeromq import ZeroMQClient
from hivemind.ipc.redis import RedisPubSub
from hivemind.ipc.rabbitmq import RabbitMQClient

__all__ = [
    "AgentMessage",
    "MessageType",
    "MessagePriority",
    "ZeroMQClient",
    "RedisPubSub",
    "RabbitMQClient",
]
