from __future__ import annotations
from abc import ABC, abstractmethod
from context.tool_context import ToolContext

class BaseTool(ABC):

    name: str = ""
    description: str = ""
    parameters: dict = {
        "type": "object",
        "properties": {},
    }

    @abstractmethod
    async def execute(self, context: ToolContext, **kwargs):
        raise NotImplementedError

    @property
    def metadata(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __repr__(self) -> str:
        return f"<Tool {self.name}>"