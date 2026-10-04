from __future__ import annotations

from sqlalchemy.orm import Session

from core.config import settings
from core.models.document import Document
from providers.embedding_provider_factory import EmbeddingProviderFactory
from repositories.qdrant_embedding_repository import QdrantEmbeddingRepository


class EmbeddingService:
    def __init__(
        self,
        db: Session | None = None,
        provider: str = "openai",
        vector_repository: QdrantEmbeddingRepository | None = None,
    ) -> None:
        self.db = db
        self.provider = EmbeddingProviderFactory.get(provider)
        self.vector_repository = (
            vector_repository or QdrantEmbeddingRepository()
        )

    async def index_document(
        self,
        *,
        document: Document,
        chunks: list[dict],
    ) -> None:
        if not chunks:
            return

        tenant_id = str(document.dataset.tenant_id)
        dataset_id = str(document.dataset_id)
        document_id = str(document.id)

        ids: list[str] = []
        vectors: list[list[float]] = []
        payloads: list[dict] = []

        for chunk in chunks:
            chunk_index = chunk["chunk_index"]
            text = chunk["text"]

            embedding = await self.provider.embed(text)

            chunk_id = f"{document_id}_{chunk_index}"

            ids.append(chunk_id)
            vectors.append(embedding)

            payloads.append(
                {
                    "tenant_id": tenant_id,
                    "dataset_id": dataset_id,
                    "document_id": document_id,
                    "chunk_id": chunk_id,
                    "chunk_index": chunk_index,
                    "text": text,
                    "metadata": chunk.get("metadata") or {},
                }
            )

        if not vectors:
            return

        self.vector_repository.ensure_collection(
            collection=settings.QDRANT_COLLECTION,
            vector_size=len(vectors[0]),
        )

        self.vector_repository.upsert(
            collection=settings.QDRANT_COLLECTION,
            ids=ids,
            vectors=vectors,
            payloads=payloads,
        )

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:
        return await self.provider.embed(query)