from typing import Any, List, Optional
 
from sqlalchemy import select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
 
from app.domain.role.model import Role, Permission, RolePermission
from app.repositories.Base.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    model_class = Role
 
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


    async def get_by_name(self, name: str) -> Optional[Role]:
        result = await self.session.execute(select(Role).where(Role.name == name))
        return result.scalars().first()


    async def _get_with_permission(self, match: ColumnElement) -> Optional[Role]:
        result = await self.session.execute(
            select(Role)
            .where(match)
            .options(
                selectinload(Role.role_permissions).selectinload(RolePermission.permission)
            )
        )
        return result.scalars().first()

    async def get_with_permissions(self, role_id: int) -> Optional[Role]:
        return await self._get_with_permission(Role.id == role_id)

    async def get_with_permission_by_uuid(self, uuid) -> Optional[Role]:
        """Role lookup keyed on the public `uuid` — what the role routes resolve
        by. get_with_permissions (by id) is kept for internal re-fetches after
        create/update."""
        return await self._get_with_permissions(Role.uuid == uuid)


    async def set_permissions(self, role: Role, permission_ids: List[int]) -> Optional[Role]:
        await self.session.execute(
            RolePermission.__table__.delete().where(RolePermission.role_id == role.id)
        )
        for permission_id in permission_ids:
            self.session.add(
                RolePermission(role_id=role.id, permission_id=permission_id)
            )
        await self.session.commit()
        return await self.get_with_permissions(role.id)


    def build_filters(self, name: Optional[str] = None, **kwargs: Any) -> List[ColumnElement]:
        filters: List[ColumnElement] = []
        if name is not None:
            filters.append(Role.name.ilike(f"%{name}%"))
        return filters

    
    def default_order_by(self) -> List[ColumnElement]:
        return [Role.name]


# Permission Repo

class PermissionRepository(BaseRepository[Permission]):
    model_class = Permission

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_codename(self, codename: str) -> Optional[Permission]:
        result = await self.session.execute(
            select(Permission).where(Permission.codename == codename)
        )
        return result.scalars().first()

    async def list_all(self) -> List[Permission]:
        result = await self.session.execute(
            select(Permission).order_by(Permission.module, Permission.id)
        )
        return list(result.scalars().all())

    async def get_by_ids(self, ids: List[int]) -> List[Permission]:
        result = await self.session.execute(
            select(Permission).where(Permission.id.in_(ids))
        )
        return list(result.scalars().all())
