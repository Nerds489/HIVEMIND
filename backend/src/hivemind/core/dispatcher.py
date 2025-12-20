"""
HIVEMIND Dispatcher

Manages concurrent task execution with semaphore-based concurrency control,
priority queuing, and timeout handling.
"""

from __future__ import annotations

import asyncio
from asyncio import Queue, Semaphore
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from hivemind.agents.base import Agent, AgentState
from hivemind.config import get_settings
from hivemind.observability.logging import LoggerMixin
from hivemind.observability.metrics import get_metrics
from hivemind.observability.tracing import get_tracer

if TYPE_CHECKING:
    from hivemind.core.coordinator import Task, TaskResult, TaskPriority


class ExecutionStatus(str, Enum):
    """Execution status for dispatcher tasks."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class QueuedTask:
    """A task waiting in the dispatcher queue."""
    task: Task
    agent: Agent
    priority: int  # Higher number = higher priority
    queued_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    status: ExecutionStatus = ExecutionStatus.QUEUED

    def __lt__(self, other: QueuedTask) -> bool:
        """Compare queued tasks by priority (higher priority first)."""
        # Higher priority comes first
        if self.priority != other.priority:
            return self.priority > other.priority
        # Earlier queued time comes first for same priority
        return self.queued_at < other.queued_at


class Dispatcher(LoggerMixin):
    """
    Dispatcher for managing concurrent task execution.

    Features:
    - Global, per-team, and per-agent concurrency limits via semaphores
    - Priority-based task queue
    - Task execution with timeout
    - Graceful cancellation
    - Metrics and tracing integration

    Concurrency Control:
    - Global semaphore: Limits total concurrent tasks across all agents
    - Per-team semaphores: Limits concurrent tasks per team
    - Per-agent semaphores: Limits concurrent tasks per agent (typically 1)
    """

    def __init__(
        self,
        max_global_concurrent: int | None = None,
        max_per_team: int | None = None,
        max_per_agent: int | None = None,
        default_timeout: float | None = None,
        executor_fn: Callable[[Task, Agent], Coroutine[Any, Any, TaskResult]] | None = None,
    ) -> None:
        """
        Initialize the Dispatcher.

        Args:
            max_global_concurrent: Maximum concurrent tasks globally
            max_per_team: Maximum concurrent tasks per team
            max_per_agent: Maximum concurrent tasks per agent
            default_timeout: Default task timeout in seconds
            executor_fn: Optional async function to execute tasks
        """
        settings = get_settings()
        concurrency = settings.concurrency

        self.max_global_concurrent = max_global_concurrent or concurrency.max_global_concurrent
        self.max_per_team = max_per_team or concurrency.max_per_team
        self.max_per_agent = max_per_agent or concurrency.max_per_agent
        self.default_timeout = default_timeout or concurrency.default_task_timeout
        self.executor_fn = executor_fn

        # Global semaphore
        self._global_semaphore = Semaphore(self.max_global_concurrent)

        # Per-team semaphores
        self._team_semaphores: dict[str, Semaphore] = {}

        # Per-agent semaphores
        self._agent_semaphores: dict[str, Semaphore] = {}

        # Task queue (priority queue)
        self._queue: asyncio.PriorityQueue[QueuedTask] = asyncio.PriorityQueue()

        # Active tasks
        self._active_tasks: dict[str, asyncio.Task] = {}

        # Metrics and tracing
        self._metrics = get_metrics()
        self._tracer = get_tracer()

        # Dispatcher state
        self._running = False
        self._worker_task: asyncio.Task | None = None

        self.logger.info(
            "Dispatcher initialized",
            max_global=self.max_global_concurrent,
            max_per_team=self.max_per_team,
            max_per_agent=self.max_per_agent,
            default_timeout=self.default_timeout,
        )

    def _get_team_semaphore(self, team_id: str) -> Semaphore:
        """Get or create a semaphore for a team."""
        if team_id not in self._team_semaphores:
            self._team_semaphores[team_id] = Semaphore(self.max_per_team)
        return self._team_semaphores[team_id]

    def _get_agent_semaphore(self, agent_id: str) -> Semaphore:
        """Get or create a semaphore for an agent."""
        if agent_id not in self._agent_semaphores:
            self._agent_semaphores[agent_id] = Semaphore(self.max_per_agent)
        return self._agent_semaphores[agent_id]

    async def submit(
        self,
        task: Task,
        agent: Agent,
        priority: int | None = None,
    ) -> QueuedTask:
        """
        Submit a task for execution.

        Args:
            task: Task to execute
            agent: Agent to execute the task
            priority: Task priority (higher = more important)

        Returns:
            QueuedTask instance
        """
        from hivemind.core.coordinator import TaskPriority

        # Determine priority
        if priority is None:
            priority = task.priority.value if hasattr(task, 'priority') else TaskPriority.NORMAL.value

        queued_task = QueuedTask(
            task=task,
            agent=agent,
            priority=priority,
        )

        # Add to queue
        await self._queue.put(queued_task)

        # Update metrics
        self._metrics.task_queue_size.labels(
            priority=str(priority),
        ).inc()

        self.logger.info(
            "Task submitted to queue",
            task_id=task.id,
            agent_id=agent.id,
            team_id=agent.team,
            priority=priority,
        )

        return queued_task

    async def execute(
        self,
        task: Task,
        agent: Agent,
        timeout: float | None = None,
    ) -> TaskResult:
        """
        Execute a task immediately (bypassing the queue).

        Args:
            task: Task to execute
            agent: Agent to execute the task
            timeout: Execution timeout in seconds

        Returns:
            TaskResult instance
        """
        from hivemind.core.coordinator import TaskResult

        timeout = timeout or self.default_timeout

        with self._tracer.span(
            "dispatcher.execute",
            {"task_id": task.id, "agent_id": agent.id},
        ):
            # Acquire semaphores
            async with self._global_semaphore:
                team_sem = self._get_team_semaphore(agent.team)
                async with team_sem:
                    agent_sem = self._get_agent_semaphore(agent.id)
                    async with agent_sem:
                        # Update agent state
                        agent.assign_task(task.id)
                        agent.start_execution()

                        # Update metrics
                        self._metrics.tasks_in_progress.labels(
                            team=agent.team,
                            agent=agent.id,
                        ).inc()

                        start_time = datetime.utcnow()

                        try:
                            # Execute the task
                            if self.executor_fn:
                                result = await asyncio.wait_for(
                                    self.executor_fn(task, agent),
                                    timeout=timeout,
                                )
                            else:
                                # Default execution - just return success
                                result = TaskResult(
                                    task_id=task.id,
                                    agent_id=agent.id,
                                    team_id=agent.team,
                                    success=True,
                                    output="Task executed (no executor provided)",
                                )

                            execution_time = (datetime.utcnow() - start_time).total_seconds()
                            result.execution_time = execution_time

                            # Update agent state
                            agent.complete_task(success=True)

                            # Update metrics
                            self._metrics.tasks_total.labels(
                                status="success",
                                team=agent.team,
                                agent=agent.id,
                            ).inc()

                            self._metrics.task_duration_seconds.labels(
                                team=agent.team,
                                agent=agent.id,
                            ).observe(execution_time)

                            self.logger.info(
                                "Task executed successfully",
                                task_id=task.id,
                                agent_id=agent.id,
                                execution_time=execution_time,
                            )

                            return result

                        except asyncio.TimeoutError:
                            execution_time = (datetime.utcnow() - start_time).total_seconds()

                            # Update agent state
                            agent.complete_task(success=False)

                            # Update metrics
                            self._metrics.tasks_total.labels(
                                status="timeout",
                                team=agent.team,
                                agent=agent.id,
                            ).inc()

                            self.logger.error(
                                "Task execution timeout",
                                task_id=task.id,
                                agent_id=agent.id,
                                timeout=timeout,
                            )

                            return TaskResult(
                                task_id=task.id,
                                agent_id=agent.id,
                                team_id=agent.team,
                                success=False,
                                output="",
                                error=f"Task execution timeout after {timeout}s",
                                execution_time=execution_time,
                            )

                        except Exception as e:
                            execution_time = (datetime.utcnow() - start_time).total_seconds()

                            # Update agent state
                            agent.complete_task(success=False)

                            # Update metrics
                            self._metrics.tasks_total.labels(
                                status="error",
                                team=agent.team,
                                agent=agent.id,
                            ).inc()

                            self.logger.error(
                                "Task execution failed",
                                task_id=task.id,
                                agent_id=agent.id,
                                error=str(e),
                            )

                            return TaskResult(
                                task_id=task.id,
                                agent_id=agent.id,
                                team_id=agent.team,
                                success=False,
                                output="",
                                error=str(e),
                                execution_time=execution_time,
                            )

                        finally:
                            # Update metrics
                            self._metrics.tasks_in_progress.labels(
                                team=agent.team,
                                agent=agent.id,
                            ).dec()

    async def _worker(self) -> None:
        """
        Worker coroutine that processes tasks from the queue.
        """
        self.logger.info("Dispatcher worker started")

        while self._running:
            try:
                # Get next task from queue (with timeout to allow checking _running)
                try:
                    queued_task = await asyncio.wait_for(
                        self._queue.get(),
                        timeout=1.0,
                    )
                except asyncio.TimeoutError:
                    continue

                # Update metrics
                self._metrics.task_queue_size.labels(
                    priority=str(queued_task.priority),
                ).dec()

                # Mark as running
                queued_task.status = ExecutionStatus.RUNNING
                queued_task.started_at = datetime.utcnow()

                # Execute the task
                try:
                    result = await self.execute(
                        queued_task.task,
                        queued_task.agent,
                    )

                    queued_task.status = ExecutionStatus.COMPLETED
                    queued_task.completed_at = datetime.utcnow()

                except Exception as e:
                    self.logger.error(
                        "Worker task execution failed",
                        task_id=queued_task.task.id,
                        error=str(e),
                    )
                    queued_task.status = ExecutionStatus.FAILED
                    queued_task.completed_at = datetime.utcnow()

                finally:
                    self._queue.task_done()

            except Exception as e:
                self.logger.error("Worker error", error=str(e))

        self.logger.info("Dispatcher worker stopped")

    async def start(self, num_workers: int = 1) -> None:
        """
        Start the dispatcher worker.

        Args:
            num_workers: Number of worker coroutines to start
        """
        if self._running:
            self.logger.warning("Dispatcher already running")
            return

        self._running = True

        # Start worker tasks
        # For simplicity, we'll just start one worker
        # In production, you could start multiple workers
        self._worker_task = asyncio.create_task(self._worker())

        self.logger.info("Dispatcher started", num_workers=1)

    async def stop(self, timeout: float = 10.0) -> None:
        """
        Stop the dispatcher worker.

        Args:
            timeout: Time to wait for graceful shutdown
        """
        if not self._running:
            self.logger.warning("Dispatcher not running")
            return

        self._running = False

        # Wait for worker to finish
        if self._worker_task:
            try:
                await asyncio.wait_for(
                    self._worker_task,
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                self.logger.warning("Dispatcher worker did not stop gracefully")
                self._worker_task.cancel()

        # Cancel all active tasks
        for task in self._active_tasks.values():
            task.cancel()

        self.logger.info("Dispatcher stopped")

    async def wait_for_completion(self, timeout: float | None = None) -> None:
        """
        Wait for all queued tasks to complete.

        Args:
            timeout: Maximum time to wait (None = wait indefinitely)
        """
        if timeout:
            await asyncio.wait_for(
                self._queue.join(),
                timeout=timeout,
            )
        else:
            await self._queue.join()

    def get_queue_size(self) -> int:
        """Get the current queue size."""
        return self._queue.qsize()

    def get_active_count(self) -> int:
        """Get the number of actively executing tasks."""
        return len(self._active_tasks)

    def get_concurrency_status(self) -> dict[str, Any]:
        """
        Get current concurrency status.

        Returns:
            Dictionary with concurrency information
        """
        return {
            "global": {
                "max": self.max_global_concurrent,
                "available": self._global_semaphore._value,
                "in_use": self.max_global_concurrent - self._global_semaphore._value,
            },
            "teams": {
                team_id: {
                    "max": self.max_per_team,
                    "available": sem._value,
                    "in_use": self.max_per_team - sem._value,
                }
                for team_id, sem in self._team_semaphores.items()
            },
            "agents": {
                agent_id: {
                    "max": self.max_per_agent,
                    "available": sem._value,
                    "in_use": self.max_per_agent - sem._value,
                }
                for agent_id, sem in self._agent_semaphores.items()
            },
            "queue_size": self.get_queue_size(),
            "active_tasks": self.get_active_count(),
        }
