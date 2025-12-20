"""
HIVEMIND Coordinator

Central orchestration component that manages task analysis, decomposition, routing,
and response synthesis from multiple agents.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from hivemind.agents.base import Agent
from hivemind.agents.teams import Team, TeamID
from hivemind.config import get_settings
from hivemind.observability.logging import LoggerMixin
from hivemind.observability.metrics import get_metrics
from hivemind.observability.tracing import get_tracer


class TaskState(str, Enum):
    """Task execution states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(int, Enum):
    """Task priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    agent_id: str
    team_id: str
    success: bool
    output: str
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0


@dataclass
class Task:
    """Represents a task to be executed by the HIVEMIND system."""

    id: str
    prompt: str
    state: TaskState = TaskState.PENDING
    priority: TaskPriority = TaskPriority.NORMAL

    # Routing information
    target_teams: list[TeamID] = field(default_factory=list)
    target_agents: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

    # Execution metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Results
    results: list[TaskResult] = field(default_factory=list)
    synthesized_response: str | None = None
    error: str | None = None

    # Sub-tasks for decomposition
    subtasks: list[Task] = field(default_factory=list)
    parent_task_id: str | None = None

    # Session context
    session_id: str | None = None
    user_id: str | None = None

    @property
    def is_complete(self) -> bool:
        """Check if task is in a terminal state."""
        return self.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED)

    @property
    def is_running(self) -> bool:
        """Check if task is currently running."""
        return self.state == TaskState.RUNNING

    @property
    def duration(self) -> float | None:
        """Get task duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def transition_to(self, new_state: TaskState) -> None:
        """Transition task to a new state."""
        self.state = new_state

        if new_state == TaskState.RUNNING:
            self.started_at = datetime.utcnow()
        elif new_state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED):
            self.completed_at = datetime.utcnow()

    def add_result(self, result: TaskResult) -> None:
        """Add an agent result to this task."""
        self.results.append(result)

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "prompt": self.prompt,
            "state": self.state.value,
            "priority": self.priority.value,
            "target_teams": [t.value for t in self.target_teams],
            "target_agents": self.target_agents,
            "keywords": self.keywords,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": self.duration,
            "results": [
                {
                    "agent_id": r.agent_id,
                    "team_id": r.team_id,
                    "success": r.success,
                    "execution_time": r.execution_time,
                }
                for r in self.results
            ],
            "error": self.error,
            "parent_task_id": self.parent_task_id,
            "session_id": self.session_id,
        }


