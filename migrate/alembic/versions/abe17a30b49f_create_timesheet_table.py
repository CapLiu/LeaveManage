"""create timesheet table

Revision ID: abe17a30b49f
Revises: dfa3c47e18b7
Create Date: 2020-11-07 20:06:45.404144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abe17a30b49f'
down_revision = 'dfa3c47e18b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'timesheet',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('approveusername', sa.String, nullable=False),
        sa.Column('year',sa.Integer),
        sa.Column('month',sa.Integer),
        sa.Column('day1',sa.String),
        sa.Column('day2', sa.String),
        sa.Column('day3', sa.String),
        sa.Column('day4', sa.String),
        sa.Column('day5', sa.String),
        sa.Column('day6', sa.String),
        sa.Column('day7', sa.String),
        sa.Column('day8', sa.String),
        sa.Column('day9', sa.String),
        sa.Column('day10', sa.String),
        sa.Column('day11', sa.String),
        sa.Column('day12', sa.String),
        sa.Column('day13', sa.String),
        sa.Column('day14', sa.String),
        sa.Column('day15', sa.String),
        sa.Column('day16', sa.String),
        sa.Column('day17', sa.String),
        sa.Column('day18', sa.String),
        sa.Column('day19', sa.String),
        sa.Column('day20', sa.String),
        sa.Column('day21', sa.String),
        sa.Column('day22', sa.String),
        sa.Column('day23', sa.String),
        sa.Column('day24', sa.String),
        sa.Column('day25', sa.String),
        sa.Column('day26', sa.String),
        sa.Column('day27', sa.String),
        sa.Column('day28', sa.String),
        sa.Column('day29', sa.String),
        sa.Column('day30', sa.String),
        sa.Column('day31', sa.String),
        sa.Column('state', sa.String),
        sa.Column('submitdate', sa.Date),
        sa.Column('approvedate', sa.Date)
    )


def downgrade():
    pass
