from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class AttendanceCreate(BaseModel):
    staff_uuid: UUID
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    date: Optional[date] = None


class AttendanceCheckin(BaseModel):
    staff_uuid: UUID


class AttendanceCheckout(BaseModel):
    staff_uuid: UUID


class AttendanceSchema(BaseModel):
    uuid: UUID
    staff_uuid: UUID
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    date: date

    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)