from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None


class DepartmentSchema(BaseModel):
    uuid: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)