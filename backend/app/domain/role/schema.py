from typing import Dict, List, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PermissionSchema(BaseModel):
    # id: int
    uuid: UUID
    module: str
    group: Optional[str] = None
    name: str
    codename: str

    model_config = ConfigDict(from_attributes=True)


# class PermissionCreate(BaseModel):
#     module: str
#     name: str
#     codename: str
#     group: Optional[str] = None


# class PermissionUpdate(BaseModel):
#     module: Optional[str] = None
#     name: Optional[str] = None
#     codename: Optional[str] = None
#     group: Optional[str] = None


# class PermissionSchema(BaseModel):
#     uuid: UUID
#     module: str
#     group: Optional[str] = None
#     name: str
#     codename: str

#     model_config = ConfigDict(from_attributes=True)



class RoleSchema(BaseModel):
    id: int
    uuid: UUID
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    permissions: List[PermissionSchema] = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_permissions(cls, role) -> "RoleSchema":
        perms = [
            PermissionSchema.model_validate(rp.permission)
            for rp in (role.role_permissions or [])
            if rp.permission is not None
        ]
        return cls(
            id=role.id,
            uuid=role.uuid,
            name=role.name,
            description=role.description,
            created_at=role.created_at,
            permissions=perms,
        )


class RoleSummarySchema(BaseModel):
    id: int
    uuid: UUID
    name: str
    description: Optional[str] = None
    badge_color: str
    is_system: bool
    permission_count: int = 0
    permission_counts_by_module: Dict[str, str] = {}

    model_config = ConfigDict(from_attributes=True)

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_ids: List[int] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None