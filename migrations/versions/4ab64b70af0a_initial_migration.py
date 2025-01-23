"""initial migration

Revision ID: 4ab64b70af0a
Revises: d443aa0e27da
Create Date: 2025-01-19 17:23:36.791457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4ab64b70af0a'
down_revision: str = 'd443aa0e27da'  # Make sure this points to the previous migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Skip table creation as they were created in the previous migration
    pass


def downgrade() -> None:
    # Skip table dropping as they will be handled by the previous migration
    pass
