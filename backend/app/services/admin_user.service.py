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
from app.core.lib.translate import get_translation