from __future__ import annotations
from google import genai
from google.genai import types
from core.config import settings
from providers.embedding_provider import EmbeddingProvider

class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())
        self.model = settings.GEMINI_EMBEDDING_MODEL
        self.dimensions = settings.GEMINI_EMBEDDING_DIMENSIONS

    async def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Cannot generate an embedding for empty text.")

        response = await self.client.aio.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=self.dimensions),
        )

        if not response.embeddings:
            raise ValueError("Gemini returned no embedding.")

        embedding = response.embeddings[0]

        if embedding.values is None:
            raise ValueError("Gemini returned an embedding without values.")

        return list(embedding.values)

    async def embed_many(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("Embedding input cannot contain empty text.")

        embeddings: list[list[float]] = []

        for text in texts:
            embeddings.append(await self.embed(text))

        return embeddings