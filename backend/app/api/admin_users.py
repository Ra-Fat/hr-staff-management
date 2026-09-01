from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.auth import (
    get_current_user,
    get_current_user_id ,
    require_permission
)
from app.core.database import get_db
from app.core.enum import StatusCode
from app.domain.admin_user.schema import AdminUserCreate, AdminUserUpdate
from app.repositories.admin_user_repository import AdminUserRepository
from app.services.admin_user_service import AdminUserService


router = APIRouter(
    prefix= '/admin/users',
    tags= ["Admin Users"],
    dependencies= [Depends(get_current_user)], 
)

def get_service(db: AsyncSession = Depends(get_db)) -> AdminUserService:
    return AdminUserService(
        AdminUserRepository(db)
    )


@router.get("", dependencies=[Depends(require_permission("admin_users.list"))])
async def get_admin_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    full_name: str = Query(None),
    email: str = Query(None),
    role_id: int = Query(None),
    status: str = Query(None),
    service: AdminUserService = Depends(get_service)
):
    return await service.filter(
        page=page,
        page_size=page_size,
        full_name= full_name,
        email= email,
        role_id= role_id,
        status= status,
    )


@router.get("/{admin_uuid}", dependencies=[Depends(require_permission("admin_users_list"))])
async def view_admin_user(
    admin_uuid: str, 
    service: AdminUserService = Depends(get_service)
):
    return await service.get(admin_uuid)


@router.post("", status_code= StatusCode.CREATED, dependencies= [Depends(require_permission("admin_user_create"))])
async def create_admin_user(
    data: AdminUserCreate,
    service: AdminUserService = Depends(get_service)
):
    return await service.create(data=data)


@router.put("/{admin_uuid}", dependencies= [Depends(require_permission("admin_user_edit"))])
async def update_admin_user(
    admin_uuid: str,
    data: AdminUserUpdate,
    service: AdminUserService = Depends(get_service)
):
    return await service.updatre(admin_uuid, data=data)


@router.patch("/{admin_uuid}/disable", dependencies=[Depends(require_permission("admin_users.disable"))])
async def disable_admin_user(
    admin_uuid: UUID,
    service: AdminUserService = Depends(get_service),
):
    return await service.disable(admin_uuid)


@router.patch("/{admin_uuid}/enable", dependencies=[Depends(require_permission("admin_users.disable"))])
async def enable_admin_user(
    admin_uuid: UUID,
    service: AdminUserService = Depends(get_service),
):
    return await service.enable(admin_uuid)


@router.delete("/{admin_uuid}", dependencies=[Depends(require_permission("admin_users.delete"))])
async def delete_admin_user(
    admin_uuid: UUID,
    current_user_id: int = Depends(get_current_user_id),
    service: AdminUserService = Depends(get_service),
):
    return await service.delete(admin_uuid, current_user_id=current_user_id)