from __future__ import annotations
from pathlib import Path
from uuid import uuid4
from sqlalchemy.orm import Session
from core.models.document import Document
from services.base_service import BaseService
from services.subscription.quota_service import QuotaService
from services.usage_service import UsageService
from storage.local_storage_provider import LocalStorageProvider
from storage.storage_provider import StorageProvider

class StorageService(BaseService):
    def __init__(self, db: Session, provider: StorageProvider | None = None) -> None:
        super().__init__(db)

        self.provider = provider or LocalStorageProvider()
        self.quota = QuotaService(db)
        self.usage = UsageService(db)

    def store(self, *, tenant_id, dataset_id, source_path: str | Path, filename: str) -> tuple[str, int]:
        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(source)

        if not source.is_file():
            raise ValueError("Source path must be a file.")

        size_bytes = source.stat().st_size

        usage = self.usage.get(tenant_id)

        self.quota.require_storage(tenant_id=tenant_id, current_usage_mb=usage.storage_used_mb, additional_bytes=size_bytes)
        storage_path = self._build_storage_path( tenant_id=str(tenant_id), dataset_id=str(dataset_id), filename=filename)

        with source.open("rb") as file:
            self.provider.store(file=file, path=storage_path)

        self.usage.record_storage(tenant_id=tenant_id, bytes_added=size_bytes)

        return storage_path, size_bytes

    def delete(self, *, document: Document) -> None:
        if document.storage_path:
            self.provider.delete(path=document.storage_path)

        if document.file_size:
            self.usage.release_storage(tenant_id=document.dataset.tenant_id, bytes_removed=document.file_size)

    def open(self, storage_path: str):
        return self.provider.open(path=storage_path)
    
    def exists(self, storage_path: str) -> bool:
        return self.provider.exists(path=storage_path)

    def size(self, storage_path: str) -> int:
        return self.provider.size(path=storage_path)

    def url(self, storage_path: str) -> str:
        return self.provider.url(path=storage_path)

    @staticmethod
    def _build_storage_path(*, tenant_id: str, dataset_id: str, filename: str) -> str:
        safe_name = Path(filename).name.replace(" ",  "_")

        return (f"{tenant_id}/datasets/{dataset_id}/{uuid4().hex}_{safe_name}")