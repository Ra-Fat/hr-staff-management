from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, text, Boolean
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from app.core.database import Base
from app.core.enum import AdminStatus
from app.core.utils import generate_uuid


class AdminUser(Base):
    __tablename__ = "auth_accounts"

    id = Column(Integer, primary_key= True, index= True)
    uuid = Column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),  
        default=generate_uuid,                   
        unique=True,
        index=True,
        nullable=False,                          
    )
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(191), nullable=True)

    last_login = Column(DateTime(timezone=True), nullable=True)

    status = Column(SqlEnum(AdminStatus, name="admin_status_enum"), nullable=False, default=AdminStatus.ACTIVE)
    role_id = Column(Integer, ForeignKey("auth_roles.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # soft deleted
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    role_obj = relationship("Role", back_populates="admin_users", lazy="selectin")
    staff_profile = relationship("Staff", back_populates="auth_account", uselist=False, lazy="noload")

    __table_args__ = (
        Index("idx_auth_accounts_email", "email"),
        UniqueConstraint("uuid"),
        Index("idx_auth_accounts_status", "status"),
    )
    