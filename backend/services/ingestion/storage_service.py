from __future__ import annotations
from pathlib import Path
import pandas as pd
from providers.storage.local_storage_provider import LocalStorageProvider

class StorageService:
    def __init__(self):
        self.provider = LocalStorageProvider()

    def save(self, *, file, folder: str = "documents") -> str:
        return self.provider.save(file=file, folder=folder)

    def delete(self, storage_path: str) -> None:
        self.provider.delete(storage_path)

    def exists(self, storage_path: str) -> bool:
        return self.provider.exists(storage_path)

    def resolve(self, storage_path: str) -> Path:
        return self.provider.resolve(storage_path)

    def url(self, storage_path: str) -> str:
        return self.provider.url(storage_path)
    
    def load_dataframe(self, path: str):
        if path.endswith(".csv"):
            return pd.read_csv(path)

        if path.endswith(".xlsx"):
            return pd.read_excel(path)

        if path.endswith(".xls"):
            return pd.read_excel(path)

        raise ValueError("Unsupported dataset format.")