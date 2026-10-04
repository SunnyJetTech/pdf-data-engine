from __future__ import annotations
from uuid import UUID
from sqlalchemy import desc, select, func
from sqlalchemy.orm import Session
from core.constants.conversation import ToolExecutionStatus
from core.models.tool_execution import ToolExecution
from repositories.base_repository import BaseRepository

class ToolExecutionRepository(BaseRepository[ToolExecution]):

    def __init__(self, db: Session):
        super().__init__(db, ToolExecution)

    def by_message(self, chat_message_id: UUID) -> list[ToolExecution]:
        stmt = select(ToolExecution).where(ToolExecution.chat_message_id == chat_message_id).order_by(desc(ToolExecution.created_at))

        return list(self.db.scalars(stmt).all())

    def successful(self, chat_message_id: UUID) -> list[ToolExecution]:
        stmt = select(ToolExecution).where(ToolExecution.chat_message_id == chat_message_id, ToolExecution.status == ToolExecutionStatus.SUCCESS)

        return list(self.db.scalars(stmt).all())

    def failed(self, chat_message_id: UUID) -> list[ToolExecution]:
        stmt = select(ToolExecution).where(ToolExecution.chat_message_id == chat_message_id, ToolExecution.status == ToolExecutionStatus.FAILED)

        return list(self.db.scalars(stmt).all())

    def by_tool(self, tool: str) -> list[ToolExecution]:
        stmt = select(ToolExecution).where(ToolExecution.tool == tool).order_by(desc(ToolExecution.created_at))

        return list(self.db.scalars(stmt).all())

    def mark_running(self, execution: ToolExecution) -> ToolExecution:

        return self.update(execution, status=ToolExecutionStatus.RUNNING)

    def mark_success(self, execution: ToolExecution, *, result: dict, execution_time: float) -> ToolExecution:

        return self.update(
            execution,
            status=ToolExecutionStatus.SUCCESS,
            result=result,
            execution_time=execution_time,
            error=None,
        )

    def mark_failed(self, execution: ToolExecution, *, error: str, execution_time: float | None = None) -> ToolExecution:

        return self.update(
            execution,
            status=ToolExecutionStatus.FAILED,
            error=error,
            execution_time=execution_time,
        )
        
    def by_id(self, execution_id: UUID) -> ToolExecution | None:
        stmt = select(ToolExecution).where(ToolExecution.id == execution_id)

        return self.db.scalar(stmt)
    
    def pending(self) -> list[ToolExecution]:
        stmt = (
            select(ToolExecution)
            .where(ToolExecution.status == ToolExecutionStatus.PENDING)
            .order_by(ToolExecution.created_at)
        )

        return list(self.db.scalars(stmt).all())
    
    def running(self) -> list[ToolExecution]:
        stmt = (
            select(ToolExecution)
            .where(ToolExecution.status == ToolExecutionStatus.RUNNING)
            .order_by(ToolExecution.created_at)
        )

        return list(self.db.scalars(stmt).all())
    
    def latest(self, chat_message_id: UUID) -> ToolExecution | None:
        stmt = (
            select(ToolExecution)
            .where(ToolExecution.chat_message_id == chat_message_id)
            .order_by(desc(ToolExecution.created_at))
            .limit(1)
        )

        return self.db.scalar(stmt)
    
    def clear_result(self, execution: ToolExecution) -> ToolExecution:

        return self.update(
            execution,
            result=None,
            error=None,
            execution_time=None,
            status=ToolExecutionStatus.PENDING,
        )
        
    def retry(self, execution: ToolExecution) -> ToolExecution:

        return self.update(
            execution,
            status=ToolExecutionStatus.PENDING,
            error=None,
        )
        
    def average_execution_time(self, tool: str) -> float:
        stmt = (
            select(func.avg(ToolExecution.execution_time))
            .where(ToolExecution.tool == tool, ToolExecution.status == ToolExecutionStatus.SUCCESS)
        )

        return float(self.db.scalar(stmt) or 0)
    
    def count_by_tool(self, tool: str) -> int:
        stmt = select(func.count()).select_from(ToolExecution).where(ToolExecution.tool == tool)

        return self.db.scalar(stmt) or 0