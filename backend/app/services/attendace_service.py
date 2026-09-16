from datetime import date as date_type, datetime, timezone, time
from typing import Any, Optional
from zoneinfo import ZoneInfo
from app.core.exceptions import BadRequestError, NotFoundError, ForbiddenError
from app.core.lib.translate import get_translation
from app.core.responses import app_success
from app.domain.attendance.schema import AttendanceSchema
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.staff_repository import StaffRepository
from app.core.geo import distance_meters
from app.core.config import settings
from app.services.base.base_service import BaseService

_TZ = ZoneInfo(settings.OFFICE_TIMEZONE)

def _parse_time(value: str) -> time:
    hour, minute = map(int, value.split(":"))
    return time(hour, minute)

OFFICE_LATITUDE = settings.OFFICE_LATITUDE
OFFICE_LONGITUDE = settings.OFFICE_LONGITUDE
OFFICE_RADIUS_METERS = settings.OFFICE_RADIUS_METERS

CHECK_IN_START = _parse_time(settings.CHECK_IN_SCHEDULE_START)
CHECK_IN_END = _parse_time(settings.CHECK_IN_SCHEDULE_END)
CHECK_OUT_START = _parse_time(settings.CHECK_OUT_SCHEDULE_START)
CHECK_OUT_END = _parse_time(settings.CHECK_OUT_SCHEDULE_END)

class AttendanceService(BaseService[AttendanceRepository]):
    response_schema = AttendanceSchema

    def __init__(self, repository: AttendanceRepository, staff_repository: StaffRepository) -> None:
        super().__init__(repository)
        self.staff_repository = staff_repository

    async def _get_or_raise(
        self,
        uuid: Any,
        not_found_msg: Optional[str] = None,
        include_deleted: bool = False,
    ):
        instance = await self.repository.get_by_uuid(uuid, include_deleted=include_deleted)
        if not instance:
            raise NotFoundError(not_found_msg or get_translation("attendance_not_found"))
        return instance

    async def _resolve_staff_id(self, staff_uuid) -> int:
        staff = await self.staff_repository.get_by_uuid(staff_uuid)
        if not staff:
            raise NotFoundError(get_translation("staff_not_found"))
        return staff.id

    def _now_local(self) -> datetime:
        return datetime.now(_TZ)

    def _validate_location(self, latitude: float, longitude: float):
        dist = distance_meters(latitude, longitude, OFFICE_LATITUDE, OFFICE_LONGITUDE)
        if dist > OFFICE_RADIUS_METERS:
            raise ForbiddenError(get_translation("outside_allowed_location"))

    def _assert_within_schedule(self, start: time, end: time, error_key: str) -> None:
        """Raise if the current local time falls outside the allowed [start, end] range."""
        now_time = self._now_local().time()
        if not (start <= now_time <= end):
            raise BadRequestError(get_translation(error_key))

    def _assert_within_office_range(self, latitude: float, longitude: float) -> None:
        """Raise if the given coordinates are farther than OFFICE_RADIUS_METERS from the office."""
        dist = distance_meters(latitude, longitude, OFFICE_LATITUDE, OFFICE_LONGITUDE)
        if dist > OFFICE_RADIUS_METERS:
            raise ForbiddenError(get_translation("outside_allowed_location"))

    async def check_in(self, staff_uuid, latitude: float, longitude: float):
        self._assert_within_schedule(CHECK_IN_START, CHECK_IN_END, "check_in_outside_range")
        self._assert_within_office_range(latitude, longitude)

        staff_id = await self._resolve_staff_id(staff_uuid)
        now = self._now_local()
        today = now.date()

        existing = await self.repository.get_by_staff_and_date(staff_id, today)
        if existing:
            if existing.check_in is not None:
                raise BadRequestError(get_translation("already_checked_in"))
            existing.check_in = now
            await self.repository.save(existing)
            return app_success(data=self.serialize(existing))

        instance = await self.repository.create(staff_id=staff_id, date=today, check_in=now)
        return app_success(data=self.serialize(instance))

    async def check_out(self, staff_uuid, latitude: float, longitude: float):
        self._assert_within_schedule(CHECK_OUT_START, CHECK_OUT_END, "check_out_outside_window")
        self._assert_within_office_range(latitude, longitude)

        staff_id = await self._resolve_staff_id(staff_uuid)
        today = self._now_local().date()

        record = await self.repository.get_by_staff_and_date(staff_id, today)
        if not record or record.check_in is None:
            raise BadRequestError(get_translation("not_checked_in_yet"))
        if record.check_out is not None:
            raise BadRequestError(get_translation("already_checked_out"))

        record.check_out = self._now_local()
        await self.repository.save(record)
        return app_success(data=self.serialize(record))

    async def get_my_attendance(
        self,
        staff_uuid,
        date_from=None,
        date_to=None,
    ):
        staff_id = await self._resolve_staff_id(staff_uuid)
        rows = await self.repository.list_by_staff(staff_id, date_from=date_from, date_to=date_to)
        return app_success(data=[self.serialize(r) for r in rows])