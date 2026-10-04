from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from core.constants.document_status import DocumentStatus
from core.models.document import Document
from core.pagination import Page, Pagination
from repositories.base_repository import BaseRepository

class DocumentRepository(BaseRepository[Document]):

    def __init__(self, db: Session) -> None:
        super().__init__(db=db, model=Document)

    def by_id(self, document_id: UUID) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)

        return self.db.scalar(stmt)

    def by_dataset(self, *, dataset_id: UUID) -> list[Document]:
        stmt = select(Document).where(Document.dataset_id == dataset_id).order_by(Document.created_at.desc(), Document.id.desc())

        return list(self.db.scalars(stmt).all())

    def by_creator(self, *, user_id: UUID) -> list[Document]:
        stmt = select(Document).where(Document.created_by == user_id).order_by( Document.created_at.desc(), Document.id.desc())

        return list(self.db.scalars(stmt).all())

    def ready(self, *, dataset_id: UUID) -> list[Document]:
        return self.by_status(dataset_id=dataset_id, status=DocumentStatus.READY)

    def processing(self, *, dataset_id: UUID) -> list[Document]:
        return self.by_status(dataset_id=dataset_id, status=DocumentStatus.PROCESSING)

    def failed(self, *, dataset_id: UUID) -> list[Document]:
        return self.by_status(dataset_id=dataset_id, status=DocumentStatus.FAILED)

    def by_status(self, *, dataset_id: UUID, status: DocumentStatus) -> list[Document]:
        stmt = (
            select(Document)
            .where( Document.dataset_id == dataset_id, Document.status == status)
            .order_by( Document.created_at.desc(), Document.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def with_dataset(self, document_id: UUID) -> Document | None:
        stmt = select(Document).options(joinedload(Document.dataset)).where(Document.id == document_id)

        return self.db.scalar(stmt)

    def change_status(self, *, document: Document, status: DocumentStatus) -> Document:
        document.status = status
        
        return document

    def paginate_by_dataset(self, *, dataset_id: UUID, pagination: Pagination) -> Page[Document]:
        base_filter = Document.dataset_id == dataset_id

        stmt = (
            select(Document)
            .where(base_filter)
            .order_by(Document.created_at.desc(), Document.id.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        )

        count_stmt = select(func.count()).select_from(Document).where(base_filter)

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt).all())

        return Page.create(items=items, total=total, pagination=pagination)

    def delete(self, document: Document) -> None:
        self.db.delete(document)