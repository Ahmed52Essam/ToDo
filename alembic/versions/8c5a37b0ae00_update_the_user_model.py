"""update the user model

Revision ID: 8c5a37b0ae00
Revises: 4feea4d11a66
Create Date: 2026-01-08 17:17:06.471062

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8c5a37b0ae00"
down_revision: Union[str, Sequence[str], None] = "4feea4d11a66"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # We open a batch operation on the 'users' table
    with op.batch_alter_table("users", schema=None) as batch_op:
        # We use batch_op to add the column and the constraint
        batch_op.add_column(sa.Column("phone_number", sa.Integer(), nullable=True))
        batch_op.create_unique_constraint("uq_users_phone", ["phone_number"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        # Drop the constraint using the specific name we gave it
        batch_op.drop_constraint("uq_users_phone", type_="unique")
        # Drop the column (no need to specify the table name 'users' here)
        batch_op.drop_column("phone_number")
