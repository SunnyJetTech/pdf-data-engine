from __future__ import annotations
from uuid import UUID
from repositories.vector_search_repository import VectorSearchRepository
from services.ingestion.embedding_service import EmbeddingService

class RetrievalService:
    def __init__(self, embedding_service: EmbeddingService | None = None, vector_repository: VectorSearchRepository | None = None) -> None:
        self.embedding_service = (embedding_service or EmbeddingService())
        self.vector_repository = (vector_repository or VectorSearchRepository())

    async def retrieve(self, *, dataset_id: UUID, question: str, limit: int = 8) -> list[dict]:
        if limit <= 0:
            return []

        embedding = await self.embedding_service.embed_query(question,)

        return self.vector_repository.retrieve(dataset_id=dataset_id, embedding=embedding, limit=limit)

    async def retrieve_context(self, *, dataset_id: UUID, question: str, limit: int = 8) -> list[str]:
        chunks = await self.retrieve(dataset_id=dataset_id, question=question, limit=limit)

        return [
            chunk["payload"]["text"]
            for chunk in chunks
            if chunk.get("payload", {}).get("text")
        ]

    async def retrieve_with_metadata(self, *, dataset_id: UUID, question: str, limit: int = 8) -> list[dict]:
        return await self.retrieve(dataset_id=dataset_id, question=question, limit=limit)

    async def retrieve_single(self, *, dataset_id: UUID, question: str) -> dict | None:
        results = await self.retrieve(dataset_id=dataset_id, question=question, limit=1)

        return results[0] if results else None