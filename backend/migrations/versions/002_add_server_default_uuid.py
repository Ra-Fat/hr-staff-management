"""add server default uuid

Revision ID: 002
Revises: 001
Create Date: 2026-09-03 03:01:01.416093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLES = [
    'attendance',
    'auth_accounts',
    'auth_permissions',
    'auth_role_permission',
    'auth_roles',
    'auth_token_blacklist',
    'departments',
    'email_verifications',
    'leave_requests',
    'staff',
]


def upgrade() -> None:
    # Ensure pgcrypto is available for gen_random_uuid()
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')

    # Backfill any existing null uuid values before enforcing NOT NULL
    for table in TABLES:
        op.execute(f"UPDATE {table} SET uuid = gen_random_uuid() WHERE uuid IS NULL")

    # Add server-side default + enforce NOT NULL on every table
    for table in TABLES:
        op.alter_column(
            table, 'uuid',
            existing_type=sa.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        )


def downgrade() -> None:
    for table in reversed(TABLES):
        op.alter_column(
            table, 'uuid',
            existing_type=sa.UUID(),
            server_default=None,
            nullable=True,
        )