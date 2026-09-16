import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.database import Base
from dotenv import load_dotenv
from app.domain.admin_user.model import AdminUser
from app.domain.attendance.model import Attendance
from app.domain.auth.model import EmailVerification, TokenBlacklist
from app.domain.department.model import Department
from app.domain.leave_request.model import LeaveRequest
from app.domain.role.model import Role, RolePermission, Permission
from app.domain.position.model import Position
from app.domain.staff.model import Staff
from app.domain.attendance.model import Attendance
from pathlib import Path

load_dotenv()

def process_revision_directives(context, revision, directives):
    """Auto-generate sequential revision IDs: 001, 002, 003..."""
    script = directives[0]
    versions_path = Path(config.get_main_option("script_location")) / "versions"

    existing = [
        f.stem.split("_")[0] for f in versions_path.glob("*.py")
        if f.stem[:3].isdigit()
    ]

    next_num = max([int(n) for n in existing], default=0) + 1
    script.rev_id = f"{next_num:03d}"


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if db_url:= os.environ.get("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata


VERSION_TABLE = 'alembic_version'


# ------------------------------------------------------------
# 4. Offline migration (generates SQL without connecting)
# ------------------------------------------------------------

def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table=VERSION_TABLE,
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------
# 5. Online migration (async)
# ------------------------------------------------------------
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection = connection,
        target_metadata= target_metadata,
        version_table=VERSION_TABLE,
        process_revision_directives=process_revision_directives, 
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


# ------------------------------------------------------------
# 6. Decide mode
# ------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()