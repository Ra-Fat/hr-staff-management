from typing import Any, List, Optional
 
from sqlalchemy import select
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
 
from app.core.enum import UserStatus
from app.models.auth_account import AuthAccount
from app.models.account_role import AccountRole
from app.repositories.Base.base_repository import BaseRepository


class AdminUserRepository(BaseRepository[AuthAccount]):
    model = AuthAccount
 
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_email(self, email: str) -> Optional[AuthAccount]:
        """Login lookup. Kept separate from get_by_uuid since credentials are
        always presented as an email, never as the public uuid."""
        result = await self.session.execute(
            select(AuthAccount).where(AuthAccount.email == email)
        )
        return result.scalars().first()

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None


    def build_filters(
        self,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs: Any,
    ) -> List[ColumnElement]:
        filters: List[ColumnElement] = []
        if email is not None:
            filters.append(AuthAccount.email.ilike(f"%{email}%"))
        if full_name is not None:
            filters.append(AuthAccount.full_name.ilike(f"%{full_name}%"))
        if status is not None:
            filters.append(AuthAccount.status == UserStatus(status))
        return filters
 
    def default_order_by(self) -> List[ColumnElement]:
        return [AuthAccount.id]