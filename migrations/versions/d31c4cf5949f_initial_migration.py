"""initial migration

Revision ID: d31c4cf5949f
Revises:
Create Date: 2026-09-17 16:33:55.331232

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# =========================================================
# REVISION IDENTIFIERS
# =========================================================

revision: str = "d31c4cf5949f"

down_revision: Union[str, Sequence[str], None] = None

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


# =========================================================
# UPGRADE
# =========================================================

def upgrade() -> None:
    """Upgrade database schema."""


    # ---------------------------------------------------------
    # USERS TABLE
    # ---------------------------------------------------------

    op.create_table(

        "users",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False
        ),

        sa.Column(
            "username",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="user"
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "username",
            name="uq_users_username"
        )
    )


    # ---------------------------------------------------------
    # EMPLOYEES TABLE
    # ---------------------------------------------------------

    op.create_table(

        "employees",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            "department",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "salary",
            sa.Float(),
            nullable=False
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "email",
            name="uq_employees_email"
        )
    )


# =========================================================
# DOWNGRADE
# =========================================================

def downgrade() -> None:
    """Downgrade database schema."""


    # ---------------------------------------------------------
    # EMPLOYEES TABLE
    # ---------------------------------------------------------

    op.drop_table(
        "employees"
    )


    # ---------------------------------------------------------
    # USERS TABLE
    # ---------------------------------------------------------

    op.drop_table(
        "users"
    )