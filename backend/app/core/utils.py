import uuid
import secrets
import bcrypt

from cryptography.fernet import Fernet
from app.core.config import settings

_fernet = Fernet(settings.FERNET_KEY.encode())


def generate_temp_password(length: int = 16) -> str:
    """A URL-safe random password for admin accounts created without one."""
    return secrets.token_urlsafe(length)

def encrypt_data(plan_text: str) -> str:
    return _fernet.encrypt(plan_text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    return _fernet.decrypt(encrypted_text.encode()).decode()

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()