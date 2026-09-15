from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_current_user_id, require_permission
from app.core.database import get_db
from app.core.enum import StaffStatus, StatusCode
from app.domain.staff.schema import StaffCreate, StaffUpdate
from app.repositories.department_repository import DepartmentRepository
from app.repositories.position_repository import PositionRepository
from app.repositories.staff_repository import StaffRepository
from app.services.staff_service import StaffService

router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
    dependencies=[Depends(get_current_user)],
)

def get_service(db: AsyncSession = Depends(get_db)) -> StaffService:
    return StaffService(
        StaffRepository(db),
        DepartmentRepository(db),
        PositionRepository(db),
    )

@router.get("", dependencies=[Depends(require_permission("staff.list"))])
async def get_staff_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    department_id: int = Query(None),
    status: StaffStatus = Query(None),
    service: StaffService = Depends(get_service),
):
    return await service.filter(
        page=page,
        page_size=page_size,
        search=search,
        department_id=department_id,
        status=status,
    )

@router.get("/{staff_uuid}", dependencies=[Depends(require_permission("staff.view"))])
async def view_staff(
    staff_uuid: UUID,
    service: StaffService = Depends(get_service),
):
    return await service.get(staff_uuid)

@router.post("", status_code=StatusCode.CREATED, dependencies=[Depends(require_permission("staff.create"))])
async def create_staff(
    data: StaffCreate,
    service: StaffService = Depends(get_service),
):
    return await service.create(data=data)

@router.put("/{staff_uuid}", dependencies=[Depends(require_permission("staff.edit"))])
async def update_staff(
    staff_uuid: UUID,
    data: StaffUpdate,
    service: StaffService = Depends(get_service),
):
    return await service.update(staff_uuid, data=data)

@router.patch("/{staff_uuid}/department", dependencies=[Depends(require_permission("staff.edit"))])
async def assign_staff_department(
    staff_uuid: UUID,
    department_uuid: UUID,
    service: StaffService = Depends(get_service),
):
    return await service.assign_department(staff_uuid, department_uuid)

@router.delete("/{staff_uuid}", dependencies=[Depends(require_permission("staff.delete"))])
async def delete_staff(
    staff_uuid: UUID,
    service: StaffService = Depends(get_service),
):
    return await service.delete(staff_uuid)
