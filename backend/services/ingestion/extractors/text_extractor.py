from __future__ import annotations
from pathlib import Path
from typing import Any
from services.ingestion.extractors.base_extractor import BaseExtractor

class TextExtractor(BaseExtractor):
    def extract(self, file_path: str | Path) -> dict[str, Any]:
        path = Path(file_path)

        text = path.read_text(encoding="utf-8", errors="ignore")

        return {
            "text": text,
            "pages": 1,
            "metadata": {
                "characters": len(text),
            },
        }