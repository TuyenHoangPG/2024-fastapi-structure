"""Add users table

Revision ID: 1e4075ebb338
Revises: 
Create Date: 2024-06-23 13:03:50.013966

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

from src.commons.constants.enum import USER_ROLES, USER_STATUS
from src.commons.models.user_model import User
from src.commons.utils.datetime import utc_now


# revision identifiers, used by Alembic.
revision: str = "1e4075ebb338"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False, default=uuid4),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("salt", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                USER_ROLES,
                create_constraint=True,
                name="user_roles",
                length=50,
            ),
            nullable=False,
            default=USER_ROLES.USER,
        ),
        sa.Column(
            "status",
            sa.Enum(
                USER_STATUS,
                create_constraint=True,
                name="user_status",
                length=50,
            ),
            nullable=False,
            default=USER_STATUS.ACTIVE,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=True, default=utc_now
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=True, default=utc_now
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    salt, password = User.hash_password("Matkhau1@3")

    op.bulk_insert(
        user_table,
        [
            {
                "email": "admin@test.co",
                "full_name": "admin",
                "role": USER_ROLES.ADMIN,
                "password": password,
                "salt": salt,
            },
            {
                "email": "super_admin@test.co",
                "full_name": "super_admin",
                "role": USER_ROLES.SUPER_ADMIN,
                "password": password,
                "salt": salt,
            },
        ],
    )


def downgrade():
    op.drop_table("users")

    user_status = postgresql.ENUM("ACTIVE", "INACTIVE", name="user_status")
    user_status.drop(op.get_bind())

    user_role = postgresql.ENUM(
        "SUPER_ADMIN",
        "ADMIN",
        "USER",
        name="user_roles",
    )
    user_role.drop(op.get_bind())
