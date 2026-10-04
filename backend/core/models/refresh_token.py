from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean,DateTime,ForeignKey,Index,String,
from sqlalchemy.orm import Mapped, mapped_column, relationship,
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.user import User

class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    family_id: Mapped[str] = mapped_column(String(64), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    replaced_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("refresh_tokens.id", ondelete="SET NULL"), nullable=True)
    created_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reuse_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
    replacement: Mapped["RefreshToken | None"] = relationship(remote_side="RefreshToken.id", uselist=False)

    __table_args__ = (Index("ix_refresh_family", "family_id", ))