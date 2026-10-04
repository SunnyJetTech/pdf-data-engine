# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
# from core.config import settings

# engine = create_engine(
#     settings.POSTGRES_DATABASE_URL,
#     echo=settings.DEBUG,
#     future=True,
# )

# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False,
# )

# class ORMBase(DeclarativeBase):
#     pass

# class DBConnection:

#     def __init__(self, auto_commit: bool = True):
#         self.db = None
#         self.auto_commit = auto_commit

#     def __enter__(self):
#         self.db = SessionLocal()
#         return self.db

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if not self.db:
#             return

#         try:
#             if exc_type:
#                 self.db.rollback()

#             elif self.auto_commit:
#                 self.db.commit()

#         finally:
#             self.db.close()

# def get_db():
#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()


# def create_tables():

#     from core.models import (
#         Activity,
#         Conversation,
#         Dataset,
#         Document,
#         Message,
#         Payment,
#         PricingPlan,
#         Quota,
#         SearchHistory,
#         Subscription,
#         Tenant,
#         TenantMember,
#         ToolCall,
#         AIUsage,
#         User,
#     )

#     ORMBase.metadata.create_all(bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from core.config import settings

engine = create_engine(
    settings.POSTGRES_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

class ORMBase(DeclarativeBase):
    pass


def get_db():
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        