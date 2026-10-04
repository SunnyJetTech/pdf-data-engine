from __future__ import annotations
from context.tool_context import ToolContext
from services.search.duplicate_service import DuplicateService
from tools.base_tool import BaseTool

class DuplicateTool(BaseTool):

    name = "find_duplicates"
    description = "Find duplicate values in a dataset column."
    parameters = {
        "type": "object",
        "properties": {
            "column": {
                "type": "string",
            }
        },
        "required": ["column"],
    }

    async def execute( self, context: ToolContext, **kwargs):
        service = DuplicateService(context)

        return service.find(**kwargs)