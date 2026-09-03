from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enum import AdminStatus


class RoleRefSchema(BaseModel):
    uuid: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class AdminUserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role_id: int
    password: Optional[str] = None


class AdminUserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_uuid: Optional[int] = None


class AdminUserSchema(BaseModel):
    uuid: UUID
    email: str
    full_name: Optional[str] = None
    status: AdminStatus
    role: Optional[RoleRefSchema] = Field(None, validation_alias="role_obj")
    last_login: Optional[datetime] = None

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
