from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PositionCreate(BaseModel):
    title: str
    description: Optional[str] = None


class PositionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PositionSchema(BaseModel):
    uuid: UUID
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)