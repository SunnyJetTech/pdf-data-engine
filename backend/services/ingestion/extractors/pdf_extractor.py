from __future__ import annotations
from pathlib import Path
from typing import Any
import fitz
from services.ingestion.extractors.base_extractor import BaseExtractor

class PDFExtractor(BaseExtractor):
    def extract(self, file_path: str | Path) -> dict[str, Any]:
        document = fitz.open(file_path)

        try:
            pages = [page.get_text() for page in document]

            metadata = document.metadata or {}

            return {
                "text": "\n\n".join(pages),
                "pages": len(pages),
                "metadata": metadata,
            }

        finally:
            document.close()