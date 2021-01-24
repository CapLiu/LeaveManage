"""add applydate column on vacation table

Revision ID: 84bff6dbbc63
Revises: ec4522815e8d
Create Date: 2021-01-24 15:46:33.563028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84bff6dbbc63'
down_revision = 'ec4522815e8d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vacation', sa.Column('applydate', sa.Date,nullable=False))


def downgrade():
    pass
