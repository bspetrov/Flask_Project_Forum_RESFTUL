"""Refining stuff

Revision ID: d9de29915e5a
Revises: e7952e39bf91
Create Date: 2022-08-16 13:23:37.895508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9de29915e5a'
down_revision = 'e7952e39bf91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('thread_comment', 'attachment',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('thread_comment', 'attachment',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)
    # ### end Alembic commands ###
