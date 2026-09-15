from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.role.model import Role, RolePermission
from app.repositories.Base.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    
    model_class = Role

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def _get_with_permissions(
        self, match
    ) -> Optional[Role]:
        stmt = (
            select(Role)
            .where(match)
            .options(
                selectinload(Role.role_permission).selectinload(RolePermission.permission)
            )
        )
        return (await self.session.execute(stmt)).scalars().first()

    async def get_by_name(
        self,
        name: str,
    ) -> Optional[Role]:
        stmt = select(Role).where(Role.name == name)
        return (await self.session.execute(stmt)).scalars().first()

    async def get_with_permissions(
        self,
        role_id: int,
    ) -> Optional[Role]:
        return await self._get_with_permissions(Role.id== role_id)

    async def get_with_permission_uuid(
        self,
        uuid
    ) -> Optional[Role]:
        return await self._get_with_permissions(Role.uuid == uuid)

    async def list_all(self) -> List[Role]:
        stmt = select(Role).options(
            selectinload(Role.role_permission).selectinload(RolePermission.permission)
        )
        return list((await self.session.execute(stmt)).scalars().all())

    async def set_permissions(
        self,
        role: Role,
        permission_ids: List[int]
    ) -> Role:
        await self.session.execute(
            RolePermission.__table__.delete().where(RolePermission.role_id == role.id)
        )
        for pid in permission_ids:
            self.session.add(
                RolePermission(
                    role_id = role.id, permission_id= pid
                )
            )
        await self.session.commit()
        return await self._get_with_permissions(role.id)


