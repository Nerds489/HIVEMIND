"""
Async repository layer for relational memory operations.

Provides CRUD operations and queries for all memory models using SQLAlchemy 2.0 async patterns.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from hivemind.config import get_settings
from hivemind.memory.relational.models import (
    AgentExecution,
    Base,
    Checkpoint,
    Conversation,
    Message,
    Session,
    Task,
)

T = TypeVar("T", bound=Base)


class Repository:
    """
    Async repository for all relational memory operations.

    Provides type-safe CRUD operations and specialized queries.
    """

    def __init__(self, session_maker: async_sessionmaker[AsyncSession] | None = None):
        """
        Initialize repository.

        Args:
            session_maker: Optional session maker. If None, creates from config.
        """
        if session_maker is None:
            settings = get_settings()
            engine = create_async_engine(
                settings.postgres.async_url,
                pool_size=settings.postgres.pool_size,
                max_overflow=settings.postgres.max_overflow,
                pool_timeout=settings.postgres.pool_timeout,
                pool_recycle=settings.postgres.pool_recycle,
                echo=settings.debug,
            )
            session_maker = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        self._session_maker = session_maker

    async def _get_session(self) -> AsyncSession:
        """Get async session."""
        return self._session_maker()

    # =========================================================================
    # Generic CRUD Operations
    # =========================================================================

    async def create(self, instance: T) -> T:
        """
        Create a new instance.

        Args:
            instance: Model instance to create

        Returns:
            Created instance with ID populated
        """
        async with self._session_maker() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def get(self, model: type[T], id: UUID) -> T | None:
        """
        Get instance by ID.

        Args:
            model: Model class
            id: Instance ID

        Returns:
            Instance or None if not found
        """
        async with self._session_maker() as session:
            return await session.get(model, id)

    async def update(self, instance: T) -> T:
        """
        Update an instance.

        Args:
            instance: Model instance to update

        Returns:
            Updated instance
        """
        async with self._session_maker() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def delete(self, instance: T) -> None:
        """
        Delete an instance.

        Args:
            instance: Model instance to delete
        """
        async with self._session_maker() as session:
            await session.delete(instance)
            await session.commit()

    async def list_all(self, model: type[T], limit: int = 100, offset: int = 0) -> Sequence[T]:
        """
        List all instances of a model.

        Args:
            model: Model class
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of instances
        """
        async with self._session_maker() as session:
            stmt = select(model).limit(limit).offset(offset)
            result = await session.execute(stmt)
            return result.scalars().all()

    # =========================================================================
    # Session Operations
    # =========================================================================

    async def create_session(self, metadata: dict | None = None) -> Session:
        """
        Create a new session.

        Args:
            metadata: Optional session metadata

        Returns:
            Created session
        """
        session = Session(metadata=metadata or {})
        return await self.create(session)

    async def get_session(self, session_id: UUID) -> Session | None:
        """
        Get session by ID with relationships loaded.

        Args:
            session_id: Session ID

        Returns:
            Session or None if not found
        """
        async with self._session_maker() as session:
            stmt = (
                select(Session)
                .where(Session.id == session_id)
                .options(
                    selectinload(Session.tasks),
                    selectinload(Session.conversations).selectinload(Conversation.messages),
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def end_session(self, session_id: UUID) -> Session | None:
        """
        End a session by setting ended_at.

        Args:
            session_id: Session ID

        Returns:
            Updated session or None if not found
        """
        session_obj = await self.get(Session, session_id)
        if session_obj:
            session_obj.ended_at = datetime.utcnow()
            return await self.update(session_obj)
        return None

    async def list_active_sessions(self, limit: int = 100) -> Sequence[Session]:
        """
        List active sessions (ended_at is NULL).

        Args:
            limit: Maximum number of results

        Returns:
            List of active sessions
        """
        async with self._session_maker() as session:
            stmt = select(Session).where(Session.ended_at.is_(None)).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    # =========================================================================
    # Task Operations
    # =========================================================================

    async def create_task(
        self,
        session_id: UUID,
        prompt: str,
        agent_id: str | None = None,
        status: str = "pending",
    ) -> Task:
        """
        Create a new task.

        Args:
            session_id: Parent session ID
            prompt: Task prompt
            agent_id: Optional agent ID
            status: Task status

        Returns:
            Created task
        """
        task = Task(
            session_id=session_id,
            prompt=prompt,
            agent_id=agent_id,
            status=status,
        )
        return await self.create(task)

    async def get_task(self, task_id: UUID) -> Task | None:
        """
        Get task by ID with relationships.

        Args:
            task_id: Task ID

        Returns:
            Task or None if not found
        """
        async with self._session_maker() as session:
            stmt = (
                select(Task)
                .where(Task.id == task_id)
                .options(
                    selectinload(Task.checkpoints),
                    selectinload(Task.executions),
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def update_task_status(
        self,
        task_id: UUID,
        status: str,
        result: str | None = None,
    ) -> Task | None:
        """
        Update task status and optionally result.

        Args:
            task_id: Task ID
            status: New status
            result: Optional result

        Returns:
            Updated task or None if not found
        """
        task = await self.get(Task, task_id)
        if task:
            task.status = status
            if result is not None:
                task.result = result
            if status in ("completed", "failed", "cancelled"):
                task.completed_at = datetime.utcnow()
            return await self.update(task)
        return None

    async def list_tasks_by_session(
        self,
        session_id: UUID,
        status: str | None = None,
        limit: int = 100,
    ) -> Sequence[Task]:
        """
        List tasks for a session, optionally filtered by status.

        Args:
            session_id: Session ID
            status: Optional status filter
            limit: Maximum number of results

        Returns:
            List of tasks
        """
        async with self._session_maker() as session:
            stmt = select(Task).where(Task.session_id == session_id)
            if status:
                stmt = stmt.where(Task.status == status)
            stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def list_tasks_by_agent(
        self,
        agent_id: str,
        limit: int = 100,
    ) -> Sequence[Task]:
        """
        List tasks assigned to an agent.

        Args:
            agent_id: Agent ID
            limit: Maximum number of results

        Returns:
            List of tasks
        """
        async with self._session_maker() as session:
            stmt = select(Task).where(Task.agent_id == agent_id).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    # =========================================================================
    # Conversation Operations
    # =========================================================================

    async def create_conversation(self, session_id: UUID) -> Conversation:
        """
        Create a new conversation.

        Args:
            session_id: Parent session ID

        Returns:
            Created conversation
        """
        conversation = Conversation(session_id=session_id)
        return await self.create(conversation)

    async def get_conversation(self, conversation_id: UUID) -> Conversation | None:
        """
        Get conversation by ID with messages.

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation or None if not found
        """
        async with self._session_maker() as session:
            stmt = (
                select(Conversation)
                .where(Conversation.id == conversation_id)
                .options(selectinload(Conversation.messages))
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def add_message(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            conversation_id: Conversation ID
            role: Message role (user/assistant/system)
            content: Message content

        Returns:
            Created message
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        return await self.create(message)

    async def list_messages(
        self,
        conversation_id: UUID,
        limit: int = 100,
    ) -> Sequence[Message]:
        """
        List messages in a conversation.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of results

        Returns:
            List of messages ordered by timestamp
        """
        async with self._session_maker() as session:
            stmt = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.timestamp)
                .limit(limit)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    # =========================================================================
    # Checkpoint Operations
    # =========================================================================

    async def create_checkpoint(
        self,
        task_id: UUID,
        state_data: dict,
    ) -> Checkpoint:
        """
        Create a task checkpoint.

        Args:
            task_id: Task ID
            state_data: State data to save

        Returns:
            Created checkpoint
        """
        checkpoint = Checkpoint(
            task_id=task_id,
            state_data=state_data,
        )
        return await self.create(checkpoint)

    async def get_latest_checkpoint(self, task_id: UUID) -> Checkpoint | None:
        """
        Get the latest checkpoint for a task.

        Args:
            task_id: Task ID

        Returns:
            Latest checkpoint or None if not found
        """
        async with self._session_maker() as session:
            stmt = (
                select(Checkpoint)
                .where(Checkpoint.task_id == task_id)
                .order_by(Checkpoint.created_at.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def list_checkpoints(
        self,
        task_id: UUID,
        limit: int = 10,
    ) -> Sequence[Checkpoint]:
        """
        List checkpoints for a task.

        Args:
            task_id: Task ID
            limit: Maximum number of results

        Returns:
            List of checkpoints ordered by creation time (newest first)
        """
        async with self._session_maker() as session:
            stmt = (
                select(Checkpoint)
                .where(Checkpoint.task_id == task_id)
                .order_by(Checkpoint.created_at.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    # =========================================================================
    # Agent Execution Operations
    # =========================================================================

    async def create_agent_execution(
        self,
        agent_id: str,
        task_id: UUID,
        status: str = "running",
    ) -> AgentExecution:
        """
        Create a new agent execution record.

        Args:
            agent_id: Agent ID
            task_id: Task ID
            status: Execution status

        Returns:
            Created agent execution
        """
        execution = AgentExecution(
            agent_id=agent_id,
            task_id=task_id,
            status=status,
        )
        return await self.create(execution)

    async def complete_agent_execution(
        self,
        execution_id: UUID,
        status: str,
        output: dict | None = None,
    ) -> AgentExecution | None:
        """
        Complete an agent execution.

        Args:
            execution_id: Execution ID
            status: Final status
            output: Optional output data

        Returns:
            Updated execution or None if not found
        """
        execution = await self.get(AgentExecution, execution_id)
        if execution:
            execution.status = status
            execution.ended_at = datetime.utcnow()
            if output is not None:
                execution.output = output
            return await self.update(execution)
        return None

    async def list_executions_by_task(
        self,
        task_id: UUID,
        limit: int = 100,
    ) -> Sequence[AgentExecution]:
        """
        List agent executions for a task.

        Args:
            task_id: Task ID
            limit: Maximum number of results

        Returns:
            List of executions ordered by start time
        """
        async with self._session_maker() as session:
            stmt = (
                select(AgentExecution)
                .where(AgentExecution.task_id == task_id)
                .order_by(AgentExecution.started_at)
                .limit(limit)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def list_executions_by_agent(
        self,
        agent_id: str,
        limit: int = 100,
    ) -> Sequence[AgentExecution]:
        """
        List executions for an agent.

        Args:
            agent_id: Agent ID
            limit: Maximum number of results

        Returns:
            List of executions ordered by start time (newest first)
        """
        async with self._session_maker() as session:
            stmt = (
                select(AgentExecution)
                .where(AgentExecution.agent_id == agent_id)
                .order_by(AgentExecution.started_at.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
