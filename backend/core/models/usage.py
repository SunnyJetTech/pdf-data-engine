from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.tenant import Tenant

class Usage(BaseModel):
    __tablename__ = "usage"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(    "tenants.id",    ondelete="CASCADE",),unique=True,nullable=False,index=True)
    datasets_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    documents_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    searches_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    chat_messages_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    exports_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    storage_used_mb: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    prompt_tokens_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    completion_tokens_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    total_tokens_used: Mapped[int] = mapped_column(Integer,default=0,nullable=False)
    last_reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)
    uploads_used: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    api_calls_used: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    last_activity_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="usage")
    
    __table_args__ = (Index("ix_ai_usage_last_reset",    "last_reset_at"))