from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, file_path: str | Path) -> dict:

        raise NotImplementedError