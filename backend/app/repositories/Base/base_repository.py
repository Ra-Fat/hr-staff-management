from typing import Any, Generic, List, Optional, Sequence, Tuple, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

ModelX = TypeVar('ModelT')

class BaseRepository(Generic[ModelX]):

    model_class: Type[ModelX]

    def __init__(self, session: AsyncSession) -> None:
                self.session = session

    async def get_by_id(self, id: Any) -> Optional[ModelX]:
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        return result.scalars().first()

    async def get_by_uuid(self, uuid: Any) -> Optional[ModelX]:
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.uuid == uuid)
        )
        return result.scalars().first()

    async def create(self, **kwargs: Any) -> ModelX:
        instance = self.model_class(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def save(self, instance: ModelX) -> ModelX:
        self.session.add(instance)
        await self.session.commit()

    async def delete(self, instance: ModelX) -> ModelX:
        await self.session.delete(instance)
        await self.session.commit()
        return instance
    