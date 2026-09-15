from typing import Any, Optional

from app.core.exceptions import ConflictError, NotFoundError
from app.core.lib.translate import get_translation
from app.core.responses import app_success
from app.domain.position.schema import PositionCreate, PositionSchema, PositionUpdate
from app.repositories.position_repository import PositionRepository
from app.services.base.base_service import BaseService

class PositionService(BaseService[PositionRepository]):
    response_schema = PositionSchema

    async def _get_or_raise(
        self,
        uuid: Any,
        not_found_msg: Optional[str] = None,
        include_deleted: bool = False,
    ):
        instance = await self.repository.get_by_uuid(uuid, include_deleted=include_deleted)
        if not instance:
            raise NotFoundError(not_found_msg or get_translation("position_not_found"))
        return instance

    async def create(self, data: PositionCreate):
        if await self.repository.exists_by_title(data.title):
            raise ConflictError(get_translation("position_title_taken"))

        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        instance = await self.repository.create(**payload)
        return app_success(data=self.serialize(instance))

    async def update(self, uuid: Any, data: PositionUpdate, not_found_msg: Optional[str] = None):
        instance = await self._get_or_raise(uuid, not_found_msg)

        if data.title is not None:
            if data.title != instance.title and await self.repository.exists_by_title(data.title, exclude_uuid=uuid):
                raise ConflictError(get_translation("position_title_taken"))
            instance.title = data.title

        if data.description is not None:
            instance.description = data.description

        await self.repository.save(instance)

        instance = await self._get_or_raise(uuid)
        return app_success(data=self.serialize(instance))