import secrets
from typing import Any, Callable, Dict, List, Optional
from fastapi import Depends , Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid import UUID
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.repositories.staff_repository import StaffRepository
from app.core.lib.translate import get_translation
from app.domain.auth.model import TokenBlacklist
from app.core.security import verify_access_token


_bearer = HTTPBearer(auto_error= False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    if credentials is None:
        raise AuthenticationError(get_translation("app_token_required"))
    try:
        payload = verify_access_token(credentials.credentials)
    except JWTError:
        raise AuthenticationError(get_translation("invalid_token"))

    # check if token has been blacklisted (logged out)
    jti = payload.get('jti')
    if jti:
        blacklisted = (
            await db.execute(select(TokenBlacklist).where(TokenBlacklist.jti == jti))
        ).scalars().first()
        if blacklisted:
            raise AuthenticationError(get_translation('invalid token'))

    return payload


async def get_current_user_id(
    payload: Dict[str, Any] = Depends(get_current_user),
) -> int:
    return int(payload['sub'])


def require_permission(codename: str) -> Callable:
    """
        Route dependency factory. Checks that the JWT payload contains the given
        permission codename. Super Admins (role == "Super Admin") bypass checks.
    
        Usage:
            @router.get("/foo", dependencies=[Depends(require_permission("tenants.view"))])
    """
    async def _check(payload: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        role_name: str = payload.get("role", '')
        if role_name == 'admin':
            return payload

        permissions: List[str] = payload.get('permissions', [])
        if codename not in permissions:
            raise AuthorizationError(get_translation("unauthorized_access"))
        return payload

    return _check


async def get_current_staff_uuid(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UUID:
    """Resolves the logged-in auth account to their linked Staff record's uuid."""
    user_id = current_user.get("sub")
    if user_id is None:
        raise AuthenticationError(get_translation("invalid_token"))

    staff_repo = StaffRepository(db)
    staff = await staff_repo.get_by_user_id(int(user_id))
    if not staff:
        raise NotFoundError(get_translation("staff_profile_not_found"))
    return staff.uuid