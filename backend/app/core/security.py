import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from jose import JWTError, jwt
from app.core.config import settings


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(
    subject: int,
    role_id: Optional[int] = None,
    role_name: Optional[str] = None,
    permissions: Optional[List[str]] = None,
    full_name: Optional[str] = None,
) -> str:
    payload: Dict[str, Any] = {
        'sub' : str(subject),
        "jti": uuid.uuid4().hex,  # unique token ID for blacklisting
        "type": "access",
        "exp": _now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
        "iat": _now(),
    }
    if role_id is not None:
        payload['role_id'] = role_id
    if role_name is not None:
        payload["role"] = role_name
    if permissions is not None:
        payload["permissions"] = permissions
    if full_name is not None:
        payload["full_name"] = full_name
    return jwt.encode(payload, settings.JWT_SECRET , algorithm= settings.JWT_ALGORITHM)


def create_refresh_token(subject: int) -> str:
    payload = {
        "sub": str(subject),
        "type": "refresh",
        "exp": _now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": _now(),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    'Decode and verify a token'
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_SECRET]
    )


def verify_access_token(token: str) -> Dict[str, Any]:
    payload = decode_token(token)
    if payload.get('type') != 'access':
        raise JWTError("Not an access token")
    return payload


def verify_refresh_token(token: str) -> Dict[str, Any]:
    payload = decode_token(token)
    if payload.get('type') != 'refresh':
        raise JWTError("Not a refresh token")
    return payload 