from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.department.model import Department
from sqlalchemy.sql import ColumnElement
from app.domain.staff.model import Staff
from app.repositories.Base.base_repository import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    model_class = Department

    def build_filters(self, name: Optional[str] = None) -> List[ColumnElement]:
        """Turn query params into filter expressions for list_paginated()."""
        filters: List[ColumnElement] = []
        if name:
            filters.append(Department.name.ilike(f"%{name}%"))
        return filters

    async def get_by_name(
        self, name: str, include_deleted: bool = False
    ) -> Optional[Department]:
        stmt = select(Department).where(Department.name == name)
        if not include_deleted:
            stmt = stmt.where(Department.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def exists_by_name(
        self, name: str, exclude_uuid: Optional[str] = None
    ) -> bool:
        """Uniqueness check for the service layer, before create/update.
        Excludes the record's own uuid so renaming a department to its
        current name doesn't falsely report a conflict."""
        stmt = select(Department.id).where(
            Department.name == name,
            Department.deleted_at.is_(None),
        )
        if exclude_uuid is not None:
            stmt = stmt.where(Department.uuid != exclude_uuid)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def count_staff_grouped(self, department_ids: list[int]) -> dict[int, int]:
        """Returns number of staff for the given department ids in one query."""

        if not department_ids:
            return {}

        stmt = (
            select(Staff.department_id, func.count(Staff.id))
            .where(
                Staff.department_id.in_(department_ids),
                Staff.deleted_at.is_(None),
            )
            .group_by(Staff.department_id)
        )
        result = await self.session.execute(stmt)
        return {dept_id: count for dept_id, count in result.all()}

    def default_order_by(self) -> List[ColumnElement]:
        return [Department.name.asc()]