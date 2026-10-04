from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.tenant import TenantStatus
from core.models.tenant import Tenant
from core.models.user import User
from repositories.tenant_member_repository import TenantMemberRepository
from repositories.tenant_repository import TenantRepository
from repositories.user_repository import UserRepository


class TenantService:

    def __init__(self, db: Session) -> None:
        self.db = db

        self.tenants = TenantRepository(db)
        self.users = UserRepository(db)
        self.memberships = TenantMemberRepository(db)

    def by_id(self, tenant_id: UUID) -> Tenant:
        tenant = self.tenants.by_id(tenant_id)

        if tenant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found.")

        return tenant

    def by_slug(self, slug: str) -> Tenant:
        tenant = self.tenants.by_slug(slug=slug)

        if tenant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found.")

        return tenant

    def rename(self, *, tenant: Tenant, name: str) -> Tenant:
        tenant.name = name
        tenant.slug = self.tenants.generate_unique_slug(name)
        return tenant

    def update_description(self, *, tenant: Tenant, description: str | None) -> Tenant:
        tenant.description = description
        return tenant

    def update_logo(self, *, tenant: Tenant, logo_url: str | None) -> Tenant:
        tenant.logo_url = logo_url
        return tenant

    def update_settings(self, *, tenant: Tenant, settings: dict) -> Tenant:
        tenant.settings = settings
        return tenant

    def change_owner(self, *, tenant: Tenant, new_owner: User) -> Tenant:
        membership = self.memberships.membership(tenant_id=tenant.id, user_id=new_owner.id)

        if membership is None:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="New owner must be a member of the tenant.")

        tenant.owner_id = new_owner.id

        return tenant

    def activate(self, tenant: Tenant) -> Tenant:
        tenant.status = TenantStatus.ACTIVE
        return tenant

    def suspend(self, tenant: Tenant) -> Tenant:
        tenant.status = TenantStatus.SUSPENDED
        return tenant

    def archive(self, tenant: Tenant) -> Tenant:
        tenant.status = TenantStatus.ARCHIVED
        return tenant

    def delete(self, tenant: Tenant) -> None:
        self.tenants.delete(tenant)

    def members(self, tenant_id: UUID):
        return self.memberships.tenant_members(tenant_id)

    def member_count( self, tenant_id: UUID) -> int:
        return self.memberships.count(tenant_id=tenant_id)