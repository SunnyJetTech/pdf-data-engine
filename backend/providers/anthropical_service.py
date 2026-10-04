from __future__ import annotations
from providers.base_provider import BaseProvider
from providers.response import AIResponse

class AnthropicProvider(BaseProvider):

    @property
    def provider_name(self) -> str:
        return "anthropic"

    async def chat(self, *, messages: list, tools: list | None = None) -> AIResponse:

        raise NotImplementedError("Anthropic provider not implemented.")

    async def chat_stream(self, *, messages: list, tools: list | None = None):

        raise NotImplementedError("Anthropic provider not implemented.")

    async def embed(self, text: str) -> list[float]:

        raise NotImplementedError("Anthropic embeddings not implemented.")