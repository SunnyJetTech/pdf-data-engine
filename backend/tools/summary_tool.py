from __future__ import annotations
from context.tool_context import ToolContext
from services.search.summary_service import SummaryService
from tools.base_tool import BaseTool

class SummaryTool(BaseTool):

    name = "summarize_dataset"
    description = "Generate a natural language summary of the dataset."
    parameters = {
        "type": "object",
        "properties": {},
    }

    async def execute(self, context: ToolContext, **kwargs):
        service = SummaryService(context)

        return service.generate()