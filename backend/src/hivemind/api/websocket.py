"""
HIVEMIND WebSocket Handler

Real-time streaming interface for task updates and results.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from hivemind.api.schemas import (
    WSError,
    WSMessage,
    WSMessageType,
    WSSubscribeRequest,
    WSTaskResult,
    WSTaskUpdate,
    WSUnsubscribeRequest,
)
from hivemind.observability import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["WebSocket"])


class ConnectionManager:
    """
    Manages WebSocket connections and message broadcasting.

    Handles connection lifecycle, subscriptions, and message routing.
    """

    def __init__(self) -> None:
        """Initialize the connection manager."""
        # Active connections: websocket -> client_id
        self.active_connections: dict[WebSocket, str] = {}

        # Task subscriptions: task_id -> set of websockets
        self.task_subscriptions: dict[str, set[WebSocket]] = {}

        # Client info: client_id -> metadata
        self.client_info: dict[str, dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """
        Accept a new WebSocket connection.

        Args:
            websocket: WebSocket connection
            client_id: Unique client identifier
        """
        await websocket.accept()
        self.active_connections[websocket] = client_id
        self.client_info[client_id] = {
            "connected_at": datetime.utcnow(),
            "subscriptions": set(),
        }

        logger.info(
            "WebSocket connected",
            client_id=client_id,
            total_connections=len(self.active_connections),
        )

        # Send welcome message
        await self._send_message(
            websocket,
            WSMessage(
                type=WSMessageType.CONNECT,
                data={"client_id": client_id, "message": "Connected to HIVEMIND"},
            ),
        )

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove a WebSocket connection.

        Args:
            websocket: WebSocket connection to remove
        """
        client_id = self.active_connections.pop(websocket, None)

        if client_id:
            # Remove from all task subscriptions
            for task_subscribers in self.task_subscriptions.values():
                task_subscribers.discard(websocket)

            # Clean up empty subscription sets
            self.task_subscriptions = {
                task_id: subscribers
                for task_id, subscribers in self.task_subscriptions.items()
                if subscribers
            }

            # Remove client info
            self.client_info.pop(client_id, None)

            logger.info(
                "WebSocket disconnected",
                client_id=client_id,
                total_connections=len(self.active_connections),
            )

    async def subscribe_to_task(self, websocket: WebSocket, task_id: str) -> None:
        """
        Subscribe a connection to task updates.

        Args:
            websocket: WebSocket connection
            task_id: Task ID to subscribe to
        """
        if task_id not in self.task_subscriptions:
            self.task_subscriptions[task_id] = set()

        self.task_subscriptions[task_id].add(websocket)

        client_id = self.active_connections.get(websocket)
        if client_id and client_id in self.client_info:
            self.client_info[client_id]["subscriptions"].add(task_id)

        logger.debug(
            "Client subscribed to task",
            client_id=client_id,
            task_id=task_id,
        )

        # Send confirmation
        await self._send_message(
            websocket,
            WSMessage(
                type=WSMessageType.SUBSCRIBE,
                data={"task_id": task_id, "message": "Subscribed to task updates"},
            ),
        )

    async def unsubscribe_from_task(self, websocket: WebSocket, task_id: str) -> None:
        """
        Unsubscribe a connection from task updates.

        Args:
            websocket: WebSocket connection
            task_id: Task ID to unsubscribe from
        """
        if task_id in self.task_subscriptions:
            self.task_subscriptions[task_id].discard(websocket)

            if not self.task_subscriptions[task_id]:
                del self.task_subscriptions[task_id]

        client_id = self.active_connections.get(websocket)
        if client_id and client_id in self.client_info:
            self.client_info[client_id]["subscriptions"].discard(task_id)

        logger.debug(
            "Client unsubscribed from task",
            client_id=client_id,
            task_id=task_id,
        )

        # Send confirmation
        await self._send_message(
            websocket,
            WSMessage(
                type=WSMessageType.UNSUBSCRIBE,
                data={"task_id": task_id, "message": "Unsubscribed from task updates"},
            ),
        )

    async def broadcast_task_update(
        self,
        task_id: str,
        state: str,
        progress: float | None = None,
        message: str | None = None,
    ) -> None:
        """
        Broadcast a task update to all subscribers.

        Args:
            task_id: Task ID
            state: Task state
            progress: Optional progress percentage (0-100)
            message: Optional status message
        """
        if task_id not in self.task_subscriptions:
            return

        update = WSTaskUpdate(
            task_id=task_id,
            state=state,
            progress=progress,
            message=message,
        )

        ws_message = WSMessage(
            type=WSMessageType.TASK_UPDATE,
            data=update.model_dump(),
        )

        await self._broadcast_to_subscribers(task_id, ws_message)

    async def broadcast_task_result(
        self,
        task_id: str,
        state: str,
        response: str | None = None,
        error: str | None = None,
    ) -> None:
        """
        Broadcast a task result to all subscribers.

        Args:
            task_id: Task ID
            state: Final task state
            response: Task response
            error: Error message if failed
        """
        if task_id not in self.task_subscriptions:
            return

        result = WSTaskResult(
            task_id=task_id,
            state=state,
            response=response,
            error=error,
        )

        ws_message = WSMessage(
            type=WSMessageType.TASK_RESULT,
            data=result.model_dump(),
        )

        await self._broadcast_to_subscribers(task_id, ws_message)

    async def _broadcast_to_subscribers(
        self,
        task_id: str,
        message: WSMessage,
    ) -> None:
        """
        Broadcast a message to task subscribers.

        Args:
            task_id: Task ID
            message: Message to broadcast
        """
        subscribers = self.task_subscriptions.get(task_id, set())

        # Send to all subscribers (remove disconnected ones)
        disconnected = []
        for websocket in subscribers:
            try:
                await self._send_message(websocket, message)
            except Exception as e:
                logger.error(
                    "Failed to send to subscriber",
                    task_id=task_id,
                    error=str(e),
                )
                disconnected.append(websocket)

        # Clean up disconnected clients
        for websocket in disconnected:
            await self.unsubscribe_from_task(websocket, task_id)

    async def _send_message(self, websocket: WebSocket, message: WSMessage) -> None:
        """
        Send a message to a WebSocket connection.

        Args:
            websocket: WebSocket connection
            message: Message to send
        """
        await websocket.send_json(message.model_dump())

    async def send_error(
        self,
        websocket: WebSocket,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Send an error message to a connection.

        Args:
            websocket: WebSocket connection
            code: Error code
            message: Error message
            details: Optional error details
        """
        error = WSError(
            code=code,
            message=message,
            details=details or {},
        )

        ws_message = WSMessage(
            type=WSMessageType.ERROR,
            data=error.model_dump(),
        )

        await self._send_message(websocket, ws_message)

    async def ping_all(self) -> None:
        """Send ping to all connected clients."""
        ping_message = WSMessage(type=WSMessageType.PING, data={})

        disconnected = []
        for websocket in list(self.active_connections.keys()):
            try:
                await self._send_message(websocket, ping_message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(websocket)

    def get_stats(self) -> dict[str, Any]:
        """
        Get connection statistics.

        Returns:
            Dictionary with stats
        """
        return {
            "total_connections": len(self.active_connections),
            "total_subscriptions": len(self.task_subscriptions),
            "clients": [
                {
                    "client_id": client_id,
                    "connected_at": info["connected_at"].isoformat(),
                    "subscriptions": list(info["subscriptions"]),
                }
                for client_id, info in self.client_info.items()
            ],
        }


# Global connection manager
manager = ConnectionManager()


@router.websocket("/v1/stream")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time streaming.

    Protocol:
    - Client connects
    - Client sends subscribe messages for tasks: {"type": "subscribe", "data": {"task_id": "..."}}
    - Server sends task updates: {"type": "task_update", "data": {...}}
    - Server sends task results: {"type": "task_result", "data": {...}}
    - Client sends unsubscribe messages: {"type": "unsubscribe", "data": {"task_id": "..."}}
    - Client disconnects
    """
    # Generate client ID
    import uuid

    client_id = str(uuid.uuid4())

    await manager.connect(websocket, client_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                # Parse message
                message_data = json.loads(data)
                message_type = message_data.get("type")
                message_payload = message_data.get("data", {})

                logger.debug(
                    "WebSocket message received",
                    client_id=client_id,
                    type=message_type,
                )

                # Handle different message types
                if message_type == "subscribe":
                    # Subscribe to task updates
                    subscribe_req = WSSubscribeRequest(**message_payload)
                    await manager.subscribe_to_task(websocket, subscribe_req.task_id)

                elif message_type == "unsubscribe":
                    # Unsubscribe from task updates
                    unsubscribe_req = WSUnsubscribeRequest(**message_payload)
                    await manager.unsubscribe_from_task(websocket, unsubscribe_req.task_id)

                elif message_type == "ping":
                    # Respond with pong
                    pong_message = WSMessage(type=WSMessageType.PONG, data={})
                    await manager._send_message(websocket, pong_message)

                else:
                    # Unknown message type
                    await manager.send_error(
                        websocket,
                        code="invalid_message_type",
                        message=f"Unknown message type: {message_type}",
                        details={"received_type": message_type},
                    )

            except json.JSONDecodeError as e:
                await manager.send_error(
                    websocket,
                    code="invalid_json",
                    message="Invalid JSON in message",
                    details={"error": str(e)},
                )

            except Exception as e:
                logger.error(
                    "Error processing WebSocket message",
                    client_id=client_id,
                    error=str(e),
                )
                await manager.send_error(
                    websocket,
                    code="processing_error",
                    message="Error processing message",
                    details={"error": str(e)},
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception as e:
        logger.exception(
            "WebSocket error",
            client_id=client_id,
            error=str(e),
        )
        manager.disconnect(websocket)


# Background task to send periodic pings
async def periodic_ping_task() -> None:
    """Send periodic pings to all connected clients."""
    while True:
        await asyncio.sleep(30)  # Ping every 30 seconds
        await manager.ping_all()


# Export manager for use by other modules
__all__ = ["router", "manager", "ConnectionManager"]
