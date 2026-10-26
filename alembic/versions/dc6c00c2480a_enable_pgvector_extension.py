"""enable_pgvector_extension

Revision ID: dc6c00c2480a
Revises: 0b5dbe155921
Create Date: 2026-10-22 18:35:50.623557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc6c00c2480a'
down_revision: Union[str, Sequence[str], None] = '0b5dbe155921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS vector;")
