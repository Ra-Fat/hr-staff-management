from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.core.auth import (
    get_current_user,
    get_current_user_id ,
    require_permission
)
from app.core.database import get_db
from app.core.enum import AdminStatus
from app.core.exceptions import AuthorizationError, NotFoundError, AuthenticationError

from app.core.security import create_access_token, create_refresh_token,  verify_access_token, verify_refresh_token
from app.core.lib.translate import get_translation
from app.core.responses import app_success
from app.core.utils import verify_password

from app.domain.admin_user.model import AdminUser
from app.domain.admin_user.schema import AdminUserSchema
from app.repositories.admin_user_repository import AdminUserRepository
from app.domain.auth.model import TokenBlacklist
from app.domain.auth.schema import(
    LoginRequest,
    RefreshRequest,
    TokenResponse,
)

from app.domain.role.model import Role, RolePermission


router = APIRouter(
    prefix= '/auth',
    tags= ['Auth'],
)


async def _load_user_with_permissions(
    db: AsyncSession,
    user_id: int
) -> Optional[AdminUser]:
    result = await db.execute(
        select(AdminUser)
        .where(AdminUser.id == user_id)
        .options(
            selectinload(AdminUser.role_obj)
            .selectinload(Role.role_permission)
            .selectinload(RolePermission.permission)
        )
    )
    return result.scalars().first()


def _extract_permissions(user: AdminUser) -> List[str]:
    if not user.role_obj:
        return []
    return [
        rp.permission.codename
        for rp in (user.role_obj.role_permission or [])
        if rp.permission
    ]

def _issue(user: AdminUser) -> TokenResponse:
    return TokenResponse(
        access_token = create_access_token(
            subject=user.id,
            role_id=user.role_id,
            role_name=user.role_obj.name if user.role_obj else None,
            permissions= _extract_permissions(user),
            full_name=user.full_name,
        ),
        refresh_token = create_refresh_token(user.id)
    )


@router.post('/login', response_model= TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession= Depends(get_db)
):
    repo = AdminUserRepository(db)

    user = await repo.get_by_email(body.email)
    if not user or not verify_password(body.password, user.password_hash):
        raise AuthenticationError('Invalid email or password')

    if user.status != AdminStatus.active:
        raise AuthenticationError(get_translation('account_disabled'))

    user.last_login = datetime.now(timezone .utc)
    await db.commit()

    user = await _load_user_with_permissions(db, user.id)
    return _issue(user)


@router.post('/refresh', response_model= TokenResponse)
async def refresh(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = verify_refresh_token(body.refresh_token)
    except JWTError:
        raise AuthenticationError(get_translation('invalid_token'))

    user = await _load_user_with_permissions(db, int(payload['sub']))
    if not user:
        raise AuthenticationError(get_translation('user_not_found'))

    if user.status != AdminStatus.active:
        raise AuthenticationError(get_translation('account_disabled'))

    return _issue(user)


@router.post('/logout', dependencies= [Depends(get_current_user)])
async def logout(
    db: AsyncSession = Depends(get_db),
    payload: Dict[str, Any] = Depends(get_current_user)
):
    jti = payload.get('jti')
    exp = payload.get('exp')
    if jti and exp:
        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        db.add(TokenBlacklist(jti= jti, expires_at= expires_at))
        await db.commit()
    return app_success(msg=get_translation('logout_success'))


@router.get('/me', dependencies= [Depends(get_current_user)])
async def me(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = await _load_user_with_permissions(db, user_id)
    if not user:
        raise NotFoundError(get_translation('user_not_found'))
    payload = AdminUserSchema.model_validate(user).model_dump(mode="json")
    return app_success(data=payload)