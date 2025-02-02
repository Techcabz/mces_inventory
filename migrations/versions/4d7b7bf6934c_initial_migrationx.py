"""Initial migrationx

Revision ID: 4d7b7bf6934c
Revises: 088eb92c19a1
Create Date: 2025-01-31 00:46:31.988987

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4d7b7bf6934c'
down_revision = '088eb92c19a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('inventory_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'categories', ['category_id'], ['id'])
        batch_op.drop_column('parent_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('inventory_ibfk_1', 'categories', ['parent_id'], ['id'])
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###
