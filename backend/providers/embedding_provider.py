from __future__ import annotations
from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError

    async def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [
            await self.embed(text)
            for text in texts
        ]