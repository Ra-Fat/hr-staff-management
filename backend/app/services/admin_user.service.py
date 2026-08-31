from typing import Optional

from sqlalchemy import or_, select
from core.enum import AdminStatus, StatusCode
from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.core.responses import app_success
from app.services.base.base_service import BaseService
from app.core.utils import generate_temp_password, hash_password
from app.domain.admin_user.schema import AdminUserSchema, AdminUserCreate, AdminUserUpdate
from app.core.lib.translate import get_translation
from app.domain.role.model import Role
from app.repositories.admin_user_repository import AdminUserRepository

class AdminUserService(BaseService[AdminUserRepository]):

    response_schema = AdminUserSchema

    def __init__(self, repository: AdminUserRepository) -> None:
        super().__init__(repository)


    async def _get_or_raise(self, uuid, not_found_msg = None):
        instance = await self.repository.get_by_uuid(uuid)
        if not instance:
            raise NotFoundError(
                not_found_msg or get_translation("admin_not_found")
            )
        return instance


    async def _validate_role(self, role_id:int) -> None:
        stmt = select(Role).where(Role.id == role_id)
        result = await self.repository.session.execute(stmt)
        if not result.scalars().first():
            raise ValidationError(get_translation("role_not_found"))


    async def filter(self, page = 1, page_size = 1, **filter_params):
        return await super().filter(
            page = page, 
            page_size = page_size,
            **filter_params
        )

    async def create(self, data: AdminUserCreate):

        if await self.repository.get_by_email(data.email):
            raise ConflictError(get_translation('email exists'))

        await self._validate_role(data.role_id)

        temp_password = data.password or generate_temp_password()

        instance = await self.repository.create(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(temp_password),
            role_id=data.role_id,
            status=AdminStatus.active,
        )

        # Re-fetch so role_obj is eagerly loaded for serialisation.
        instance = await self.repository.get_by_id(instance.id)
        payload = self.serialize(instance)

        if data.password is None:
            payload["temp_password"] = temp_password
            return app_success(code=StatusCode.CREATED, data=payload)


    async def update(self, uuid, data: AdminUserUpdate , not_found_msg = None):
        instance = await self._get_or_raise(uuid)
        if data.full_name is not None:
            instance.full_name = data.full_name
        if data.email is not None:
            conflict = await self.repository.get_by_email(data.email)
            if conflict and conflict.id != instance.id:
                raise ConflictError(get_translation("email_exists"))
            instance.email = data.email
        if data.role_id is not None:
            await self._validate_role(data.role_id)
            instance.role_id = data.role_id
        if data.password is not None:
            instance.password_hash = hash_password(data.password)

        await self.repository.save(instance)

        instance = await self.repository.get_by_id(
            instance.id, realm=self.realm, tenant_code=self.tenant_code
        )
        return app_success(data=self.serialize(instance))