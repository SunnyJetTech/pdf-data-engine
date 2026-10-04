from __future__ import annotations
from typing import Any
from context.tool_context import ToolContext
from tools import tool_registry

class ToolExecutor:
    @staticmethod
    async def execute(*, tool_name: str, context: ToolContext, arguments: dict[str, Any] | None = None) -> Any:
        tool = tool_registry.get(tool_name)

        if tool is None:
            raise ValueError(f"Unknown tool '{tool_name}'.")

        arguments = arguments or {}

        try:
            return await tool.execute(context, **arguments)

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "tool_name": tool_name,
            }

    @staticmethod
    async def execute_many(*, tool_calls: list[dict], context: ToolContext) -> list[dict]:
        results: list[dict] = []

        for call in tool_calls:
            result = await ToolExecutor.execute(tool_name=call["name"], context=context, arguments=call.get("arguments") or {})

            results.append(
                {
                    "call_id": call["id"],
                    "tool_name": call["name"],
                    "result": result,
                }
            )

        return results