from datetime import date as date_type
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_current_staff_uuid, require_permission
from app.core.database import get_db
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.staff_repository import StaffRepository
from app.services.attendace_service import AttendanceService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
    dependencies=[Depends(get_current_user)],
)

def get_service(db: AsyncSession = Depends(get_db)) -> AttendanceService:
    return AttendanceService(AttendanceRepository(db), StaffRepository(db))

@router.get("", dependencies=[Depends(require_permission("attendance.list"))])
async def get_attendance_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    staff_id: int = Query(None),
    date_from: date_type = Query(None),
    date_to: date_type = Query(None),
    service: AttendanceService = Depends(get_service),
):
    return await service.filter(
        page=page, page_size=page_size,
        staff_id=staff_id, date_from=date_from, date_to=date_to,
    )

@router.get("/{attendance_uuid}", dependencies=[Depends(require_permission("attendance.list"))])
async def view_attendance(
    attendance_uuid: UUID,
    service: AttendanceService = Depends(get_service),
):
    return await service.get(attendance_uuid)


@router.post("/check-in")
async def check_in(
    staff_uuid: UUID = Depends(get_current_staff_uuid),
    service: AttendanceService = Depends(get_service),
):
    return await service.check_in(staff_uuid)

@router.post("/check-out")
async def check_out(
    staff_uuid: UUID = Depends(get_current_staff_uuid),
    service: AttendanceService = Depends(get_service),
):
    return await service.check_out(staff_uuid)