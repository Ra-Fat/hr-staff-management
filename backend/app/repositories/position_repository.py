from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.sql import ColumnElement

from app.domain.position.model import Position
from app.repositories.Base.base_repository import BaseRepository

class PositionRepository(BaseRepository[Position]):
    model_class = Position

    def default_order_by(self) -> List[ColumnElement]:
        return [Position.title.asc()]

    def build_filters(self, title: Optional[str] = None) -> List[ColumnElement]:
        filters: List[ColumnElement] = []
        if title:
            filters.append(Position.title.ilike(f"%{title}%"))
        return filters

    async def exists_by_title(
        self, title: str, exclude_uuid: Optional[str] = None
    ) -> bool:
        stmt = select(Position.id).where(
            Position.title == title,
            Position.deleted_at.is_(None),
        )
        if exclude_uuid is not None:
            stmt = stmt.where(Position.uuid != exclude_uuid)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None