"""
HIVEMIND Session Routes

API endpoints for session management and conversation context.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hivemind.api.dependencies import get_context_manager, get_current_user
from hivemind.api.schemas import (
    MessageResponse,
    SessionCreate,
    SessionResponse,
    SessionWithMessages,
)
from hivemind.core.context import ContextManager
from hivemind.observability import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/v1/sessions", tags=["Sessions"])


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new session",
    description="Create a new conversation session with optional user context and metadata",
)
async def create_session(
    request: SessionCreate,
    context_manager: ContextManager = Depends(get_context_manager),
    current_user: str | None = Depends(get_current_user),
) -> SessionResponse:
    """
    Create a new conversation session.

    Args:
        request: Session creation request
        context_manager: Context manager dependency
        current_user: Current user (if authenticated)

    Returns:
        Created session information
    """
    # Use current_user if not explicitly provided
    user_id = request.user_id or current_user

    # Create session
    context = await context_manager.create_session(
        user_id=user_id,
        metadata=request.metadata,
    )

    logger.info(
        "Session created via API",
        session_id=context.session_id,
        user_id=user_id,
    )

    return SessionResponse(
        session_id=context.session_id,
        user_id=context.user_id,
        created_at=context.created_at,
        last_activity=context.last_activity,
        metadata=context.metadata,
        message_count=len(context.messages),
    )


@router.get(
    "/{session_id}",
    response_model=SessionWithMessages,
    summary="Get session details",
    description="Retrieve session information including conversation history",
)
async def get_session(
    session_id: str,
    include_messages: bool = True,
    limit: int | None = None,
    context_manager: ContextManager = Depends(get_context_manager),
    current_user: str | None = Depends(get_current_user),
) -> SessionWithMessages:
    """
    Get session details.

    Args:
        session_id: Session ID
        include_messages: Whether to include messages
        limit: Maximum number of messages to return
        context_manager: Context manager dependency
        current_user: Current user (if authenticated)

    Returns:
        Session information with messages

    Raises:
        HTTPException: If session not found
    """
    context = await context_manager.get_session(session_id)

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    # Optional: Check user authorization
    # if current_user and context.user_id != current_user:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    messages = []
    if include_messages:
        msgs = context.get_messages(limit=limit)
        messages = [
            MessageResponse(
                id=m.id,
                role=m.role,
                content=m.content,
                timestamp=m.timestamp,
                metadata=m.metadata,
            )
            for m in msgs
        ]

    return SessionWithMessages(
        session_id=context.session_id,
        user_id=context.user_id,
        created_at=context.created_at,
        last_activity=context.last_activity,
        metadata=context.metadata,
        message_count=len(context.messages),
        messages=messages,
    )


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete session",
    description="Delete a session and all its conversation history",
)
async def delete_session(
    session_id: str,
    context_manager: ContextManager = Depends(get_context_manager),
    current_user: str | None = Depends(get_current_user),
) -> None:
    """
    Delete a session.

    Args:
        session_id: Session ID
        context_manager: Context manager dependency
        current_user: Current user (if authenticated)

    Raises:
        HTTPException: If session not found
    """
    # Check if session exists
    context = await context_manager.get_session(session_id)

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    # Optional: Check user authorization
    # if current_user and context.user_id != current_user:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    # Delete session
    await context_manager.delete_session(session_id)

    logger.info(
        "Session deleted via API",
        session_id=session_id,
        user_id=context.user_id,
    )


@router.get(
    "/{session_id}/messages",
    response_model=list[MessageResponse],
    summary="Get session messages",
    description="Retrieve conversation messages from a session",
)
async def get_session_messages(
    session_id: str,
    limit: int | None = None,
    roles: list[str] | None = None,
    context_manager: ContextManager = Depends(get_context_manager),
    current_user: str | None = Depends(get_current_user),
) -> list[MessageResponse]:
    """
    Get messages from a session.

    Args:
        session_id: Session ID
        limit: Maximum number of messages to return
        roles: Filter by message roles
        context_manager: Context manager dependency
        current_user: Current user (if authenticated)

    Returns:
        List of messages

    Raises:
        HTTPException: If session not found
    """
    context = await context_manager.get_session(session_id)

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    # Get messages
    messages = context.get_messages(limit=limit, roles=roles)

    return [
        MessageResponse(
            id=m.id,
            role=m.role,
            content=m.content,
            timestamp=m.timestamp,
            metadata=m.metadata,
        )
        for m in messages
    ]


@router.get(
    "",
    response_model=list[SessionResponse],
    summary="List sessions",
    description="List all sessions, optionally filtered by user",
)
async def list_sessions(
    user_id: str | None = None,
    context_manager: ContextManager = Depends(get_context_manager),
    current_user: str | None = Depends(get_current_user),
) -> list[SessionResponse]:
    """
    List all sessions.

    Args:
        user_id: Optional filter by user ID
        context_manager: Context manager dependency
        current_user: Current user (if authenticated)

    Returns:
        List of sessions
    """
    # If authenticated, default to current user's sessions
    if current_user and not user_id:
        user_id = current_user

    session_ids = await context_manager.list_sessions(user_id=user_id)

    sessions = []
    for session_id in session_ids:
        context = await context_manager.get_session(session_id)
        if context:
            sessions.append(
                SessionResponse(
                    session_id=context.session_id,
                    user_id=context.user_id,
                    created_at=context.created_at,
                    last_activity=context.last_activity,
                    metadata=context.metadata,
                    message_count=len(context.messages),
                )
            )

    return sessions
