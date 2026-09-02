from typing import Any, Generic, List, Optional, Sequence, Tuple, Type, TypeVar
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

ModelX = TypeVar('ModelT')

class BaseRepository(Generic[ModelX]):

    model_class: Type[ModelX]

    def __init__(self, session: AsyncSession) -> None:
                self.session = session

    async def get_by_id(self, id: Any, include_deleted: bool= False) -> Optional[ModelX]:
        stmt = select(self.model_class).where(self.model_class.id == id)
        if not include_deleted:
            stmt = stmt.where(self.model_class.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_uuid(self, uuid: Any, include_deleted: bool = False) -> Optional[ModelX]:
        stmt = select(self.model_class).where(self.model_class.uuid == uuid)
        if not include_deleted:
            stmt = stmt.where(self.model_class.deleted_at.is_(None))
        result = await self.session.execute(stmt)
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

    async def hard_delete(self, instance: ModelX) -> ModelX:
        """Use only  to remove the row permanently."""
        await self.session.delete(instance)
        await self.session.commit()
        return instance

    async def restore(self, instance: ModelX) -> ModelX:
        instance.deleted_at = None
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelX) -> ModelX:
        "Soft Delete: stamps delete_at instead of removing the row"
        instance.deleted_at = datetime.now(timezone.utc)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def list_paginated(
        self, 
        page: int= 1,
        page_size: int = 10,
        filters: Optional[Sequence[ColumnElement]] = None,
        order_by: Optional[Sequence[ColumnElement]] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ModelX], int, int]:

        page = max(page, 1)
        page_size = max(page_size, 1)

        where = list(filters) if filters else []
        if not include_deleted:
            where.append(self.model_class.deleted_at.is_(None))
        
        order = order_by if order_by is not None else self.default_order_by()

        total_records: int = (
            await self.session.execute(
                select(func.count()).select_from(self.model_class).where(*where)
            )
        ).scalar_one()

        stmt = select(self.model_class).where(*where)
        if order:
            stmt = stmt.order_by(*order)
        offset = (page - 1) * page_size
        rows = (
            await self.session.execute(stmt.offset(offset).limit(page_size))
        ).scalars().all()


        total_pages = (total_records + page_size -1) // page_size if total_records else 0 
        return list(rows), total_records, total_pages

    def build_filters(self, **kwargs: Any) -> List[ColumnElement]:
         return []

    def default_order_by(self) -> List[ColumnElement]:
        return []
    