from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enum import LeaveStatus, LeaveType


class StaffRefSchema(BaseModel):
    uuid: UUID
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestCreate(BaseModel):
    staff_uuod: UUID
    leave_type: LeaveType
    start_date: date
    end_date: date


class LeaveRequestUpdate(BaseModel):
    status: Optional[LeaveStatus] = None
    reviewed_by: Optional[int] = None


class LeaveRequestSchema(BaseModel):
    uuid: UUID
    staff_id: int
    leave_type: LeaveType
    start_date: date
    end_date: date
    status: LeaveStatus
    reviewed_by: Optional[UUID] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestDetailSchema(LeaveRequestSchema):
    staff: Optional[StaffRefSchema] = None
    reviewer_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)