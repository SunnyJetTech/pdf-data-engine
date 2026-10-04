from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.models.dataset import Dataset
from repositories.dataset_repository import DatasetRepository
from services.base_service import BaseService
from services.subscription.quota_service import QuotaService
from services.usage_service import UsageService

class DatasetService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

        self.datasets = DatasetRepository(db)
        self.quota = QuotaService(db)
        self.usage = UsageService(db)

    def get(self, dataset_id: UUID) -> Dataset:
        dataset = self.datasets.by_id(dataset_id)

        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

        return dataset

    def by_slug(self, *, tenant_id: UUID, slug: str) -> Dataset:
        dataset = self.datasets.by_slug(tenant_id=tenant_id, slug=slug)

        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

        return dataset

    def by_tenant(self, tenant_id: UUID) -> list[Dataset]:

        return self.datasets.by_tenant(tenant_id=tenant_id)

    def by_creator(self, user_id: UUID) -> list[Dataset]:

        return self.datasets.by_creator(user_id=user_id)

    def create(self, *, tenant_id: UUID, created_by: UUID, **data) -> Dataset:
        usage = self.usage.get(tenant_id)
        self.quota.require_dataset(tenant_id=tenant_id, current_usage=usage.datasets_used)
        slug = data["slug"]

        if self.datasets.exists_slug(tenant_id=tenant_id, slug=slug):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dataset slug already exists.")

        dataset = Dataset(tenant_id=tenant_id, created_by=created_by, **data)

        self.datasets.add(dataset)
        self.commit_refresh(dataset)
        self.usage.record_dataset(tenant_id)
        self._log_created(actor_id=created_by, dataset=dataset)

        return dataset

    def update(self, *, dataset: Dataset, **changes) -> Dataset:
        self.datasets.update(dataset, **changes)

        return self.commit_refresh(dataset)

    def archive(self, *, dataset: Dataset, actor_id: UUID) -> Dataset:
        self.datasets.archive(dataset)
        dataset = self.commit_refresh(dataset)
        self._log_archived( actor_id=actor_id, dataset=dataset)

        return dataset

    def restore(self, *, dataset: Dataset, actor_id: UUID) -> Dataset:
        self.datasets.restore(dataset)
        dataset = self.commit_refresh(dataset)

        self._log_restored( actor_id=actor_id, dataset=dataset)

        return dataset

    def delete(self, *, dataset: Dataset, actor_id: UUID) -> None:
        tenant_id = dataset.tenant_id
        dataset_id = dataset.id
        
        self.datasets.delete(dataset)
        self.commit()

        self._log_deleted(actor_id=actor_id, tenant_id=tenant_id, dataset_id=dataset_id)

    def update_statistics(self, *, dataset: Dataset, documents_count: int, rows_count: int, columns_count: int) -> Dataset:

        self.datasets.update_statistics(
            dataset=dataset,
            documents_count=documents_count,
            rows_count=rows_count,
            columns_count=columns_count,
        )

        return self.commit_refresh(dataset)

    def paginate(self, *, tenant_id: UUID, pagination):
        return self.datasets.paginate_by_tenant(tenant_id=tenant_id, pagination=pagination)

    def _log_created(self, *, actor_id: UUID, dataset: Dataset) -> None:
        self.activity.log(
            actor_id=actor_id,
            tenant_id=dataset.tenant_id,
            action=ActivityAction.DATASET_CREATED,
            target_type="dataset",
            target_id=dataset.id,
        )

    def _log_archived(self, *, actor_id: UUID, dataset: Dataset) -> None:
        self.activity.log(
            actor_id=actor_id,
            tenant_id=dataset.tenant_id,
            action=ActivityAction.DATASET_ARCHIVED,
            target_type="dataset",
            target_id=dataset.id,
        )

    def _log_restored(self, *, actor_id: UUID, dataset: Dataset) -> None:
        self.activity.log(
            actor_id=actor_id,
            tenant_id=dataset.tenant_id,
            action=ActivityAction.DATASET_RESTORED,
            target_type="dataset",
            target_id=dataset.id,
        )

    def _log_deleted(self, *, actor_id: UUID, tenant_id: UUID, dataset_id: UUID) -> None:
        self.activity.log(
            actor_id=actor_id,
            tenant_id=tenant_id,
            action=ActivityAction.DATASET_DELETED,
            target_type="dataset",
            target_id=dataset_id,
        )