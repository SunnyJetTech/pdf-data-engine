from __future__ import annotations
from context.tool_context import ToolContext
from services.search.statistics_service import StatisticsService
from tools.base_tool import BaseTool

class StatisticsTool(BaseTool):

    name = "dataset_statistics"
    description = "Generate descriptive statistics for the current dataset."
    parameters = {
        "type": "object",
        "properties": {},
    }

    async def execute(self, context: ToolContext, **kwargs):
        service = StatisticsService(context)

        return service.generate()