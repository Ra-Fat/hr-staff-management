from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, text, Boolean
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from sqlalchemy.schema import UniqueConstraint
from app.core.utils import generate_uuid


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=generate_uuid, unique=True, index=True)
    email = Column(String(191), nullable=False, unique=True)
    code_hash = Column(String(64), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    attempts = Column(Integer, nullable=False, default=0)
    last_sent_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        Index("idx_email_verifications_email", "email"),
        UniqueConstraint("uuid"),
        Index("idx_email_verifications_expires_at", "expires_at"),
    )


class TokenBlacklist(Base):
    __tablename__ = "auth_token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=generate_uuid, unique=True, index=True)
    
    jti = Column(String(64), nullable=False, unique=True, index=True)  # JWT unique ID
    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)