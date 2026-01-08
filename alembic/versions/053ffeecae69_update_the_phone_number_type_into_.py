"""update the phone number type into string to handle the leading zeros

Revision ID: 053ffeecae69
Revises: 8c5a37b0ae00
Create Date: 2026-01-08 18:04:23.629108

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "053ffeecae69"
down_revision: Union[str, Sequence[str], None] = "8c5a37b0ae00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        # We use batch_op to add the column and the constraint
        batch_op.alter_column(
            "phone_number",
            existing_type=sa.INTEGER(),
            type_=sa.String(),
            existing_nullable=True,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        # We use batch_op to add the column and the constraint
        batch_op.alter_column(
            "phone_number",
            existing_type=sa.String(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )
