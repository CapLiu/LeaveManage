"""add vacationcategory table

Revision ID: c64d2a66c558
Revises: 6c2d306b2fbb
Create Date: 2021-01-23 19:54:39.457828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c64d2a66c558'
down_revision = '6c2d306b2fbb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('timesheetevent', sa.Column('eventcategory', sa.String))


def downgrade():
    pass
