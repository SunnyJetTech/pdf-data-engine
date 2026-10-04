from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.models.invitation import Invitation
from repositories.base_repository import BaseRepository

class InvitationRepository(BaseRepository[Invitation]):

    def __init__(self, db):
        super().__init__(db=db, model=Invitation)

    def by_id(self, invitation_id: uuid.UUID) -> Invitation | None:
        stmt = select(Invitation).where(Invitation.id == invitation_id)

        return self.db.scalar(stmt)

    def by_token(self, token: str) -> Invitation | None:
        stmt = (
            select(Invitation)
            .options(joinedload(Invitation.tenant), joinedload(Invitation.role))
            .where(Invitation.token == token)
        )

        return self.db.scalar(stmt)

    def pending_by_email(self, email: str) -> list[Invitation]:
        stmt = (
            select(Invitation)
            .options(joinedload(Invitation.tenant), joinedload(Invitation.role))
            .where(Invitation.email == email, Invitation.accepted_at.is_(None))
            .order_by(Invitation.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    def tenant_invitations(self, tenant_id: uuid.UUID) -> list[Invitation]:
        stmt = select(Invitation).where(Invitation.tenant_id == tenant_id).order_by(Invitation.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def active_invitation(self, *, tenant_id: uuid.UUID, email: str) -> Invitation | None:
        stmt = (
            select(Invitation)
            .where(Invitation.tenant_id == tenant_id, Invitation.email == email, Invitation.accepted_at.is_(None))
            .order_by(Invitation.created_at.desc())
        )

        return self.db.scalar(stmt)

    def expired(self) -> list[Invitation]:
        stmt = select(Invitation).where(Invitation.accepted_at.is_(None), Invitation.expires_at < datetime.utcnow())

        return list(self.db.scalars(stmt).all())

    def mark_accepted(self, invitation: Invitation) -> Invitation:
        invitation.accepted_at = datetime.utcnow()

        return invitation
    
