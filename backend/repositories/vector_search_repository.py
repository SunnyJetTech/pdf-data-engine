from __future__ import annotations
from uuid import UUID
from core.config import settings
from repositories.qdrant_embedding_repository import QdrantEmbeddingRepository

class VectorSearchRepository:
    def __init__(self, embedding_repository: QdrantEmbeddingRepository | None = None) -> None:
        self.repository = (embedding_repository or QdrantEmbeddingRepository())

    @property
    def collection(self) -> str:
        return settings.QDRANT_COLLECTION

    def retrieve(self, *, dataset_id: UUID, embedding: list[float], limit: int = 8) -> list[dict]:
        return self.repository.search(collection=self.collection, dataset_id=dataset_id, vector=embedding, limit=limit)

    def similar_chunks(self, *, dataset_id: UUID, embedding: list[float], limit: int = 5) -> list[dict]:
        return self.retrieve( dataset_id=dataset_id, embedding=embedding, limit=limit)

    def hybrid_search(self, *, dataset_id: UUID, embedding: list[float], keyword_results: list[dict] | None = None, limit: int = 8) -> list[dict]:
        """
        Perform vector retrieval.

        Keyword fusion is intentionally not implemented until a
        keyword-search repository is available.
        """
        return self.retrieve( dataset_id=dataset_id, embedding=embedding, limit=limit)

    def delete_document(self, *, document_id: UUID) -> None:
        self.repository.delete_document(collection=self.collection, document_id=document_id)

    def delete_dataset(self, *, dataset_id: UUID) -> None:
        self.repository.delete_dataset(collection=self.collection, dataset_id=dataset_id)

    def count(self, *, dataset_id: UUID) -> int:
        return self.repository.count(collection=self.collection, dataset_id=dataset_id)