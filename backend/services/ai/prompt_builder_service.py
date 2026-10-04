from __future__ import annotations
from typing import Any
from core.constants.conversation import MessageRole
from core.models.chat_message import ChatMessage

class PromptBuilderService:
    @staticmethod
    def build(
        *,
        system_prompt: str,
        history: list[ChatMessage],
        memory: dict[str, dict[str, Any]],
        retrieved_context: list[str],
        user_message: str,
    ) -> list[dict[str, str]]:

        messages: list[dict[str, str]] = []
        messages.append({"role": MessageRole.SYSTEM.value, "content": system_prompt})

        if memory:
            messages.append({"role": MessageRole.SYSTEM.value, "content": PromptBuilderService._memory_prompt(memory)})

        if retrieved_context:
            messages.append(
                {"role": MessageRole.SYSTEM.value, "content": PromptBuilderService._context_prompt(retrieved_context)}
            )
            
        messages.extend(PromptBuilderService._history(history))
        messages.append({"role": MessageRole.USER.value, "content": user_message})

        return messages

    @staticmethod
    def _history(history: list[ChatMessage]) -> list[dict[str, str]]:

        return [{"role": message.role.value, "content": message.content} for message in history]

    @staticmethod
    def _memory_prompt(memory: dict[str, dict[str, Any]]) -> str:
        lines: list[str] = ["Conversation Memory:"]

        for namespace, values in memory.items():
            lines.append(f"[{namespace}]")

            for key, value in values.items():
                lines.append(f"{key}: {value}")

            lines.append("")

        return "\n".join(lines).strip()

    @staticmethod
    def _context_prompt(context: list[str]) -> str:
        lines = ["Retrieved Context:", ""]

        for index, chunk in enumerate(context, start=1):
            lines.append(f"[{index}]")
            lines.append(chunk)
            lines.append("")

        return "\n".join(lines).strip()