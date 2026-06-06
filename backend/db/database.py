from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker, declarative_base)
from core.config import settings 

engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=settings.DEBUG, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class DBConnection:

    def __init__(self, auto_commit: bool = True):
        self.db = None
        self.auto_commit = auto_commit

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type,  exc_val, exc_tb):
        if not self.db:
            return

        try:
            if exc_type:
                self.db.rollback()

            elif self.auto_commit:
                self.db.commit()

        finally:
            self.db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

def create_tables():
    from core.Models import (User, Subscription, Payment, UploadedFile, ColumnMetadata)

    Base.metadata.create_all(bind=engine)