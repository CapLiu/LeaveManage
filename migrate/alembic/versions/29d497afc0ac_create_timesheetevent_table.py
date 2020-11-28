"""create timesheetevent table

Revision ID: 29d497afc0ac
Revises: abe17a30b49f
Create Date: 2020-11-08 15:45:13.729122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d497afc0ac'
down_revision = 'abe17a30b49f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'timesheetevent',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('eventcode', sa.String, unique=True, nullable=False),
        sa.Column('nickname', sa.String, unique=True,nullable=False),
    )


def downgrade():
    pass
