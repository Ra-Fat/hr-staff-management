from typing import Any, List, Optional
 
from sqlalchemy import select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.models.department import Department
from app.repositories.base.base_repository import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    model_class = Department
 
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
 
    async def get_by_name(self, name: str) -> Optional[Department]:
        result = await self.session.execute(
            select(Department).where(Department.name == name)
        )
        return result.scalars().first()


    def build_filters(self, name: Optional[str] = None, **kwargs: Any) -> List[ColumnElement]:
        filters: List[ColumnElement] = []
        if name is not None:
            filters.append(Department.name.ilike(f"%{name}%"))
        return filters
 
    def default_order_by(self) -> List[ColumnElement]:
        return [Department.name]

    