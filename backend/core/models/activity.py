from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Index, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.document import Document
    from core.models.tenant import Tenant
    from core.models.user import User

class Activity(BaseModel):
    __tablename__ = "activities"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    document_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON,default=dict, nullable=False)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="activities")
    user: Mapped["User"] = relationship(back_populates="activities")
    document: Mapped["Document"] = relationship(back_populates="activities")

    __table_args__ = (
        Index("ix_activity_tenant_created", "tenant_id", "created_at"),
        Index("ix_activity_user_created", "user_id", "created_at"),
        Index("ix_activity_action", "action")
    )