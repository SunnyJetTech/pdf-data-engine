from __future__ import annotations
from context.tool_context import ToolContext
from services.search_service import SearchService
from tools.base_tool import BaseTool

class SearchTool(BaseTool):

    name = "search_dataset"
    description = "Search rows inside the active dataset."
    parameters = {
        "type": "object",
        "properties": {
            "filters": {"type": "array"},
            "sort": {"type": "object"},
            "page": {"type": "integer"},
            "page_size": {"type": "integer"},
            "columns": {"type": "array"},
        },
    }

    async def execute( self, context: ToolContext, **kwargs):
        service = SearchService(context)

        return service.search(**kwargs)