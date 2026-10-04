from __future__ import annotations
import uuid
import re
import unicodedata
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.models.tenant import Tenant
from repositories.base_repository import BaseRepository


class TenantRepository(BaseRepository[Tenant]):

    def __init__(self, db):
        super().__init__(db=db, model=Tenant)

    def by_id(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).where(Tenant.id == tenant_id)

        return self.db.scalar(stmt)

    def by_slug(self, slug: str) -> Tenant | None:
        stmt = select(Tenant).where(Tenant.slug == slug)

        return self.db.scalar(stmt)

    def by_owner(self, owner_id: uuid.UUID) -> list[Tenant]:
        stmt = select(Tenant).where(Tenant.owner_id == owner_id).order_by(Tenant.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def active(self) -> list[Tenant]:
        stmt = select(Tenant).where(Tenant.status == "active").order_by(Tenant.name.asc())

        return list(self.db.scalars(stmt).all())

    def with_members(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).options(joinedload(Tenant.members)).where(Tenant.id == tenant_id)

        return self.db.scalar(stmt)

    def with_datasets(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).options(joinedload(Tenant.datasets)).where(Tenant.id == tenant_id)

        return self.db.scalar(stmt)

    def with_api_keys(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).options(joinedload(Tenant.api_keys),).where(Tenant.id == tenant_id)

        return self.db.scalar(stmt)

    def with_webhooks(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).options(joinedload(Tenant.webhooks),).where(Tenant.id == tenant_id)

        return self.db.scalar(stmt)

    def with_invitations(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).options(joinedload(Tenant.invitations),).where(Tenant.id == tenant_id)

        return self.db.scalar(stmt)

    def generate_unique_slug(self, name: str) -> str:
        base_slug = self._slugify(name)
        slug = base_slug
        counter = 2

        while self.exists(slug=slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug
    
    @staticmethod
    def _slugify(value: str) -> str:

        value = unicodedata.normalize("NFKD", value)
        value = value.encode("ascii", "ignore").decode("ascii").lower().strip()
        value = re.sub(r"[^a-z0-9]+",   "-",   value)
        value = re.sub(r"-{2,}", "-", value)

        return value.strip("-")