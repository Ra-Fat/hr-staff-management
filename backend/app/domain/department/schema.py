from uuid import UUID
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None


class DepartmentSchema(BaseModel):
    uuid: UUID
    name: str
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)