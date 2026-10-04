from __future__ import annotations
from typing import Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Filter, PointStruct, VectorParams
from core.config import settings

class QdrantService:
    def __init__(self, client: QdrantClient | None = None) -> None:
        self.client = client or QdrantClient(url=settings.QDRANT_URL, api_key=getattr(settings, "QDRANT_API_KEY", None))

    def ensure_collection(self, *, collection_name: str, vector_size: int) -> None:
        collections = self.client.get_collections().collections
        existing = {collection.name for collection in collections}

        if collection_name in existing:
            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def delete_collection(self, *, collection_name: str) -> None:
        self.client.delete_collection(collection_name=collection_name)

    def upsert( self, *, collection_name: str, ids: list[str], vectors: list[list[float]], payloads: list[dict[str, Any]]) -> None:
        if not ids:
            return

        if not (len(ids) == len(vectors) == len(payloads)):
            raise ValueError("ids, vectors, and payloads must have the same length.")

        points = [
            PointStruct(id=point_id, vector=vector, payload=payload)
            for point_id, vector, payload in zip(ids, vectors, payloads)
        ]

        self.client.upsert(collection_name=collection_name, points=points, wait=True)

    def delete_points(self, *, collection_name: str, ids: list[str]) -> None:
        if not ids:
            return

        self.client.delete(collection_name=collection_name, points_selector=ids, wait=True)

    def delete_by_filter(self, *, collection_name: str, query_filter: Filter) -> None:
        self.client.delete(collection_name=collection_name, points_selector=query_filter, wait=True)

    def search(self, *, collection_name: str, vector: list[float], limit: int = 10, query_filter: Filter | None = None) -> list[Any]:
        if limit <= 0:
            return []

        result = self.client.query_points(
            collection_name=collection_name,
            query=vector,
            query_filter=query_filter,
            with_payload=True,
            limit=limit,
        )

        return result.points

    def count(self, *, collection_name: str, query_filter: Filter | None = None, exact: bool = True) -> int:
        result = self.client.count(collection_name=collection_name, count_filter=query_filter, exact=exact)

        return result.count

    def health(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False