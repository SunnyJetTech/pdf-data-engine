from __future__ import annotations
from providers.base_provider import BaseProvider
from providers.response import AIResponse

class GeminiProvider(BaseProvider):

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def chat(self, *, messages: list, tools: list | None = None) -> AIResponse:

        raise NotImplementedError("Gemini provider not implemented.")

    async def chat_stream(self, *, messages: list, tools: list | None = None):

        raise NotImplementedError("Gemini provider not implemented.")

    async def embed(self, text: str) -> list[float]:

        raise NotImplementedError("Gemini embeddings not implemented.")