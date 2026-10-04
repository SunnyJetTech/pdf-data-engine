from __future__ import annotations
from collections.abc import Callable
from providers.embedding_provider import EmbeddingProvider
from providers.gemini_embedding_provider import GeminiEmbeddingProvider
from providers.openai_embedding_provider import OpenAIEmbeddingProvider
from providers.anthropic_embedding_provider import AnthropicEmbeddingProvider

class EmbeddingProviderFactory:
    _providers: dict[str, Callable[[], EmbeddingProvider]] = {
        "openai": OpenAIEmbeddingProvider,
        "gemini": GeminiEmbeddingProvider,
        "anthropic": AnthropicEmbeddingProvider,
        
    }

    @classmethod
    def get(cls, provider: str = "openai") -> EmbeddingProvider:
        if not isinstance(provider, str):
            raise ValueError("Embedding provider must be a string.")

        provider_name = provider.strip().lower()

        provider_class = cls._providers.get(provider_name)

        if provider_class is None:
            supported = ", ".join(sorted(cls._providers))
            raise ValueError(
                f"Unsupported embedding provider: {provider_name}. "
                f"Supported providers: {supported}"
            )

        return provider_class()