"""
HIVEMIND Completion Routes

API endpoints for task submission and completion.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hivemind.api.dependencies import get_coordinator, get_current_user
from hivemind.api.schemas import (
    AgentResultResponse,
    CompletionRequest,
    CompletionResponse,
    CompletionResult,
    TaskState,
    TaskStatusResponse,
)
from hivemind.core.coordinator import Coordinator, TaskPriority
from hivemind.observability import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/v1/completions", tags=["Completions"])


# Map API priority enum to internal priority enum
PRIORITY_MAP = {
    "low": TaskPriority.LOW,
    "normal": TaskPriority.NORMAL,
    "high": TaskPriority.HIGH,
    "critical": TaskPriority.CRITICAL,
}


@router.post(
    "",
    response_model=CompletionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a task for processing",
    description="Submit a prompt to the HIVEMIND system for processing by appropriate agents",
)
async def create_completion(
    request: CompletionRequest,
    coordinator: Coordinator = Depends(get_coordinator),
    current_user: str | None = Depends(get_current_user),
) -> CompletionResponse:
    """
    Submit a task for processing.

    Args:
        request: Completion request
        coordinator: Coordinator dependency
        current_user: Current user (if authenticated)

    Returns:
        Task submission response with task ID
    """
    # Use current_user if not explicitly provided
    user_id = request.user_id or current_user

    # Map priority
    priority = PRIORITY_MAP.get(request.priority.value, TaskPriority.NORMAL)

    # Create task (don't process yet, just create)
    task = coordinator.create_task(
        prompt=request.prompt,
        priority=priority,
        session_id=request.session_id,
        user_id=user_id,
    )

    logger.info(
        "Task created via API",
        task_id=task.id,
        session_id=request.session_id,
        user_id=user_id,
    )

    # Process task asynchronously (in background)
    # For now, we'll process it immediately
    # In production, you might want to use a background task
    import asyncio
    asyncio.create_task(_process_task_background(coordinator, task.id))

    return CompletionResponse(
        task_id=task.id,
        state=TaskState.PENDING,
        message="Task submitted successfully",
    )


async def _process_task_background(coordinator: Coordinator, task_id: str) -> None:
    """
    Process a task in the background.

    Args:
        coordinator: Coordinator instance
        task_id: Task ID to process
    """
    try:
        task = coordinator.get_task(task_id)
        if not task:
            logger.error("Task not found for background processing", task_id=task_id)
            return

        # Analyze and extract keywords
        coordinator.analyze_task(task)

        # Route to teams/agents
        routes = await coordinator.route_task(task)

        if not routes:
            task.error = "No suitable agents found for task"
            task.transition_to(TaskState.FAILED)
            return

        # Execute task
        await coordinator.execute_task(task, routes)

        # Synthesize response
        coordinator.synthesize_response(task)

        logger.info("Task processed in background", task_id=task_id, state=task.state.value)

    except Exception as e:
        logger.exception("Background task processing failed", task_id=task_id, error=str(e))


@router.get(
    "/{task_id}",
    response_model=TaskStatusResponse,
    summary="Get task status",
    description="Retrieve the status and details of a task",
)
async def get_task_status(
    task_id: str,
    coordinator: Coordinator = Depends(get_coordinator),
    current_user: str | None = Depends(get_current_user),
) -> TaskStatusResponse:
    """
    Get task status and details.

    Args:
        task_id: Task ID
        coordinator: Coordinator dependency
        current_user: Current user (if authenticated)

    Returns:
        Task status information

    Raises:
        HTTPException: If task not found
    """
    task = coordinator.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found: {task_id}",
        )

    # Optional: Check user authorization
    # if current_user and task.user_id != current_user:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    # Convert task state to API state
    state = TaskState(task.state.value)

    # Convert results
    results = [
        AgentResultResponse(
            agent_id=r.agent_id,
            team_id=r.team_id,
            success=r.success,
            execution_time=r.execution_time,
        )
        for r in task.results
    ]

    return TaskStatusResponse(
        task_id=task.id,
        state=state,
        prompt=task.prompt,
        priority=task.priority.name.lower(),
        created_at=task.created_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        duration=task.duration,
        target_teams=[t.value for t in task.target_teams],
        target_agents=task.target_agents,
        keywords=task.keywords,
        results=results,
        error=task.error,
        session_id=task.session_id,
    )


@router.get(
    "/{task_id}/result",
    response_model=CompletionResult,
    summary="Get task result",
    description="Retrieve the final result and synthesized response from a completed task",
)
async def get_task_result(
    task_id: str,
    coordinator: Coordinator = Depends(get_coordinator),
    current_user: str | None = Depends(get_current_user),
) -> CompletionResult:
    """
    Get task result.

    Args:
        task_id: Task ID
        coordinator: Coordinator dependency
        current_user: Current user (if authenticated)

    Returns:
        Task result with synthesized response

    Raises:
        HTTPException: If task not found or not completed
    """
    task = coordinator.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found: {task_id}",
        )

    # Optional: Check user authorization
    # if current_user and task.user_id != current_user:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    # Check if task is complete
    if not task.is_complete:
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=f"Task not yet complete: {task.state.value}",
        )

    # Convert task state
    state = TaskState(task.state.value)

    # Get synthesized response
    response = task.synthesized_response

    # If task failed, use error as response
    if task.error:
        response = None

    return CompletionResult(
        task_id=task.id,
        state=state,
        prompt=task.prompt,
        response=response,
        error=task.error,
        duration=task.duration,
        created_at=task.created_at,
        completed_at=task.completed_at,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel task",
    description="Cancel a running task",
)
async def cancel_task(
    task_id: str,
    coordinator: Coordinator = Depends(get_coordinator),
    current_user: str | None = Depends(get_current_user),
) -> None:
    """
    Cancel a task.

    Args:
        task_id: Task ID
        coordinator: Coordinator dependency
        current_user: Current user (if authenticated)

    Raises:
        HTTPException: If task not found or already complete
    """
    task = coordinator.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found: {task_id}",
        )

    # Optional: Check user authorization
    # if current_user and task.user_id != current_user:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    # Check if task can be cancelled
    if task.is_complete:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task already complete: {task.state.value}",
        )

    # Cancel task
    cancelled = await coordinator.cancel_task(task_id)

    if not cancelled:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel task",
        )

    logger.info("Task cancelled via API", task_id=task_id, user_id=task.user_id)


@router.get(
    "",
    response_model=list[TaskStatusResponse],
    summary="List tasks",
    description="List all tasks, optionally filtered by session or state",
)
async def list_tasks(
    session_id: str | None = None,
    state: TaskState | None = None,
    limit: int = 100,
    coordinator: Coordinator = Depends(get_coordinator),
    current_user: str | None = Depends(get_current_user),
) -> list[TaskStatusResponse]:
    """
    List tasks.

    Args:
        session_id: Optional filter by session ID
        state: Optional filter by task state
        limit: Maximum number of tasks to return
        coordinator: Coordinator dependency
        current_user: Current user (if authenticated)

    Returns:
        List of tasks
    """
    # Get tasks
    if session_id:
        tasks = coordinator.get_tasks_by_session(session_id)
    elif state:
        from hivemind.core.coordinator import TaskState as InternalTaskState
        internal_state = InternalTaskState(state.value)
        tasks = coordinator.get_tasks_by_state(internal_state)
    else:
        tasks = coordinator.get_all_tasks()

    # Limit results
    tasks = tasks[:limit]

    # Convert to response models
    return [
        TaskStatusResponse(
            task_id=task.id,
            state=TaskState(task.state.value),
            prompt=task.prompt,
            priority=task.priority.name.lower(),
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            duration=task.duration,
            target_teams=[t.value for t in task.target_teams],
            target_agents=task.target_agents,
            keywords=task.keywords,
            results=[
                AgentResultResponse(
                    agent_id=r.agent_id,
                    team_id=r.team_id,
                    success=r.success,
                    execution_time=r.execution_time,
                )
                for r in task.results
            ],
            error=task.error,
            session_id=task.session_id,
        )
        for task in tasks
    ]
