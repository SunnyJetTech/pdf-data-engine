from __future__ import annotations
import re
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload
from core.constants.dataset_constants import DatasetStatus
from core.models.dataset import Dataset
from core.pagination import Page, Pagination
from repositories.base_repository import BaseRepository

class DatasetRepository(BaseRepository[Dataset]):

    def __init__(self, db: Session) -> None:
        super().__init__(db=db, model=Dataset)

    def by_id(self, dataset_id: UUID) -> Dataset | None:
        stmt = select(Dataset).where(Dataset.id == dataset_id)

        return self.db.scalar(stmt)

    def by_slug(self, *, tenant_id: UUID, slug: str) -> Dataset | None:
        stmt = select(Dataset).where(Dataset.tenant_id == tenant_id, Dataset.slug == slug)

        return self.db.scalar(stmt)

    def by_creator(self, *, user_id: UUID) -> list[Dataset]:
        stmt = select(Dataset).where(Dataset.created_by == user_id).order_by( Dataset.created_at.desc(), Dataset.id.desc())

        return list(self.db.scalars(stmt).all())

    def by_tenant(self, *, tenant_id: UUID) -> list[Dataset]:
        stmt = select(Dataset).where(Dataset.tenant_id == tenant_id).order_by(Dataset.created_at.desc(), Dataset.id.desc())

        return list(self.db.scalars(stmt).all())

    def exists_slug(self, *, tenant_id: UUID, slug: str) -> bool:
        stmt = select(Dataset.id).where(Dataset.tenant_id == tenant_id,Dataset.slug == slug)

        return self.db.scalar(stmt) is not None

    def archive(self, dataset: Dataset) -> Dataset:
        dataset.status = DatasetStatus.ARCHIVED
        return dataset

    def restore(self, dataset: Dataset) -> Dataset:
        dataset.status = DatasetStatus.READY
        return dataset

    def update_statistics(self, *, dataset: Dataset, documents_count: int, rows_count: int, columns_count: int) -> Dataset:
        dataset.documents_count = documents_count
        dataset.rows_count = rows_count
        dataset.columns_count = columns_count

        return dataset

    def paginate_by_tenant(self, *, tenant_id: UUID, pagination: Pagination) -> Page[Dataset]:
        base_filter = Dataset.tenant_id == tenant_id

        stmt = (
            select(Dataset)
            .where(base_filter)
            .order_by( Dataset.created_at.desc(), Dataset.id.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        )

        count_stmt = select(func.count()).select_from(Dataset).where(base_filter)

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt).all())

        return Page.create(items=items, total=total, pagination=pagination)

    def with_documents(self, dataset_id: UUID) -> Dataset | None:
        stmt = select(Dataset).options(selectinload(Dataset.documents)).where(Dataset.id == dataset_id)

        return self.db.scalar(stmt)

    def ready(self, *, tenant_id: UUID) -> list[Dataset]:
        stmt = (
            select(Dataset)
            .where(Dataset.tenant_id == tenant_id,Dataset.status == DatasetStatus.READY)
            .order_by(Dataset.created_at.desc(),Dataset.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def processing(self, *, tenant_id: UUID) -> list[Dataset]:
        stmt = (
            select(Dataset)
            .where(Dataset.tenant_id == tenant_id,Dataset.status == DatasetStatus.PROCESSING)
            .order_by(Dataset.created_at.desc(),Dataset.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def search(self, *, tenant_id: UUID, keyword: str) -> list[Dataset]:
        keyword = keyword.strip()

        if not keyword:
            return self.by_tenant(tenant_id=tenant_id)

        stmt = (
            select(Dataset)
            .where(Dataset.tenant_id == tenant_id,Dataset.name.ilike(f"%{keyword}%"))
            .order_by(Dataset.created_at.desc(),Dataset.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def owned_by( self, *, dataset_id: UUID, user_id: UUID) -> Dataset | None:
        stmt = select(Dataset).where(Dataset.id == dataset_id,Dataset.created_by == user_id)

        return self.db.scalar(stmt)

    def change_status(self, *, dataset: Dataset, status: DatasetStatus) -> Dataset:
        
        dataset.status = status
        return dataset

    def update_statistics_from_documents(self, *, dataset: Dataset, documents_count: int, rows_count: int, columns_count: int) -> Dataset:
        return self.update_statistics(dataset=dataset, documents_count=documents_count, rows_count=rows_count, columns_count=columns_count)

    def generate_slug_candidate(self, name: str) -> str:
        base = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")

        return base or "dataset"