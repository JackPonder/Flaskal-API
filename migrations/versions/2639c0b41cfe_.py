"""empty message

Revision ID: 2639c0b41cfe
Revises: 
Create Date: 2022-07-04 22:33:58.559945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2639c0b41cfe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('poll_options', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=128),
               existing_nullable=True)

    with op.batch_alter_table('polls', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('polls', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)

    with op.batch_alter_table('poll_options', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)

    # ### end Alembic commands ###