class Coordinator(LoggerMixin):
    """
    Central Coordinator for the HIVEMIND system.

    Responsibilities:
    - Task analysis and keyword extraction
    - Task decomposition into subtasks
    - Route tasks to appropriate teams/agents via Router
    - Manage task execution via Dispatcher
    - Synthesize responses from multiple agents
    - Track task state and lifecycle
    """

    def __init__(
        self,
        router: Any,  # Router instance
        dispatcher: Any,  # Dispatcher instance
        context_manager: Any | None = None,  # ContextManager instance
    ) -> None:
        """
        Initialize the Coordinator.

        Args:
            router: Router instance for task routing
            dispatcher: Dispatcher instance for execution
            context_manager: Optional context manager for session handling
        """
        self.router = router
        self.dispatcher = dispatcher
        self.context_manager = context_manager

        self._tasks: dict[str, Task] = {}
        self._metrics = get_metrics()
        self._tracer = get_tracer()

        self.logger.info("Coordinator initialized")

    def create_task(
        self,
        prompt: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        session_id: str | None = None,
        user_id: str | None = None,
        parent_task_id: str | None = None,
    ) -> Task:
        """
        Create a new task.

        Args:
            prompt: The task prompt/description
            priority: Task priority level
            session_id: Optional session ID for context
            user_id: Optional user ID
            parent_task_id: Optional parent task ID for subtasks

        Returns:
            Created Task instance
        """
        task_id = str(uuid.uuid4())

        task = Task(
            id=task_id,
            prompt=prompt,
            priority=priority,
            session_id=session_id,
            user_id=user_id,
            parent_task_id=parent_task_id,
        )

        self._tasks[task_id] = task

        self.logger.info(
            "Task created",
            task_id=task_id,
            priority=priority.value,
            session_id=session_id,
        )

        return task

    def analyze_task(self, task: Task) -> None:
        """
        Analyze task and extract keywords for routing.

        Args:
            task: Task to analyze
        """
        with self._tracer.span("task.analyze", {"task_id": task.id}):
            # Extract keywords from the prompt
            keywords = self._extract_keywords(task.prompt)
            task.keywords = keywords

            self.logger.debug(
                "Task analyzed",
                task_id=task.id,
                keywords=keywords,
            )

    def _extract_keywords(self, prompt: str) -> list[str]:
        """
        Extract keywords from a prompt for routing.

        This is a simple implementation that extracts significant words.
        In production, this could use NLP/embedding techniques.

        Args:
            prompt: The task prompt

        Returns:
            List of keywords
        """
        # Convert to lowercase and split
        words = prompt.lower().split()

        # Filter out common stop words
        stop_words = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "should",
            "could", "may", "might", "can", "must", "i", "you", "he", "she", "it",
            "we", "they", "what", "which", "who", "when", "where", "why", "how",
            "this", "that", "these", "those", "to", "from", "in", "on", "at", "by",
            "for", "with", "about", "as", "of", "and", "or", "but", "not",
        }

        # Extract significant words (length > 3, not stop words)
        keywords = [
            word.strip(".,;:!?()[]{}\"'")
            for word in words
            if len(word) > 3 and word not in stop_words
        ]

        return list(set(keywords))  # Remove duplicates

    def decompose_task(self, task: Task) -> list[Task]:
        """
        Decompose a complex task into subtasks.

        This is a placeholder for task decomposition logic.
        In production, this could use LLM-based planning.

        Args:
            task: Task to decompose

        Returns:
            List of subtasks
        """
        # For now, we don't decompose - just return the original task
        # This can be enhanced with intelligent decomposition logic
        return [task]

    async def route_task(self, task: Task) -> list[tuple[Team | None, Agent | None]]:
        """
        Route task to appropriate teams and agents.

        Args:
            task: Task to route

        Returns:
            List of (team, agent) tuples for execution
        """
        with self._tracer.span("task.route", {"task_id": task.id}):
            # Use router to find target teams/agents
            routes = self.router.route(task.keywords)

            # Update task with routing information
            task.target_teams = [r[0].id for r in routes if r[0]]
            task.target_agents = [r[1].id for r in routes if r[1]]

            self.logger.info(
                "Task routed",
                task_id=task.id,
                teams=[t.value for t in task.target_teams],
                agents=task.target_agents,
            )

            return routes

    async def execute_task(
        self,
        task: Task,
        routes: list[tuple[Team | None, Agent | None]],
    ) -> None:
        """
        Execute task through the dispatcher.

        Args:
            task: Task to execute
            routes: List of (team, agent) tuples
        """
        with self._tracer.span("task.execute", {"task_id": task.id}):
            task.transition_to(TaskState.RUNNING)

            self._metrics.tasks_in_progress.labels(
                team="all",
                agent="all",
            ).inc()

            try:
                # Execute all routes in parallel
                execution_tasks = []
                for team, agent in routes:
                    if agent:
                        execution_tasks.append(
                            self.dispatcher.execute(task, agent)
                        )

                # Wait for all executions to complete
                results = await asyncio.gather(*execution_tasks, return_exceptions=True)

                # Process results
                for result in results:
                    if isinstance(result, Exception):
                        self.logger.error(
                            "Task execution failed",
                            task_id=task.id,
                            error=str(result),
                        )
                        task.error = str(result)
                    elif isinstance(result, TaskResult):
                        task.add_result(result)

                # Update task state
                if task.error or any(not r.success for r in task.results if isinstance(r, TaskResult)):
                    task.transition_to(TaskState.FAILED)
                    self._metrics.tasks_total.labels(
                        status="failed",
                        team="all",
                        agent="all",
                    ).inc()
                else:
                    task.transition_to(TaskState.COMPLETED)
                    self._metrics.tasks_total.labels(
                        status="completed",
                        team="all",
                        agent="all",
                    ).inc()

            except Exception as e:
                self.logger.error(
                    "Task execution error",
                    task_id=task.id,
                    error=str(e),
                )
                task.error = str(e)
                task.transition_to(TaskState.FAILED)
                self._metrics.tasks_total.labels(
                    status="failed",
                    team="all",
                    agent="all",
                ).inc()
            finally:
                self._metrics.tasks_in_progress.labels(
                    team="all",
                    agent="all",
                ).dec()

                # Record duration
                if task.duration:
                    self._metrics.task_duration_seconds.labels(
                        team="all",
                        agent="all",
                    ).observe(task.duration)

    def synthesize_response(self, task: Task) -> str:
        """
        Synthesize a unified response from multiple agent results.

        Args:
            task: Task with results to synthesize

        Returns:
            Synthesized response string
        """
        with self._tracer.span("task.synthesize", {"task_id": task.id}):
            if not task.results:
                return "No results to synthesize."

            if len(task.results) == 1:
                # Single result, just return it
                result = task.results[0]
                return result.output

            # Multiple results - synthesize them
            synthesis_parts = []

            for result in task.results:
                if result.success:
                    synthesis_parts.append(
                        f"[{result.team_id}] {result.output}"
                    )

            if not synthesis_parts:
                return "All agent executions failed."

            # Simple concatenation for now
            # In production, this could use LLM-based synthesis
            synthesized = "\n\n".join(synthesis_parts)
            task.synthesized_response = synthesized

            self.logger.info(
                "Response synthesized",
                task_id=task.id,
                result_count=len(task.results),
            )

            return synthesized

    async def process_task(
        self,
        prompt: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        session_id: str | None = None,
        user_id: str | None = None,
    ) -> tuple[Task, str]:
        """
        Process a task from start to finish.

        This is the main entry point for task processing.

        Args:
            prompt: Task prompt/description
            priority: Task priority
            session_id: Optional session ID
            user_id: Optional user ID

        Returns:
            Tuple of (task, synthesized_response)
        """
        with self._tracer.span("coordinator.process_task"):
            # Create task
            task = self.create_task(
                prompt=prompt,
                priority=priority,
                session_id=session_id,
                user_id=user_id,
            )

            try:
                # Analyze and extract keywords
                self.analyze_task(task)

                # Route to teams/agents
                routes = await self.route_task(task)

                if not routes:
                    task.error = "No suitable agents found for task"
                    task.transition_to(TaskState.FAILED)
                    return task, task.error

                # Execute task
                await self.execute_task(task, routes)

                # Synthesize response
                response = self.synthesize_response(task)

                return task, response

            except Exception as e:
                self.logger.error(
                    "Task processing failed",
                    task_id=task.id,
                    error=str(e),
                )
                task.error = str(e)
                task.transition_to(TaskState.FAILED)
                return task, f"Task processing failed: {e}"

    def get_task(self, task_id: str) -> Task | None:
        """
        Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task instance or None
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks."""
        return list(self._tasks.values())

    def get_tasks_by_state(self, state: TaskState) -> list[Task]:
        """Get all tasks in a specific state."""
        return [t for t in self._tasks.values() if t.state == state]

    def get_tasks_by_session(self, session_id: str) -> list[Task]:
        """Get all tasks for a session."""
        return [t for t in self._tasks.values() if t.session_id == session_id]

    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a running task.

        Args:
            task_id: Task ID to cancel

        Returns:
            True if cancelled, False if not found or already complete
        """
        task = self.get_task(task_id)
        if not task or task.is_complete:
            return False

        task.transition_to(TaskState.CANCELLED)
        self.logger.info("Task cancelled", task_id=task_id)
        return True
