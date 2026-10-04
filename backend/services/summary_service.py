from __future__ import annotations
from context.tool_context import ToolContext
from services.storage.storage_service import StorageService

class SummaryService:

    def __init__(self, context: ToolContext):
        self.context = context
        self.storage = StorageService()

    def generate(self) -> dict:
        dataframe = self.storage.load_dataframe(self.context.dataset.storage_path)

        rows = len(dataframe)
        columns = len(dataframe.columns)
        missing = dataframe.isnull().sum().sum()

        dtypes = {column: str(dtype) for column, dtype in dataframe.dtypes.items()}

        return {
            "summary": (
                f"The dataset contains {rows:,} rows and "
                f"{columns} columns."
            ),
            "rows": rows,
            "columns": columns,
            "missing_values": int(missing),
            "column_types": dtypes,
        }