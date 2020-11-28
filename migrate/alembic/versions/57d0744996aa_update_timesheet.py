"""update timesheet

Revision ID: 57d0744996aa
Revises: 29d497afc0ac
Create Date: 2020-11-08 19:40:56.081709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57d0744996aa'
down_revision = '29d497afc0ac'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("timesheet") as batch_op:
        batch_op.drop_column('username')
        batch_op.add_column(sa.Column('username', sa.String,nullable=True))




def downgrade():
    pass
