from typing import Dict, List, Optional
import re

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.core.responses import app_success
from app.core.lib.translate import get_translation
from app.domain.role.schema import(
    RoleCreate,
    RoleSchema,
    RoleSummarySchema,
    PermissionSchema,
    RoleUpdate
)
from app.core.permission import PERMISSION_DEFINITIONS
from app.repositories.role_repository import RoleRepository
from app.repositories.permission_repository import PermissionRepository

def _normalize(name: str) -> str:
    return re.sub(r"[\s-]+", "_", name.strip().lower())

def _build_module_totals() -> Dict[str, int]:
    """
    Builds a lookup table of permission totals, keyed by BOTH:
    - top-level category (e.g. "attendance", "leave")
    - submenu name (e.g. "admin_users", "staff", "departments")
    This handles the fact that `permission.module` in the DB is
    inconsistent about which level it stores.
    """
    totals: Dict[str, int] = {}

    for category, submenus in PERMISSION_DEFINITIONS.items():
        cat_key = _normalize(category)
        cat_total = sum(len(perms) for perms in submenus.values())
        totals[cat_key] = totals.get(cat_key, 0) + cat_total

        for submenu, perms in submenus.items():
            sub_key = _normalize(submenu)
            totals[sub_key] = totals.get(sub_key, 0) + len(perms)

    return totals

def _to_summary(role) -> RoleSummarySchema:
    counts: Dict[str, int] = {}
    for rp in role.role_permission or []:
        if rp.permission:
            mod = rp.permission.module
            counts[mod] = counts.get(mod, 0) + 1

    module_totals = _build_module_totals()

    formatted = {
        mod: f"{granted}/{module_totals.get(mod, '?')}"
        for mod, granted in counts.items()
    }
    return RoleSummarySchema(
        id=role.id,
        uuid=role.uuid,
        name=role.name,
        description=role.description,
        permission_count=len(role.role_permission or []),
        permission_counts_by_module=formatted,
    )


class RoleService:
    def __init__(self, role_repo: RoleRepository, perm_repo: PermissionRepository)-> None:
        self.role_repo = role_repo
        self.perm_repo = perm_repo

    async def _owned_or_raise(self, uuid):
        role = await self.role_repo.get_with_permission_uuid(uuid)
        if not role:
            raise ValidationError(get_translation("role_not_found"))
        return role

    async def get_role(self, uuid):
        role = await self.role_repo.get_with_permission_uuid(uuid)
        if not role:
            raise NotFoundError(get_translation("role_not_found"))
        return app_success(data=RoleSchema.from_orm_with_permissions(role))

    async def list_roles(self):
        roles = await self.role_repo.list_all()
        summaries = [_to_summary(r) for r in roles]
        return app_success(data=summaries)

    async def list_permission(self):
        perms = await self.perm_repo.list_all()
        data = [PermissionSchema.model_validate(p) for p in perms]
        return app_success(data=data)


    async def create_role(self, data: RoleCreate):
        if await self.role_repo.get_by_name(data.name):
            raise ConflictError(get_translation('role_name_exists'))
        if data.permission_ids:
            found = await self.perm_repo.get_by_ids(data.permission_ids)
            if len(found) != len(data.permission_ids):
                raise ValidationError(get_translation("invalid_permission_ids"))

        role = await self.role_repo.create(
            name = data.name,
            description=data.description,
        )
        if data.permission_ids:
            role = await self.role_repo.set_permissions(
                role, data.permission_ids
            )
        else:
            role = await self.role_repo.get_with_permissions(role.id)

        return app_success(data=RoleSchema.from_orm_with_permissions(role))


    async def update_role(self, uuid, data: RoleUpdate):
        role = await self._owned_or_raise(uuid)

        if data.name is not None and data.name != role.name:
            conflict = await self.role_repo.get_by_name(data.name)

            if conflict:
                raise ConflictError(get_translation("role_name_exists"))
            role.name = data.name
        if data.description is not None:
            role.description = data.description

        await self.role_repo.save(role)

        if data.permission_ids is not None:
            if data.permission_ids:
                found = await self.perm_repo.get_by_ids(data.permission_ids)
                if len(found) != len(data.permission_ids):
                    raise ValidationError(get_translation("invalid_permission_ids"))
            role = await self.role_repo.set_permissions(role)

        else:
            role = await self.role_repo.get_with_permissions(role.id)

        return app_success(data=RoleSchema.from_orm_with_permissions(role))


    async def delete_role(self, uuid):
        role = await self._owned_or_raise(uuid)
        await self.role_repo.delete(role)
        return app_success()
     
        