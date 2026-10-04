from __future__ import annotations
import json
from typing import Any
from openai import AsyncOpenAI
from core.config import settings
from providers.base_provider import BaseProvider
from providers.response import AIResponse

class OpenAIProvider(BaseProvider):
    DEFAULT_MODEL = "gpt-5.5"

    def __init__(self, *, model: str | None = None) -> None:

        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model or getattr(settings, "OPENAI_CHAT_MODEL", self.DEFAULT_MODEL)

    @property
    def provider_name(self) -> str:
        return "openai"

    async def chat( self, *, messages: list, tools: list | None = None) -> AIResponse:

        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

        response = await self.client.chat.completions.create(**request)

        choice = response.choices[0]

        tool_calls: list[dict[str, Any]] = []

        if choice.message.tool_calls:

            for tool in choice.message.tool_calls:

                arguments = tool.function.arguments

                try:
                    arguments = json.loads(arguments)

                except Exception:
                    pass

                tool_calls.append(
                    {
                        "id": tool.id,
                        "name": tool.function.name,
                        "arguments": arguments,
                    }
                )

        usage = response.usage

        return AIResponse(
            provider=self.provider_name,
            model=response.model,
            content=choice.message.content or "",
            tool_calls=tool_calls,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            finish_reason=choice.finish_reason,
            metadata={},
        )

    async def chat_stream(self, *, messages: list, tools: list | None = None):
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }

        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

        stream = await self.client.chat.completions.create(**request)

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                yield delta.content