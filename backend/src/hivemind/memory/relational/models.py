"""
SQLAlchemy 2.0 async models for relational memory.

Defines the core data structures for session management, task tracking,
conversations, checkpoints, and agent execution history.
"""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base for all models."""

    type_annotation_map = {
        dict: JSONB,
    }


class Session(Base):
    """
    Session represents a user interaction session.

    Sessions group related tasks, conversations, and agent executions.
    """

    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    metadata: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )

    # Relationships
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    # Indexes
    __table_args__ = (
        Index("ix_sessions_created_at", "created_at"),
        Index("ix_sessions_ended_at", "ended_at"),
    )

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, created_at={self.created_at})>"


class Task(Base):
    """
    Task represents a unit of work assigned to one or more agents.

    Tasks track prompts, results, status, and execution timeline.
    """

    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )
    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    agent_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="tasks",
    )
    checkpoints: Mapped[List["Checkpoint"]] = relationship(
        "Checkpoint",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    executions: Mapped[List["AgentExecution"]] = relationship(
        "AgentExecution",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    # Indexes
    __table_args__ = (
        Index("ix_tasks_session_id", "session_id"),
        Index("ix_tasks_status", "status"),
        Index("ix_tasks_agent_id", "agent_id"),
        Index("ix_tasks_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, status={self.status}, agent_id={self.agent_id})>"


class Conversation(Base):
    """
    Conversation represents a dialogue context within a session.

    Conversations contain ordered messages and can span multiple tasks.
    """

    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="conversations",
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.timestamp",
    )

    # Indexes
    __table_args__ = (
        Index("ix_conversations_session_id", "session_id"),
        Index("ix_conversations_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, session_id={self.session_id})>"


class Message(Base):
    """
    Message represents a single message in a conversation.

    Messages have a role (user/assistant/system) and content.
    """

    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )

    # Indexes
    __table_args__ = (
        Index("ix_messages_conversation_id", "conversation_id"),
        Index("ix_messages_timestamp", "timestamp"),
        Index("ix_messages_role", "role"),
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"


class Checkpoint(Base):
    """
    Checkpoint represents a saved state snapshot during task execution.

    Enables task resumption and state recovery.
    """

    __tablename__ = "checkpoints"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    task_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    state_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="checkpoints",
    )

    # Indexes
    __table_args__ = (
        Index("ix_checkpoints_task_id", "task_id"),
        Index("ix_checkpoints_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Checkpoint(id={self.id}, task_id={self.task_id}, created_at={self.created_at})>"


class AgentExecution(Base):
    """
    AgentExecution tracks individual agent runs within a task.

    Records which agent ran, when, status, and output.
    """

    __tablename__ = "agent_executions"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    agent_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    task_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="running",
    )
    output: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="executions",
    )

    # Indexes
    __table_args__ = (
        Index("ix_agent_executions_agent_id", "agent_id"),
        Index("ix_agent_executions_task_id", "task_id"),
        Index("ix_agent_executions_status", "status"),
        Index("ix_agent_executions_started_at", "started_at"),
    )

    def __repr__(self) -> str:
        return f"<AgentExecution(id={self.id}, agent_id={self.agent_id}, status={self.status})>"
