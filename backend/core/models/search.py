from __future__ import annotations
import uuid
from sqlalchemy import ForeignKey, JSON, Index, JSON, String, Boolean, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from core.models.dataset import Dataset
    from core.models.user import User

class SearchHistory(BaseModel):

    __tablename__ = "search_history"

    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    request: Mapped[dict] = mapped_column(JSON, nullable=False)
    dataset: Mapped["Dataset"] = relationship(back_populates="search_history")
    user: Mapped["User"] = relationship(back_populates="search_history")
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    __table_args__ = (
        Index("ix_search_history_dataset_created", "dataset_id", "created_at"))
    
class SavedSearch(BaseModel):

    __tablename__ = "saved_searches"

    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE") ,nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", ), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    filters: Mapped[list] = mapped_column(JSON, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    dataset: Mapped["Dataset"] = relationship(back_populates="saved_searches")
    user: Mapped["User"] = relationship(back_populates="saved_searches")
    
    __table_args__ = (UniqueConstraint("dataset_id", "user_id", "name", name="uq_saved_search_name"))