"""add timesheeteventcategory table

Revision ID: 3a0fddcfb6bd
Revises: c64d2a66c558
Create Date: 2021-01-23 20:04:53.431940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a0fddcfb6bd'
down_revision = 'c64d2a66c558'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'timesheeteventcategory',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('eventcategoryname', sa.String, nullable=False),
        sa.Column('createdate', sa.Date, nullable=False),
    )


def downgrade():
    pass
