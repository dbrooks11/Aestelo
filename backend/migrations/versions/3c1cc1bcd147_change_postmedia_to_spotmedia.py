"""Change postmedia to spotmedia

Revision ID: 3c1cc1bcd147
Revises: d32c7afc444f
Create Date: 2026-01-08 23:58:43.904082

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = '3c1cc1bcd147'
down_revision = 'd32c7afc444f'
branch_labels = None
depends_on = None

def upgrade():
    # This moves the table, the data, the indexes, and the foreign keys safely.
    op.rename_table('post_media', 'spot_media')

def downgrade():
    op.rename_table('spot_edmia', 'post_media')