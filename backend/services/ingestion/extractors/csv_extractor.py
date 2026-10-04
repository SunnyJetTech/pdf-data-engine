from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd
from services.ingestion.extractors.base_extractor import BaseExtractor

class CSVExtractor(BaseExtractor):
    def extract(self, file_path: str | Path) -> dict[str, Any]:
        dataframe = pd.read_csv(file_path)
        text = dataframe.to_csv(index=False)

        return {
            "text": text,
            "pages": 1,
            "metadata": {
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "column_names": list(dataframe.columns),
            },
        }