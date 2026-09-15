from typing import Any, List, Optional
from sqlalchemy import func, select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from app.core.exceptions import ValidationError
from app.core.lib.translate import get_translation
from app.domain.admin_user.model import AdminUser
from app.domain.role.model import Role, RolePermission
from app.repositories.Base.base_repository import BaseRepository


class AdminUserRepository(BaseRepository[AdminUser]):
    model_class = AdminUser

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_email(self, email: str ) -> Optional[AdminUser]:
        stmt = select(AdminUser).where(AdminUser.email == email)
        return (await self.session.execute(stmt)).scalars().first()

    async def _get_scoped(self, match) -> Optional[AdminUser]:
        stmt = (
            select(AdminUser)
            .where(match)
            .options(
                selectinload(AdminUser.role_obj).selectinload(Role.role_permission).selectinload(RolePermission.permission)

            )

        )
        return (await self.session.execute(stmt)).scalars().first()

    async def get_by_id(self, id: Any) -> Optional[AdminUser]:
        return await self._get_scoped(AdminUser.id == id)

    async def get_by_uuid(self, uuid: Any) -> Optional[AdminUser]:
        return await self._get_scoped(AdminUser.uuid == uuid)

    def build_filters(
        self,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        role_id: Optional[int] = None,
        status: Optional[str] = None,
        **kwargs: Any 
    ) -> List[ColumnElement]:

        filters: List[ColumnElement] = []

        if full_name is not None:
            filters.append(AdminUser.full_name.ilike(f"%{full_name}%"))
        if email is not None:
            filters.append(AdminUser.email.ilike(f"%{email}%"))
        if role_id is not None:
            filters.append(AdminUser.role_id == role_id)
        if status is not None:
            try:
                filters.append(AdminUser.status == AdminUser(status))
            except ValueError:
                raise ValidationError(get_translation("invalid_filter_by"))
        
        return filters

    def default_order_by(self) -> List[ColumnElement]:
        return [AdminUser.id]