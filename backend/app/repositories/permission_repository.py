from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.role.model import Permission
from app.repositories.Base.base_repository import BaseRepository


class PermissionRepository(BaseRepository[Permission]):    
    model_class = Permission

    def __int__(self, session: AsyncSession) -> None:
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