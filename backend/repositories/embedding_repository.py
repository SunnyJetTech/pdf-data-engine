from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class EmbeddingRepository(ABC):
    @abstractmethod
    def ensure_collection( self, *, collection: str, vector_size: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def upsert(self, *, collection: str, ids: list[str], vectors: list[list[float]], payloads: list[dict]) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, *, collection: str, vector: list[float], dataset_id: UUID, limit: int = 10) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def delete_document(self, *, collection: str, document_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_dataset(self, *, collection: str, dataset_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def count(self, *, collection: str, dataset_id: UUID) -> int:
        raise NotImplementedError