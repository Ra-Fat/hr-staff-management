from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.sql import ColumnElement

from app.core.enum import StaffStatus
from app.domain.staff.model import Staff
from app.repositories.Base.base_repository import BaseRepository


class StaffRepository(BaseRepository[Staff]):

    model_class = Staff

    def build_filters(
        self,
        search: Optional[str] = None,
        department_id: Optional[int] = None,
        status: Optional[StaffStatus] = None,
    ) -> List[ColumnElement]:
        """Turn query params into filter expressions for list_paginated()."""
        filters: List[ColumnElement] = []

        if search:
            like = f"%{search}%"
            filters.append(
                or_(
                    Staff.first_name.ilike(like),
                    Staff.last_name.ilike(like),
                    Staff.position.ilike(like),
                )
            )

        if department_id is not None:
            filters.append(Staff.department_id == department_id)
        if status is not None:
            filters.append(Staff.status == status)

        return filters


    async def get_by_uuid(
        self, uuid, include_deleted: bool = False
    ) -> Optional[Staff]:
        """Override base to eager-load relationships needed for a staff
        detail view"""
        return await super().get_by_uuid(uuid, include_deleted=include_deleted)


    async def get_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> Optional[Staff]:
        """Look up the staff profile for a logged-in"""
        stmt = select(Staff).where(Staff.user_id == user_id)
        if not include_deleted:
            stmt = stmt.where(Staff.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_department(
        self, department_id: int, include_deleted: bool = False
    ) -> List[Staff]:
        """Used for department manager views and the 'assign manager'
        picker — pulls every staff member in one department."""
        stmt = select(Staff).where(Staff.department_id == department_id)
        if not include_deleted:
            stmt = stmt.where(Staff.deleted_at.is_(None))
        stmt = stmt.order_by(*self.default_order_by())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    