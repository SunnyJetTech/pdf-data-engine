from __future__ import annotations
from context.tool_context import ToolContext
from services.storage.storage_service import StorageService

class StatisticsService:

    def __init__(self, context: ToolContext):
        self.context = context
        self.storage = StorageService()

    def generate(self) -> dict:
        dataframe = self.storage.load_dataframe(self.context.dataset.storage_path)
        numeric = dataframe.select_dtypes(include="number")

        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": list(dataframe.columns),
            "numeric_columns": list(numeric.columns),
            "statistics": numeric.describe().to_dict(),
        }