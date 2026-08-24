from typing import Optional

from sqlalchemy import or_, select
from app.core.enum import UserStatus, StatusCode
from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.core.responses import app_success
from app.core.lib.translate import get_translation
# from app.repositories.admin import AdminUserRepository
from app.services.base.base_service import BaseService
# from app.repositories.adminUserRepository import 
from app.repositories.admin_user_repository import AdminUserRepository

class AdminUserService(BaseService[AdminUserRepository]):
    def __init__(
        self,
        repository: AdminUserRepository,
    ) -> None:
        super().__init__(repository)


