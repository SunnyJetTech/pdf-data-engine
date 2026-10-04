from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.chunk import Chunk
from repositories.base_repository import BaseRepository

class ChunkRepository(BaseRepository[Chunk]):

    def __init__(self, db: Session) -> None:
        super().__init__(db=db, model=Chunk)

    def by_id(self, chunk_id: UUID) -> Chunk | None:
        stmt = select(Chunk).where(Chunk.id == chunk_id)

        return self.db.scalar(stmt)

    def by_document(self, document_id: UUID) -> list[Chunk]:
        stmt = select(Chunk).where(Chunk.document_id == document_id).order_by(Chunk.chunk_index.asc())

        return list(self.db.scalars(stmt).all())

    def by_dataset(self, dataset_id: UUID) -> list[Chunk]:
        stmt = select(Chunk).where(Chunk.dataset_id == dataset_id).order_by(Chunk.document_id.asc(), Chunk.chunk_index.asc())

        return list(self.db.scalars(stmt).all())

    def create(self, *, dataset_id: UUID, document_id: UUID, chunk_index: int, text: str, token_count: int = 0, metadata: dict | None = None) -> Chunk:
        chunk = Chunk(
            dataset_id=dataset_id,
            document_id=document_id,
            chunk_index=chunk_index,
            text=text,
            token_count=token_count,
            metadata=metadata or {},
        )

        self.add(chunk)

        return chunk

    def create_many(self, chunks: list[Chunk]) -> None:

        self.db.add_all(chunks)

    def delete_by_document(self, document_id: UUID) -> int:

        chunks = self.by_document(document_id)

        for chunk in chunks:
            self.delete(chunk)

        return len(chunks)

    def count_document(self, document_id: UUID) -> int:

        return len(self.by_document(document_id))

    def count_dataset(self, dataset_id: UUID) -> int:

        return len(self.by_dataset(dataset_id))