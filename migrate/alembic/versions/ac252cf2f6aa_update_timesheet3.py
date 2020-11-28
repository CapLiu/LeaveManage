"""update timesheet3

Revision ID: ac252cf2f6aa
Revises: 572ba5d9b261
Create Date: 2020-11-08 20:09:10.226290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac252cf2f6aa'
down_revision = '572ba5d9b261'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('timesheet', sa.Column('username', sa.String))


def downgrade():
    pass
