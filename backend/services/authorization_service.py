from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.tenant import TenantStatus
from core.models.permission import Permission
from core.models.role import Role
from core.models.tenant import Tenant
from core.models.tenant_member import MembershipStatus, TenantMember
from core.models.user import User
from repositories.permission_repository import PermissionRepository
from repositories.role_permission_repository import RolePermissionRepository
from repositories.role_repository import RoleRepository
from repositories.tenant_member_repository import TenantMemberRepository
from repositories.tenant_repository import TenantRepository


class AuthorizationService:

    def __init__(self, db: Session) -> None:
        self.db = db

        self.permissions = PermissionRepository(db)
        self.roles = RoleRepository(db)
        self.role_permissions = RolePermissionRepository(db)
        self.memberships = TenantMemberRepository(db)
        self.tenants = TenantRepository(db)

    def get_membership(self, *, user: User, tenant_id: uuid.UUID) -> TenantMember:
        membership = self.memberships.membership(tenant_id=tenant_id, user_id=user.id)

        if membership is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this tenant.")

        if membership.status != MembershipStatus.ACTIVE:
            raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Your tenant membership is not active.")

        if membership.role is None:
            raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Your tenant role is not configured.")

        if membership.role.tenant_id != tenant_id:
            raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Invalid tenant role.")

        return membership

    def tenant_access( self, *, user: User, tenant_id: uuid.UUID) -> Tenant:
        tenant = self.tenants.by_id(tenant_id)

        if tenant is None:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found.")

        if user.is_superuser:
            return tenant

        if tenant.status != TenantStatus.ACTIVE:
            raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Tenant is not active.")

        self.get_membership( user=user, tenant_id=tenant_id)

        return tenant

    @staticmethod
    def _permission_matches(permission: Permission, *, resource: str, action: str) -> bool:
        if ( permission.resource == resource and permission.action == action):
            return True

        if ( permission.resource == resource and permission.action == "*"): 
            return True

        if ( permission.resource == "*" and permission.action == "*"):
            return True

        return False

    def has_permission(self, *, user: User, tenant_id: uuid.UUID, resource: str, action: str) -> bool:
        if user.is_superuser:
            return True

        tenant = self.tenants.by_id(tenant_id)

        if tenant is None:
            return False

        if tenant.status != TenantStatus.ACTIVE:
            return False

        membership = self.memberships.membership(tenant_id=tenant_id, user_id=user.id)

        if membership is None:
            return False

        if membership.status != MembershipStatus.ACTIVE:
            return False

        role = membership.role

        if role is None:
            return False

        if role.tenant_id != tenant_id:
            return False

        role_permissions = self.role_permissions.by_role(role.id,)

        return any(
            assignment.permission is not None
            and self._permission_matches( assignment.permission, resource=resource, action=action)
            for assignment in role_permissions
        )

    def require_permission(self, *, user: User, tenant_id: uuid.UUID, resource: str, action: str) -> None:
        if not self.has_permission(user=user, tenant_id=tenant_id, resource=resource, action=action):
            raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")

    def get_role(self, *, tenant_id: uuid.UUID, role_id: uuid.UUID) -> Role:
        role = self.roles.by_id(role_id)

        if role is None:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")

        if role.tenant_id != tenant_id:
            raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Role does not belong to this tenant.")

        return role

    def ensure_owner_role(self, *, tenant_id: uuid.UUID) -> Role:
        role = self.roles.owner_role(tenant_id)

        if role is not None:
            return role

        role = Role( tenant_id=tenant_id, name="Owner", description="Tenant owner", is_system=True)

        self.db.add(role)
        self.db.flush()

        return role

    def assign_role( self, *, actor: User, tenant_id: uuid.UUID, member: TenantMember, role_id: uuid.UUID) -> TenantMember:
        self.require_permission( user=actor, tenant_id=tenant_id, resource="members", action="manage")

        if member.tenant_id != tenant_id:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Member does not belong to this tenant.")

        role = self.get_role(tenant_id=tenant_id, role_id=role_id)

        member.role_id = role.id

        return member
    
    def assign_permission(self, *, actor: User, tenant_id: uuid.UUID, role_id: uuid.UUID, permission_id: uuid.UUID) -> None:
        self.require_permission( user=actor, tenant_id=tenant_id, resource="roles", action="manage")

        role = self.get_role( tenant_id=tenant_id, role_id=role_id)

        permission = self.permissions.by_id(permission_id)

        if permission is None:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found.")

        if self.role_permissions.assignment_exists(
            role_id=role.id,
            permission_id=permission.id,
        ):
            return

        self.role_permissions.assign(
            role_id=role.id,
            permission_id=permission.id,
        )

    def revoke_permission( self, *, actor: User, tenant_id: uuid.UUID, role_id: uuid.UUID, permission_id: uuid.UUID) -> None:

        self.require_permission( user=actor, tenant_id=tenant_id, resource="roles", action="manage")

        self.get_role(tenant_id=tenant_id, role_id=role_id)

        permission = self.permissions.by_id(permission_id)

        if permission is None:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found.")

        self.role_permissions.revoke(role_id=role_id, permission_id=permission_id)