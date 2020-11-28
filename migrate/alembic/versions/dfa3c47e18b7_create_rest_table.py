"""create rest table

Revision ID: dfa3c47e18b7
Revises: 0b427108a839
Create Date: 2020-10-07 17:19:54.053542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfa3c47e18b7'
down_revision = '0b427108a839'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'usergroup',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('groupname', sa.String, unique=True, nullable=False),
        sa.Column('createdate', sa.Date),
    )

    op.create_table(
        'groupprivilege',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('groupname', sa.String, unique=True, nullable=False),
        sa.Column('funclist', sa.String),
    )


def downgrade():
    pass
