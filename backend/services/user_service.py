from __future__ import annotations
from sqlalchemy.orm import Session
from auth.password_manager import password_hash
from core.models.user import User
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)

    def by_id(self, user_id) -> User | None:
        return self.users.by_id(user_id)

    def by_email(self, email: str) -> User | None:
        return self.users.by_email(email=email)

    def by_username(self, username: str) -> User | None:
        return self.users.by_username(username=username)

    def activate(self, user: User) -> User:
        user.is_active = True
        return user

    def deactivate(self, user: User) -> User:
        user.is_active = False
        return user

    def change_password( self, *, user: User, new_password: str) -> User:
        user.password_hash = password_hash(new_password)

        return user