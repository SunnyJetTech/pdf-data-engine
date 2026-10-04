from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.tenant import Tenant
    from core.models.user import User


class APIKey(BaseModel):
    __tablename__ = "api_keys"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"),nullable=False,index=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"),nullable=True,index=True)
    name: Mapped[str] = mapped_column(String(150),nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(20),nullable=False)
    key_hash: Mapped[str] = mapped_column(String(255),nullable=False,unique=True,index=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="api_keys")
    creator: Mapped["User | None"] = relationship(foreign_keys=[created_by])
    
    __table_args__ = (
        Index("ix_api_key_tenant_active", "tenant_id", "is_active"),    
    )