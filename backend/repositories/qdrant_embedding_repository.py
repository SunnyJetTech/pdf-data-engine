from __future__ import annotations
from uuid import UUID
from qdrant_client.models import FieldCondition, Filter, MatchValue
from repositories.embedding_repository import EmbeddingRepository
from services.qdrant_service import QdrantService

class QdrantEmbeddingRepository(EmbeddingRepository):
    def __init__(self, qdrant: QdrantService | None = None) -> None:
        self.qdrant = qdrant or QdrantService()

    def ensure_collection(self, *, collection: str, vector_size: int) -> None:
        self.qdrant.ensure_collection(collection_name=collection, vector_size=vector_size)

    def upsert( self, *, collection: str, ids: list[str], vectors: list[list[float]], payloads: list[dict]) -> None:
        self.qdrant.upsert(collection_name=collection, ids=ids, vectors=vectors, payloads=payloads)

    def search(self, *, collection: str, vector: list[float], dataset_id: UUID, limit: int = 10) -> list[dict]:
        if limit <= 0:
            return []

        query_filter = Filter(
            must=[
                FieldCondition(key="dataset_id", match=MatchValue(value=str(dataset_id))),
            ],
        )

        points = self.qdrant.search( collection_name=collection, vector=vector, limit=limit, query_filter=query_filter)

        return [
            {
                "id": point.id,
                "score": point.score,
                "payload": point.payload or {},
            }
            for point in points
        ]

    def delete_document(self, *, collection: str, document_id: UUID) -> None:
        query_filter = Filter(
            must=[
                FieldCondition(key="document_id", match=MatchValue(value=str(document_id))),
            ],
        )

        self.qdrant.delete_by_filter(collection_name=collection, query_filter=query_filter)

    def delete_dataset(self, *, collection: str, dataset_id: UUID) -> None:
        query_filter = Filter(
            must=[
                FieldCondition(key="dataset_id", match=MatchValue(value=str(dataset_id))),
            ],
        )

        self.qdrant.delete_by_filter(collection_name=collection, query_filter=query_filter)

    def count(self, *, collection: str, dataset_id: UUID) -> int:
        query_filter = Filter(
            must=[
                FieldCondition(key="dataset_id", match=MatchValue(value=str(dataset_id))),
            ],
        )

        return self.qdrant.count(collection_name=collection, query_filter=query_filter, exact=True)