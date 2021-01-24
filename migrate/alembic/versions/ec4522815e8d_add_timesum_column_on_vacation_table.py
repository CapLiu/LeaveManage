"""add timesum column on vacation table

Revision ID: ec4522815e8d
Revises: 3a0fddcfb6bd
Create Date: 2021-01-24 15:29:33.354722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec4522815e8d'
down_revision = '3a0fddcfb6bd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vacation', sa.Column('timesum', sa.String,nullable=False))
    op.add_column('vacation',sa.Column('approveuser',sa.String,nullable=False))
    op.add_column('vacation', sa.Column('approvedate', sa.Date, nullable=False))
    op.add_column('vacation', sa.Column('state', sa.String, nullable=False))


def downgrade():
    pass
