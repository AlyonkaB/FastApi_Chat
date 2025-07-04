"""add created_at to message

Revision ID: db8548f82db4
Revises: 9ba0b469a4ca
Create Date: 2025-06-26 17:03:55.546193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "db8548f82db4"
down_revision: Union[str, None] = "9ba0b469a4ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("messages", sa.Column("created_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("messages", "created_at")
    # ### end Alembic commands ###
