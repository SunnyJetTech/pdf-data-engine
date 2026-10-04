from tools import tool_registry
from tools.search_tool import SearchTool
from tools.statistics_tool import StatisticsTool
from tools.duplicate_tool import DuplicateTool
from tools.export_tool import ExportTool
from tools.summary_tool import SummaryTool

TOOLS = (
    SearchTool,
    StatisticsTool,
    DuplicateTool,
    ExportTool,
    SummaryTool,
)

def register_tools():

    for tool in TOOLS:
        tool_registry.register(
            tool()
        )