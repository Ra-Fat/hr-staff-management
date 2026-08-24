from typing import Any, Generic, List, Optional, Sequence, Tuple, Type, TypeVar
 
from sqlalchemy import func, select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
 
ModelT = TypeVar("ModelT")

class BaseRepository(Generic[ModelT]):
    """
    Generic async repository — pure data access, no serialisation.
 
    Subclasses declare:
        model_class : Type[ModelT]  — the SQLAlchemy ORM model
 
    Override `build_filters` to return a list of SQLAlchemy column expressions
    that are passed directly to .where(*filters), and `default_order_by` to
    give listings a stable, deterministic order.
    """
 
    model_class: Type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
 
    async def get_by_id(self, id: Any) -> Optional[ModelT]:
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        return result.scalars().first()

    async def get_by_uuid(self, uuid: Any) -> Optional[ModelT]:
        """Look up by the public `uuid` identifier. `id` stays the internal PK;
        this is what the API layer resolves routes by."""
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.uuid == uuid)
        )
        return result.scalars().first()

    
    async def create(self, **kwargs: Any) -> ModelT:
        instance = self.model_class(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    
    async def save(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    
    async def delete(self, instance: ModelT) -> ModelT:
        await self.session.delete(instance)
        await self.session.commit()
        return instance


    async def list_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Sequence[ColumnElement]] = None,
        order_by: Optional[Sequence[ColumnElement]] = None,
    ) -> Tuple[List[ModelT], int, int]:
        # Defensive clamp: routers validate query params, but internal callers
        # may pass anything and a page <= 0 would produce a negative OFFSET.
        page = max(page, 1)
        page_size = max(page_size, 1)
 
        where = filters or []
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
 
        total_pages = (total_records + page_size - 1) // page_size if total_records else 0
        return list(rows), total_records, total_pages


    def build_filters(self, **kwargs: Any) -> List[ColumnElement]:
        """Override in subclasses to return a list of SQLAlchemy where-clause expressions."""
        return []

    
    def default_order_by(self) -> List[ColumnElement]:
        """Override in subclasses; without an ORDER BY, paginated results are
        not guaranteed to be stable across pages."""
        return []