from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    get_current_user, require_permission
)
from app.core.database import get_db
from app.core.enum import StatusCode
from app.domain.department.schema import DepartmentUpdate, DepartmentCreate, DepartmentSchema
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService

router = APIRouter(
    prefix="/admin/departments",
    tags=["Departments"],
    dependencies=[Depends(get_current_user)],
)

def get_service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    return DepartmentService(DepartmentRepository(db))


@router.get("", dependencies=[Depends(require_permission("departments.list"))])
async def get_department_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: str = Query(None),
    service: DepartmentService = Depends(get_service),
):
    return await service.filter(page=page, page_size=page_size, name=name)

@router.get("/{department_uuid}", dependencies=[Depends(require_permission("departments.list"))])
async def view_department(
    department_uuid: UUID,
    service: DepartmentService = Depends(get_service),
):
    return await service.get(department_uuid)


@router.post("", status_code=StatusCode.CREATED, dependencies=[Depends(require_permission("departments.create"))])
async def create_department(
    data: DepartmentCreate,
    service: DepartmentService = Depends(get_service),
):
    return await service.create(data=data)

@router.put("/{department_uuid}", dependencies=[Depends(require_permission("departments.edit"))])
async def update_department(
    department_uuid: UUID,
    data: DepartmentUpdate,
    service: DepartmentService = Depends(get_service),
):
    return await service.update(department_uuid, data=data)

@router.delete("/{department_uuid}", dependencies=[Depends(require_permission("departments.delete"))])
async def delete_department(
    department_uuid: UUID,
    service: DepartmentService = Depends(get_service),
):
    return await service.delete(department_uuid)