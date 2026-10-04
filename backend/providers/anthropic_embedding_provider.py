from __future__ import annotations
from providers.embedding_provider import EmbeddingProvider

class AnthropicEmbeddingProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Anthropic does not currently provide an embedding API.")