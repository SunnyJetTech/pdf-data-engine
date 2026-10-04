from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd
from services.ingestion.extractors.base_extractor import BaseExtractor

class ExcelExtractor(BaseExtractor):
    def extract(self, file_path: str | Path) -> dict[str, Any]:
        workbook = pd.read_excel(file_path, sheet_name=None)

        sheets: list[str] = []
        rows = 0
        columns = 0

        for sheet_name, dataframe in workbook.items():
            rows += len(dataframe)
            columns = max(columns, len(dataframe.columns))

            sheets.append(f"# Sheet: {sheet_name}\n")
            sheets.append(dataframe.to_csv(index=False))

        return {
            "text": "\n\n".join(sheets),
            "pages": len(workbook),
            "metadata": {
                "rows": rows,
                "columns": columns,
                "sheet_count": len(workbook),
                "sheet_names": list(workbook.keys()),
            },
        }