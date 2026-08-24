from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enum import UserStatus


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
    role_id: Optional[int] = None


class AdminUserSchema(BaseModel):
    uuid: UUID
    email: str
    full_name: Optional[str] = None
    status: UserStatus
     # The ORM relationship is named `account_roles`; expose it as `role` in the API.
    role: Optional[RoleRefSchema] = Field(None, validation_alias="account_roles")
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
