"""create user table

Revision ID: 0b427108a839
Revises: 
Create Date: 2020-10-07 16:45:26.729601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b427108a839'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id',sa.Integer,primary_key=True,autoincrement=True),
        sa.Column('username',sa.String,unique=True,nullable=False),
        sa.Column('password',sa.String,nullable=False),
        sa.Column('email',sa.String,unique=True,nullable=False),
        sa.Column('usergroup',sa.String,nullable=False),
        sa.Column('state',sa.String),
        sa.Column('registerdate',sa.Date),
        sa.Column('lastlogintime',sa.DateTime)
    )


def downgrade():
    op.drop_table('user')
