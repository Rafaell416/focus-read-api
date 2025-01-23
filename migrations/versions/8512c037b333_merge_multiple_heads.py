"""merge multiple heads

Revision ID: 8512c037b333
Revises: 4ab64b70af0a, d443aa0e27da
Create Date: 2025-01-22 21:19:38.134380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8512c037b333'
down_revision: Union[str, None] = ('4ab64b70af0a', 'd443aa0e27da')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
