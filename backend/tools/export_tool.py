from __future__ import annotations
from context.tool_context import ToolContext
from services.search.export_service import ExportService
from tools.base_tool import BaseTool

class ExportTool(BaseTool):

    name = "export_dataset"
    description = "Export the active dataset."
    parameters = {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "enum": ["csv", "xlsx"],
            },
            "filename": {
                "type": "string",
            },
        },
    }

    async def execute(self, context: ToolContext, **kwargs):
        service = ExportService(context)

        return await service.export(**kwargs)