from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from .role import Role
    from .tenant import Tenant
    from .user import User

class Invitation(BaseModel):
    __tablename__ = "invitations"

    tenant_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("roles.id",ondelete="RESTRICT"), nullable=False, index=True)
    invited_by_id: Mapped[uuid.UUID | None] = mapped_column( ForeignKey("users.id",ondelete="SET NULL"), nullable=True, index=True)
    email: Mapped[str] = mapped_column( String(255), nullable=False, index=True)
    token: Mapped[str] = mapped_column( String(255), unique=True, nullable=False, index=True)
    accepted_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    
    tenant: Mapped["Tenant"] = relationship( back_populates="invitations")
    role: Mapped["Role"] = relationship( back_populates="invitations")
    invited_by: Mapped["User | None"] = relationship( foreign_keys=[invited_by_id])
    
    __table_args__ = (
        Index("ix_invitation_email","email"),
        Index("ix_invitation_expires","expires_at"),
    )