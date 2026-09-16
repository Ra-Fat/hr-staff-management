from datetime import date as date_type
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.sql import ColumnElement

from app.domain.attendance.model import Attendance
from app.repositories.Base.base_repository import BaseRepository


class AttendanceRepository(BaseRepository[Attendance]):

    model_class = Attendance

    def build_filters(
        self,
        staff_id: Optional[int] = None,
        date_from: Optional[date_type] = None,
        date_to: Optional[date_type] = None,
    ) -> List[ColumnElement]:
        filters: List[ColumnElement] = []
        if staff_id is not None:
            filters.append(Attendance.staff_id == staff_id)
        if date_from is not None:
            filters.append(Attendance.date >= date_from)
        if date_to is not None:
            filters.append(Attendance.date <= date_to)
        return filters


    async def get_by_staff_and_date(
        self, 
        staff_id: int,
        target_date: date_type,
        include_deleted: bool = False
    )-> Optional[Attendance]:
        """The core lookup for check-in/check-out — is there already a
        record for this staff member today?"""
        stmt = select(Attendance).where(
            Attendance.staff_id == staff_id,
            Attendance.date == target_date,
        )
        if not include_deleted:
            stmt = stmt.where(Attendance.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_staff(
        self,
        staff_id: int,
        date_from: Optional[date_type] = None,
        date_to: Optional[date_type] = None,
        include_deleted: bool = False,
    ) -> List[Attendance]:
        stmt = select(Attendance).where(Attendance.staff_id == staff_id)
        if date_from is not None:
            stmt = stmt.where(Attendance.date >= date_from)
        if date_to is not None:
            stmt = stmt.where(Attendance.date <= date_to)
        if not include_deleted:
            stmt = stmt.where(Attendance.deleted_at.is_(None))
        stmt = stmt.order_by(Attendance.date.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    def default_order_by(self) -> List[ColumnElement]:
        return [Attendance.date.desc()]