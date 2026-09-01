import logging
from typing import Any, Dict, Generic, Type, TypeVar, Optional

from pydantic import BaseModel

from app.core.exceptions import NotFoundError
from app.core.lib.translate import get_translation
from app.core.responses import app_success, app_success_paginated

logger = logging.getLogger(__name__)

RepoT = TypeVar("RepoT")

class BaseService(Generic[RepoT]):

    response_schema: Type[BaseModel]

    def __init__(self, repository: RepoT) -> None:
        self.repository = repository

    def serialize(self, instance: Any) -> Dict[str, Any]:
        return self.response_schema.model_validate(instance).model_dump(mode='json')

    async def _get_or_raise(
        self,
        id: Any,
        not_found_msg: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Any:
        instance = await self.repository.get_by_id(id, include_deleted=include_deleted)
        if not instance:
            raise NotFoundError(not_found_msg or get_translation('record_not_found'))
        return instance

    async def filter(
        self,
        page: int = 1,
        page_size: int = 10,
        include_deleted: bool = False,
        **filter_params: Any,
    ):
        filters = self.repository.build_filters(**filter_params)
        rows, total, pages = await self.repository.list_paginated(
            page=page, page_size=page_size, filters=filters,
            include_deleted=include_deleted,
        )
        return app_success_paginated(
            total_records=total, total_pages=pages,
            current_page=page, page_size=page_size,
            lists=[self.serialize(r) for r in rows]
        )

    async def list(self, page: int = 1, page_size: int = 10, include_deleted: bool = False):
        return await self.filter(page=page, page_size=page_size, include_deleted=include_deleted)

    async def get(self, id: Any, not_found_msg: str= None, include_deleted: bool = False):
        instance = await self._get_or_raise(id, not_found_msg, include_deleted=include_deleted)
        return app_success(data=self.serialize(instance))

    async def create(self, data: BaseModel):
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        instance = await self.repository.create(**payload)
        return app_success(data= self.serialize(instance))

    async def update(self, id: Any, data: BaseModel, not_found_msg: Optional[str] = None):
        instance = await self._get_or_raise(id, not_found_msg)
        for field, value in data.model_dump().items():
            if value is not None:
                setattr(instance, field, value)
        await self.repository.save(instance)
        return app_success(data=self.serialize(instance))

    async def delete(self, id: Any, not_found_msg: Optional[str] = None):
        """Soft delete a record."""
        instance = await self._get_or_raise(id, not_found_msg)
        deleted = await self.repository.delete(instance)
        return app_success(data=self.serialize(deleted))

    async def restore(self, id: Any, not_found_msg: Optional[str] = None):
        """Restore a previously soft-deleted record."""
        instance = await self._get_or_raise(id, not_found_msg, include_deleted=True)
        restored = await self.repository.restore(instance)
        return app_success(data=self.serialize(restored))

    async def hard_delete(self, id: Any, not_found_msg: Optional[str] = None):
        """Permanently remove a record"""
        instance = await self._get_or_raise(id, not_found_msg, include_deleted=True)
        deleted = await self.repository.hard_delete(instance)
        return app_success(data=self.serialize(deleted))