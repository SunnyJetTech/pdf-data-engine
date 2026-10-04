from __future__ import annotations
from pathlib import Path
from services.ingestion.extractors.base_extractor import BaseExtractor
from services.ingestion.extractors.csv_extractor import CSVExtractor
from services.ingestion.extractors.excel_extractor import ExcelExtractor
from services.ingestion.extractors.pdf_extractor import PDFExtractor
from services.ingestion.extractors.text_extractor import TextExtractor

class ExtractorFactory:
    def __init__(self) -> None:
        self._extractors: dict[str, BaseExtractor] = {
            ".pdf": PDFExtractor(),
            ".csv": CSVExtractor(),
            ".xlsx": ExcelExtractor(),
            ".xls": ExcelExtractor(),
            ".txt": TextExtractor(),
            ".md": TextExtractor(),
        }

    def get(self, path: str | Path) -> BaseExtractor:
        extension = Path(path).suffix.lower()

        extractor = self._extractors.get(extension)

        if extractor is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return extractor