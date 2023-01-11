"""empty message

Revision ID: 3a22407701c8
Revises: 78d40ab26730
Create Date: 2023-01-09 16:06:23.980091

"""
from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_extension import PGExtension
from sqlalchemy import text as sql_text
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3a22407701c8'
down_revision = '78d40ab26730'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flags', schema=None) as batch_op:
        batch_op.drop_column('resolution_reason')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('flags', schema=None) as batch_op:
        batch_op.add_column(sa.Column('resolution_reason', postgresql.ENUM('QUERY_RESOLVED', 'STOP_ASSESSMENT', name='resolutiontype'), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
