from __future__ import annotations
from pathlib import Path
from context.tool_context import ToolContext
from services.storage.storage_service import StorageService

class ExportService:

    def __init__(self, context: ToolContext):
        self.context = context
        self.storage = StorageService()

    async def export(self, *, format: str = "csv", filename: str | None = None) -> dict:
        dataframe = self.storage.load_dataframe(self.context.dataset.storage_path)

        filename = filename or f"{self.context.dataset.slug}.{format}"

        export_dir = Path("exports")
        export_dir.mkdir( parents=True, exist_ok=True)

        destination = export_dir / filename

        if format == "csv":
            dataframe.to_csv(destination, index=False)

        elif format == "xlsx":
            dataframe.to_excel(destination, index=False)

        else:
            raise ValueError(f"Unsupported export format '{format}'.")

        return {
            "success": True,
            "filename": filename,
            "path": str(destination),
        }