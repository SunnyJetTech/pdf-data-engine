from __future__ import annotations
from abc import ABC, abstractmethod
from providers.response import AIResponse

class BaseProvider(ABC):

    @abstractmethod
    async def chat(self, *, messages: list, tools: list | None = None) -> AIResponse:
        ...

    @abstractmethod
    async def chat_stream(self, *, messages: list, tools: list | None = None):
        ...

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...