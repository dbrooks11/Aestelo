"""Change Post model to Spot and corresponding columns

Revision ID: d32c7afc444f
Revises: 41d3a52f90ed
Create Date: 2026-01-08 23:35:45.703773

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd32c7afc444f'
down_revision = '41d3a52f90ed'
branch_labels = None
depends_on = None


def upgrade():
    # This single line moves the table, the data, and the indexes safely.
    op.rename_table('post', 'spot')

def downgrade():
    op.rename_table('spot', 'post')