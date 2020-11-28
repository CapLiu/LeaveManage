"""update timesheet2

Revision ID: 572ba5d9b261
Revises: 57d0744996aa
Create Date: 2020-11-08 20:08:03.387506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '572ba5d9b261'
down_revision = '57d0744996aa'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("timesheet") as batch_op:
        batch_op.drop_column('username')


def downgrade():
    pass
