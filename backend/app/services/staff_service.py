from typing import Any, Optional

from pydantic import BaseModel
from uuid import UUID

from app.core.enum import StaffStatus
from app.core.exceptions import NotFoundError, ConflictError
from app.core.lib.translate import get_translation
from app.core.responses import app_success, app_success_paginated
from app.repositories.department_repository import DepartmentRepository
from app.repositories.position_repository import PositionRepository
from app.repositories.staff_repository import StaffRepository
from app.domain.staff.schema import StaffCreate, StaffSchema, StaffStatus, StaffUpdate
from app.services.base.base_service import BaseService


class StaffService(BaseService[StaffRepository]):

    response_schema = StaffSchema

    def __init__(
        self,
        repository: StaffRepository,
        department_repository: DepartmentRepository,
        position_repository: PositionRepository,
    ) -> None:
        super().__init__(repository)
        self.department_repository = department_repository
        self.position_repository = position_repository

    async def _get_or_raise(
        self,
        uuid: Any,
        not_found_msg: Optional[str] = None,
        include_deleted: bool = False,
    ):
        instance = await self.repository.get_by_uuid(uuid, include_deleted=include_deleted)
        if not instance:
            raise NotFoundError(not_found_msg or get_translation("staff_not_found"))
        return instance

    async def _validate_department(self, department_id: Optional[int]) -> None:
        if department_id is None:
            return
        department = await self.department_repository.get_by_id(department_id)
        if not department:
            raise NotFoundError(get_translation("department_not_found"))

    async def _resolve_department_id(self, department_uuid: Optional[UUID]) -> Optional[int]:
        """Translate the public department_uuid into the internal FK id."""
        if department_uuid is None:
            return None
        department = await self.department_repository.get_by_uuid(department_uuid)
        if not department:
            raise NotFoundError(get_translation("department_not_found"))
        return department.id

    async def _resolve_position_id(self, position_uuid: Optional[UUID]) -> Optional[int]:
        if position_uuid is None:
            return None
        position = await self.position_repository.get_by_uuid(position_uuid)
        if not position:
            raise NotFoundError(get_translation("position_not_found"))
        return position.id

    async def create(self, data: StaffCreate):
        payload = data.model_dump(exclude={"department_uuid", "position_uuid", "email"}, exclude_none=True)
        payload["department_id"] = await self._resolve_department_id(data.department_uuid)
        payload["position_id"] = await self._resolve_position_id(data.position_uuid)

        instance = await self.repository.create(**payload)
        return app_success(data=self.serialize(instance))
    
    async def update(self, uuid: Any, data: StaffUpdate, not_found_msg: Optional[str] = None):
        instance = await self._get_or_raise(uuid, not_found_msg)

        updates = data.model_dump(exclude={"department_uuid", "position_uuid"}, exclude_none=True)
        for field, value in updates.items():
            setattr(instance, field, value)

        if data.department_uuid is not None:
            instance.department_id = await self._resolve_department_id(data.department_uuid)

        if data.position_uuid is not None:
            instance.position_id = await self._resolve_position_id(data.position_uuid)

        await self.repository.save(instance)
        return app_success(data=self.serialize(instance))
    
    async def assign_department(self, uuid: Any, department_uuid: UUID):
        instance = await self._get_or_raise(uuid)
        instance.department_id = await self._resolve_department_id(department_uuid)
        await self.repository.save(instance)
        return app_success(data=self.serialize(instance))

    async def assign_position(self, uuid: Any, position_uuid: UUID):
        instance = await self._get_or_raise(uuid)
        instance.position_id = await self._resolve_position_id(position_uuid)
        await self.repository.save(instance)
        return app_success(data=self.serialize(instance))
    
    async def list_by_department(self, department_uuid: UUID):
        department = await self.department_repository.get_by_uuid(department_uuid)
        if not department:
            raise NotFoundError(get_translation("department_not_found"))
        rows = await self.repository.list_by_department(department.id)
        return app_success(data=[self.serialize(r) for r in rows])