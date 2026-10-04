from __future__ import annotations
from openai import AsyncOpenAI
from core.config import settings
from providers.embedding_provider import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBEDDING_MODEL

    async def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Cannot generate an embedding for empty text.")

        response = await self.client.embeddings.create( model=self.model, input=text)

        return response.data[0].embedding

    async def embed_many(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("Embedding input cannot contain empty text.")

        response = await self.client.embeddings.create( model=self.model, input=texts)

        return [
            item.embedding
            for item in response.data
        ]