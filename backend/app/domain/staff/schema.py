from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enum import StaffStatus


class DepartmentRefSchema(BaseModel):
    uuid: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class StaffCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    department_uuid: Optional[UUID] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    profile_url: Optional[str] = None
    salary: Optional[float] = None


class StaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department_uuid: Optional[UUID] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    salary: Optional[float] = None
    profile_url: Optional[str] = None
    status: Optional[StaffStatus] = None


class StaffSchema(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str
    full_name: str
    position: Optional[str] = None
    status: StaffStatus
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class StaffDetailSchema(StaffSchema):
    department: Optional[DepartmentRefSchema] = None
    salary: Optional[float] = None
    profile_url: Optional[str] = None
    hire_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)