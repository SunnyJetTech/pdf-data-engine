from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel
from core.constants.membership import MembershipStatus

if TYPE_CHECKING:
    from .role import Role
    from .tenant import Tenant
    from .user import User


class TenantMember(BaseModel):
    __tablename__ = "tenant_members"

    tenant_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[MembershipStatus] = mapped_column(SQLEnum(MembershipStatus), default=MembershipStatus.ACTIVE, nullable=False)
    invited_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    tenant: Mapped["Tenant"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="tenant_memberships")
    role: Mapped["Role"] = relationship(back_populates="members")

    __table_args__ = (
        UniqueConstraint( "tenant_id", "user_id", name="uq_tenant_member"),
        Index( "ix_tenant_member_role", "role_id"),
        Index( "ix_tenant_member_status", "status"),
    )