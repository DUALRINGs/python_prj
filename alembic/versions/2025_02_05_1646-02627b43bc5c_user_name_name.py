"""user_name ->> name

Revision ID: 02627b43bc5c
Revises: 3a9a138979ed
Create Date: 2025-02-05 16:46:14.486188

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "02627b43bc5c"
down_revision: Union[str, None] = "3a9a138979ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_accesstoken_created_at", table_name="accesstoken")
    op.drop_table("accesstoken")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accesstoken",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "token", sa.VARCHAR(length=43), autoincrement=False, nullable=False
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="accesstoken_user_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("token", name="accesstoken_pkey"),
    )
    op.create_index(
        "ix_accesstoken_created_at",
        "accesstoken",
        ["created_at"],
        unique=False,
    )
    # ### end Alembic commands ###
