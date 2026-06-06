from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    is_admin = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    subscriptions = relationship(
        "Subscription",
        back_populates="user"
    )

    uploads = relationship(
        "UploadedFile",
        back_populates="user"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    plan_name = Column(
        String(100)
    )

    is_active = Column(
        Boolean,
        default=True
    )

    start_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    expiry_date = Column(
        DateTime
    )

    user = relationship(
        "User",
        back_populates="subscriptions"
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    amount = Column(
        String(50)
    )

    currency = Column(
        String(10),
        default="NGN"
    )

    reference = Column(
        String(255),
        unique=True
    )

    status = Column(
        String(50)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    filename = Column(
        String(255)
    )

    original_filename = Column(
        String(255)
    )

    has_header = Column(
        Boolean,
        default=False
    )

    row_count = Column(
        Integer,
        default=0
    )

    column_count = Column(
        Integer,
        default=0
    )

    mongo_collection = Column(
        String(255)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="uploads"
    )

    columns = relationship(
        "ColumnMetadata",
        back_populates="file"
    )


class ColumnMetadata(Base):
    __tablename__ = "column_metadata"

    id = Column(
        Integer,
        primary_key=True
    )

    file_id = Column(
        Integer,
        ForeignKey("uploaded_files.id")
    )

    db_column = Column(
        String(100)
    )

    display_name = Column(
        String(255)
    )

    file = relationship(
        "UploadedFile",
        back_populates="columns"
    )
    
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    token = Column(String(255))

    expires_at = Column(DateTime)

    used = Column(Boolean, default=False)
    
class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    token = Column(String(255))

    expires_at = Column(DateTime)

    verified = Column(Boolean, default=False)