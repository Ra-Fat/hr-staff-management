from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, require_permission
from app.core.database import get_db
from app.core.enum import StatusCode
from app.domain.position.schema import PositionCreate, PositionUpdate
from app.repositories.position_repository import PositionRepository
from app.services.position_service import PositionService

router = APIRouter(
    prefix="/positions",
    tags=["Positions"],
    dependencies=[Depends(get_current_user)],
)


def get_service(db: AsyncSession = Depends(get_db)) -> PositionService:
    return PositionService(PositionRepository(db))


@router.get("", dependencies=[Depends(require_permission("positions.list"))])
async def get_position_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: str = Query(None),
    service: PositionService = Depends(get_service),
):
    return await service.filter(page=page, page_size=page_size, title=title)


@router.get("/{position_uuid}", dependencies=[Depends(require_permission("positions.list"))])
async def view_position(
    position_uuid: UUID,
    service: PositionService = Depends(get_service),
):
    return await service.get(position_uuid)


@router.post("", status_code=StatusCode.CREATED, dependencies=[Depends(require_permission("positions.create"))])
async def create_position(
    data: PositionCreate,
    service: PositionService = Depends(get_service),
):
    return await service.create(data=data)


@router.put("/{position_uuid}", dependencies=[Depends(require_permission("positions.edit"))])
async def update_position(
    position_uuid: UUID,
    data: PositionUpdate,
    service: PositionService = Depends(get_service),
):
    return await service.update(position_uuid, data=data)


@router.delete("/{position_uuid}", dependencies=[Depends(require_permission("positions.delete"))])
async def delete_position(
    position_uuid: UUID,
    service: PositionService = Depends(get_service),
):
    return await service.delete(position_uuid)