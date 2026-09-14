from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    get_current_user, require_permission
)
from app.core.database import get_db
from app.core.enum import StatusCode
from app.domain.role.schema import RoleCreate, RoleUpdate
from app.repositories.role_repository import RoleRepository
from app.repositories.permission_repository import PermissionRepository
from app.services.role_service import RoleService

router = APIRouter(
    prefix="/admin/roles",
    tags=["Roles & Permissions"],
    dependencies=[Depends(get_current_user)],
)


def get_service(db: AsyncSession = Depends(get_db)) -> RoleService:
    return RoleService(
        RoleRepository(db),
        PermissionRepository(db),
    )

@router.get("")
async def list_roles(
    service: RoleService = Depends(get_service),
    _=Depends(require_permission("roles.view")),
):
    return await service.list_roles()


@router.get("/permissions")
async def list_permissions(
    service: RoleService = Depends(get_service),
    _=Depends(require_permission("roles.view")),
):
    return await service.list_permission()


@router.get("/{role_uuid}")
async def get_role(
    role_uuid: UUID,
    service: RoleService = Depends(get_service),
    _=Depends(require_permission("roles.view")),
):
    return await service.get_role(role_uuid)


@router.post("", status_code=StatusCode.CREATED)
async def create_role(
    data: RoleCreate,
    service: RoleService = Depends(get_service),
    _=Depends(require_permission("roles.create")),
):
    return await service.create_role(data)


@router.put("/{role_uuid}")
async def update_role(
    role_uuid: UUID,
    data: RoleUpdate,
    service: RoleService = Depends(get_service),
    _=Depends(require_permission("roles.edit")),
):
    return await service.update_role(role_uuid, data)


@router.delete("/{role_uuid}")
async def delete_role(
    role_uuid: UUID,
    service: RoleService = Depends(get_service),
    _=Depends(require_permission("roles.edit")),
):
    return await service.delete_role(role_uuid)
