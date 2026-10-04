from __future__ import annotations
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.gemini_provider import GeminiProvider

class ProviderFactory:

    _providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
    }

    @classmethod
    def get(cls, provider: str):
        provider = provider.lower()

        if provider not in cls._providers:
            raise ValueError(f"Unknown provider '{provider}'.")

        return cls._providers[provider]()

    @classmethod
    def fallbacks(cls, provider: str):
        provider = provider.lower()

        order = [
            "openai",
            "anthropic",
            "gemini",
        ]

        return [
            cls.get(name)
            for name in order
            if name != provider
        ]