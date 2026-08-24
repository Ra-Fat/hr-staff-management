# app/models/permission.py
from sqlalchemy import Column, Integer, String, text, Index, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.util import generate_uuid


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=generate_uuid, primary_key=True, index=True)
    
    module = Column(String(100), nullable=False)
    group = Column(String(100), nullable=True)
    name = Column(String(191), nullable=False)
    codename = Column(String(191), nullable=False, unique=True)

    role_permissions = relationship("RolePermission", back_populates="permission", lazy="noload")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        Index("idx_permissions_module", "module"),
        Index("idx_permissions_codename", "codename"),
    )


class Role(Base):
    __tablename__ = "auth_roles"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=generate_uuid, primary_key=True, index=True)

    description = Column(String(255), nullable=True)

    role_permissions = relationship("RolePermission", back_populates="role",lazy="selectin", cascade="all, delete-orphan")
    admin_users = relationship("AdminUser", back_populates="role_obj", lazy="noload")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_roles_name", "name"),
    )


class RolePermission(Base):
    __tablename__ = "auth_role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=generate_uuid, primary_key=True, index=True)

    role_id = Column(Integer, ForeignKey("auth_roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("auth_permissions.id", ondelete="CASCADE"), nullable=False)

    role = relationship("Role", back_populates="role_permissions", lazy="noload")
    permission = relationship("Permission", back_populates="roles", lazy="selectin")