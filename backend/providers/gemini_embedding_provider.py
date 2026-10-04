from __future__ import annotations
from providers.embedding_provider import EmbeddingProvider

class GeminiEmbeddingProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Gemini embedding provider is not configured.")