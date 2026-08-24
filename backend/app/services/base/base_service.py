import logging
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel

from app.core.exceptions import NotFoundError
from app.core.lib.translate import get_translation
# from app.core.responses import app_success, app_success_paginated
from app.core.responses import app_success, app_success_paginated



logger = logging.getLogger(__name__)

RepoT = TypeVar("RepoT")

class BaseService(Generic[RepoT]):
    """
    Generic CRUD service.

    Subclasses declare:
        response_schema : Type[BaseModel] — the Pydantic schema used to
        serialise every instance, so list and detail endpoints always
        return the same shape.

    Methods raise domain exceptions (NotFoundError, ConflictError, etc.)
    instead of returning error dicts — callers get typed success responses
    and exceptions are caught by the global handlers in main.py.
    """

    response_schema: Type[BaseModel]

    def __init__(self, repository: RepoT) -> None:
        self.repository = repository


    def serialize(self, instance: Any) -> Dict[str, Any]:
        return self.response_schema.model_validate(instance).model_dump(mode="json")

    async def _get_or_raise(self, id: Any, not_found_msg: str = None) -> Any:
        instance = await self.repository.get_by_id(id)
        if not instance:
            raise NotFoundError(not_found_msg or get_translation("record_not_found"))
        return instance

    async def filter(self, page: int = 1, page_size: int = 10, **filter_params: Any):
        filters = self.repository.build_filters(**filter_params)
        rows, total, pages = await self.repository.list_paginated(
            page=page, page_size=page_size, filters=filters,
        )
        return app_success_paginated(
            total_records=total, total_pages=pages,
            current_page=page, page_size=page_size,
            lists=[self.serialize(r) for r in rows],
        )


    async def list(self, page: int = 1, page_size: int = 10):
        return await self.filter(page=page, page_size=page_size)

    async def get(self, id: Any, not_found_msg: str = None):
        instance = await self._get_or_raise(id, not_found_msg)
        return app_success(data=self.serialize(instance))

    async def create(self, data: BaseModel):
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        instance = await self.repository.create(**payload)
        return app_success(data=self.serialize(instance))

    async def update(self, id: Any, data: BaseModel, not_found_msg: str = None):
        instance = await self._get_or_raise(id, not_found_msg)
        for field, value in data.model_dump().items():
            if value is not None:
                setattr(instance, field, value)
        await self.repository.save(instance)
        return app_success(data=self.serialize(instance))

    async def delete(self, id: Any, not_found_msg: str = None):
        instance = await self._get_or_raise(id, not_found_msg)
        deleted = await self.repository.delete(instance)
        return app_success(data=self.serialize(deleted))