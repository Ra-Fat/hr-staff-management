from typing import Any, Optional

from app.core.exceptions import NotFoundError, ConflictError
from app.core.lib.translate import get_translation
from app.core.responses import app_success, app_success_paginated
from app.repositories.department_repository import DepartmentRepository
from app.domain.department.schema import DepartmentCreate, DepartmentSchema, DepartmentUpdate
from app.services.base.base_service import BaseService

class DepartmentService(BaseService[DepartmentRepository]):
    response_schema = DepartmentSchema

    async def _get_or_raise(
        self,
        uuid: Any,
        not_found_msg: Optional[str] = None,
        include_deleted: bool = False,
    ):
        instance = await self.repository.get_by_uuid(uuid, include_deleted=include_deleted)
        if not instance:
            raise NotFoundError(not_found_msg or get_translation("department_not_found"))
        return instance

    async def get(self, uuid: Any, not_found_msg: Optional[str] = None, include_deleted: bool = False):
        instance = await self._get_or_raise(uuid, not_found_msg, include_deleted=include_deleted)
        count = await self.repository.count_by_department(instance.id)
        data = self.serialize(instance)
        data["staff_count"] = count
        return app_success(data=data)

    async def create(self, data: DepartmentCreate):
        if await self.repository.exists_by_name(data.name):
            raise ConflictError(get_translation("department_name_taken"))

        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        instance = await self.repository.create(**payload)
        return app_success(data=self.serialize(instance))

    async def update(self, uuid: Any, data: DepartmentUpdate, not_found_msg: Optional[str] = None):
        instance = await self._get_or_raise(uuid, not_found_msg)

        if data.name is not None:
            if data.name != instance.name and await self.repository.exists_by_name(data.name, exclude_uuid=uuid):
                raise ConflictError(get_translation("department_name_taken"))
            instance.name = data.name

        await self.repository.save(instance)

        instance = await self._get_or_raise(uuid)
        return app_success(data=self.serialize(instance))

    async def filter(self, page: int = 1, page_size: int = 10, include_deleted: bool = False, **filter_params: Any):
        filters = self.repository.build_filters(**filter_params)
        rows, total, pages = await self.repository.list_paginated(
            page=page, page_size=page_size, filters=filters, include_deleted=include_deleted,
        )

        counts = await self.repository.count_staff_grouped([row.id for row in rows])

        lists = []
        for row in rows:
            data = self.serialize(row)
            data["staff_count"] = counts.get(row.id, 0)
            lists.append(data)

        return app_success_paginated(
            total_records=total, total_pages=pages,
            current_page=page, page_size=page_size,
            lists=lists,
        )
 
    