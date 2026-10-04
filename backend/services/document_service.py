from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.constants.document_status import DocumentStatus
from core.models.dataset import Dataset
from core.models.document import Document
from repositories.document_repository import DocumentRepository
from services.base_service import BaseService
from services.dataset_service import DatasetService
from services.usage_service import UsageService

class DocumentService(BaseService):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

        self.documents = DocumentRepository(db)
        self.datasets = DatasetService(db)
        self.usage = UsageService(db)

    def get(self, document_id: UUID) -> Document:
        document = self.documents.by_id(document_id)

        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

        return document

    def by_dataset(self, dataset_id: UUID) -> list[Document]:
        return self.documents.by_dataset(dataset_id=dataset_id)

    def by_creator(self, user_id: UUID) -> list[Document]:
        return self.documents.by_user(user_id=user_id)

    def create(self, *, dataset: Dataset, uploaded_by: UUID, **data) -> Document:
        if not self.usage.require_document(dataset.tenant_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Document quota exceeded.")

        document = Document(dataset_id=dataset.id, uploaded_by=uploaded_by, status=DocumentStatus.PENDING, **data)

        self.documents.add(document)
        self.usage.record_document( tenant_id=dataset.tenant_id)

        self.db.commit()
        self.db.refresh(document)

        self._refresh_dataset(dataset)
        self._log_created( actor_id=uploaded_by, document=document)

        return document

    def mark_processing(self, document: Document) -> Document:
        self.documents.update(document, status=DocumentStatus.PROCESSING)

        return self.commit_refresh(document)

    def mark_ready( self, *, document: Document, rows: int, columns: int) -> Document:
        self.documents.update(document, status=DocumentStatus.READY, rows_count=rows, columns_count=columns)

        self.db.commit()
        self.db.refresh(document)

        self._refresh_dataset(document.dataset)

        return document

    def mark_failed(self, *, document: Document, error: str) -> Document:
        self.documents.update(document, status=DocumentStatus.FAILED, error_message=error)

        self.db.commit()
        self.db.refresh(document)

        return document

    def delete(self, *, document: Document, actor_id: UUID) -> None:
        dataset = document.dataset


        self.db.commit()

        self._refresh_dataset(dataset)
        self._log_deleted(actor_id=actor_id, dataset_id=dataset.id, document_id=document.id)

    def _refresh_dataset(self, dataset: Dataset) -> None:
        documents = self.documents.by_dataset(dataset_id=dataset.id)

        rows = sum(document.rows_count or 0 for document in documents)
        columns = max((document.columns_count or 0 for document in documents), default=0)

        self.datasets.update_statistics(dataset=dataset, documents_count=len(documents), rows_count=rows, columns_count=columns)

    def _log_created(self, *, actor_id: UUID, document: Document) -> None:
        self.activity.log(
            actor_id=actor_id,
            tenant_id=document.dataset.tenant_id,
            action=ActivityAction.DOCUMENT_CREATED,
            target_type="document",
            target_id=document.id,
        )

    def _log_deleted(self, *, actor_id: UUID, dataset_id: UUID, document_id: UUID) -> None:
        dataset = self.datasets.get(dataset_id)

        self.activity.log(
            actor_id=actor_id,
            tenant_id=dataset.tenant_id,
            action=ActivityAction.DOCUMENT_DELETED,
            target_type="document",
            target_id=document_id,
        )
