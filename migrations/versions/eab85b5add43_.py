"""empty message

Revision ID: eab85b5add43
Revises: 91b8882f4cf8
Create Date: 2023-01-02 18:00:57.381309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eab85b5add43'
down_revision = '91b8882f4cf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('universities', 'phone_num',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('universities', 'phone_num',
               existing_type=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###
