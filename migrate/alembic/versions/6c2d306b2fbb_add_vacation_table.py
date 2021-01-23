"""add vacation table

Revision ID: 6c2d306b2fbb
Revises: ead049362c51
Create Date: 2021-01-23 18:12:48.815233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c2d306b2fbb'
down_revision = 'ead049362c51'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vacation',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('vacationcategory', sa.String, nullable=False),
        sa.Column('startdate', sa.Date,nullable=False),
        sa.Column('startdateMorning', sa.Boolean,nullable=False),
        sa.Column('enddate', sa.Date,nullable=False),
        sa.Column('enddateMorning', sa.Boolean,nullable=False),
        sa.Column('reason', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('vacation')
