from __future__ import annotations
import uuid
from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

class Chunk(BaseModel):
    __tablename__ = "chunks"

    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column( Integer, nullable=False)
    text: Mapped[str] = mapped_column( Text, nullable=False)
    token_count: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    metadata: Mapped[dict] = mapped_column( JSONB, default=dict, nullable=False)
    
    dataset = relationship("Dataset", lazy="joined")
    document = relationship("Document", lazy="joined")

    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uq_chunk_document_index"),
    )