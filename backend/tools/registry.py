from __future__ import annotations
from typing import Dict
from tools.base_tool import BaseTool

class ToolRegistry:

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        self._tools.pop(name, None)

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def all(self) -> list[BaseTool]:
        return list(self._tools.values())

    def exists(self, name: str) -> bool:
        return name in self._tools

    def metadata(self) -> list[dict]:
        return [tool.metadata for tool in self._tools.values()]
    
    def names(self):
        return list(self._tools.keys())



