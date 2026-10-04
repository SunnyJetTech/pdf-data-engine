from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from .invitation import Invitation
    from .role_permission import RolePermission
    from .tenant import Tenant
    from .tenant_member import TenantMember


class Role(BaseModel):
    __tablename__ = "roles"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="roles")
    members: Mapped[list["TenantMember"]] = relationship(back_populates="role")
    invitations: Mapped[list["Invitation"]] = relationship(back_populates="role")
    role_permissions: Mapped[list["RolePermission"]] = relationship(back_populates="role", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_role_name_per_tenant"),
        Index("ix_role_tenant_system", "tenant_id", "is_system"),
    )