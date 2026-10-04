from __future__ import annotations
from pathlib import Path
from uuid import UUID
from sqlalchemy.orm import Session
from core.constants.document_status import DocumentStatus
from core.models.chunk import Chunk
from core.models.document import Document
from repositories.chunk_repository import ChunkRepository
from repositories.document_repository import DocumentRepository
from services.ingestion.chunk_service import ChunkService
from services.ingestion.embedding_service import EmbeddingService
from services.ingestion.extractor_factory import ExtractorFactory
from services.storage.storage_service import StorageService

class DocumentIngestionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.documents = DocumentRepository(db)
        self.chunks = ChunkRepository(db)
        self.storage = StorageService()
        self.extractors = ExtractorFactory()
        self.chunker = ChunkService()
        self.embeddings = EmbeddingService(db)

    async def ingest(self, document_id: UUID) -> Document:
        document = self._get_document(document_id)

        self._mark_processing(document)

        try:
            file_path = self._resolve_file(document)

            extractor = self.extractors.get(file_path)
            extracted = extractor.extract(file_path)

            text = self._normalize(extracted.get("text", ""))

            chunks = self.chunker.chunk(document_id=document.id, text=text)
            chunk_models = self._build_chunks(document=document, chunks=chunks)
            self.chunks.create_many(chunk_models)
            self.db.flush()

            await self.embeddings.index_document(document=document, chunks=chunks)

            self._mark_ready(document=document, extracted=extracted)

            return document

        except Exception as exc:
            self._mark_failed(document=document, error=str(exc))
            raise

    def _get_document(self, document_id: UUID) -> Document:
        document = self.documents.by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        return document

    def _resolve_file(self, document: Document) -> Path:
        if not document.storage_path:
            raise ValueError("Document has no storage path.")

        return self.storage.resolve(document.storage_path)

    @staticmethod
    def _normalize(text: str) -> str:
        return text.strip()

    @staticmethod
    def _build_chunks(*, document: Document, chunks: list[dict]) -> list[Chunk]:
        return [
            Chunk(
                dataset_id=document.dataset_id,
                document_id=document.id,
                chunk_index=chunk["chunk_index"],
                text=chunk["text"],
                token_count=chunk.get("token_count", 0),
                metadata=chunk.get("metadata") or {},
            )
            for chunk in chunks
        ]

    def _mark_processing(self, document: Document) -> None:
        self.documents.update(document, status=DocumentStatus.PROCESSING, error_message=None)

        self.db.commit()

    def _mark_ready( self, *, document: Document, extracted: dict) -> None:
        metadata = extracted.get("metadata") or {}

        self.documents.update(
            document,
            status=DocumentStatus.READY,
            rows_count=self._extract_int(metadata, "rows"),
            columns_count=self._extract_int(metadata, "columns"),
            error_message=None,
        )

        self.db.commit()
        self.db.refresh(document)

    def _mark_failed(self, *, document: Document, error: str) -> None:
        self.db.rollback()
        self.documents.update( document, status=DocumentStatus.FAILED, error_message=error[:500])

        self.db.commit()
        self.db.refresh(document)

    @staticmethod
    def _extract_int(metadata: dict, key: str, default: int = 0) -> int:
        value = metadata.get(key, default)

        try:
            return int(value)
        except (TypeError, ValueError):
            return default