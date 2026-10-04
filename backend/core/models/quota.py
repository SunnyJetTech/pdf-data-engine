from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.tenant import Tenant

class Quota(BaseModel):
    __tablename__ = "quotas"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    datasets_limit: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    documents_limit: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    searches_limit: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    chat_messages_limit: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    exports_limit: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    storage_limit_mb: Mapped[int] = mapped_column(Integer, default=1024, nullable=False)
    ai_tokens_limit: Mapped[int] = mapped_column(Integer, default=500000, nullable=False)
    reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    uploads_limit: Mapped[int] = mapped_column( Integer, default=100, nullable=False)
    api_keys_limit: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    team_members_limit: Mapped[int] = mapped_column( Integer, default=1, nullable=False)
    max_file_size_mb: Mapped[int] = mapped_column( Integer, default=50, nullable=False)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="quota")

    __table_args__ = (Index("ix_quota_reset_at", "reset_at"))