from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from .role_permission import RolePermission

class Permission(BaseModel):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role_permissions: Mapped[list["RolePermission"]] = relationship(back_populates="permission", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("resource", "action", name="uq_permission_resource_action"),
        Index("ix_permission_resource_action", "resource", "action"),
    )