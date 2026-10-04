from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from core.models.base import BaseModel
from core.models.chat_session import ChatSession
from core.enums.dataset import DatasetStatus
from datetime import datetime
from sqlalchemy import UniqueConstraint
from core.models.search import SearchHistory

if TYPE_CHECKING:
    from .document import Document
    from .tenant import Tenant
    from .user import User
    from .search import SavedSearch

class Dataset(BaseModel):

    __tablename__ = "datasets"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE",),nullable=False,index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL",),nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    mongo_collection: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[DatasetStatus] = mapped_column(String(30), default=DatasetStatus.PROCESSING)
    documents_count: Mapped[int] = mapped_column(Integer, default=0)
    rows_count: Mapped[int] = mapped_column(Integer, default=0)
    columns_count: Mapped[int] = mapped_column(Integer, default=0)
    last_used_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    last_chat_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="datasets")
    created_by_user: Mapped["User"] = relationship(back_populates="datasets")
    documents: Mapped[list["Document"]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    chat_sessions: Mapped[list["ChatSession"]] = relationship("ChatSession", back_populates="dataset", cascade="all, delete-orphan")
    saved_searches: Mapped[list["SavedSearch"]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    search_history: Mapped[list["SearchHistory"]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    
    __table_args__ = (UniqueConstraint("tenant_id", "slug", name="uq_dataset_tenant_slug"))
