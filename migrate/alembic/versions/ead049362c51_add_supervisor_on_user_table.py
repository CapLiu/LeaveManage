"""add supervisor on user table

Revision ID: ead049362c51
Revises: ac252cf2f6aa
Create Date: 2020-11-10 20:47:31.458590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead049362c51'
down_revision = 'ac252cf2f6aa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('supervisor', sa.String))


def downgrade():
    pass
