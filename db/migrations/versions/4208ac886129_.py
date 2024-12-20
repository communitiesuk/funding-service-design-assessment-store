"""Empty message.

Revision ID: 4208ac886129
Revises: 817e90e9bab4
Create Date: 2022-12-21 14:20:41.094674

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4208ac886129"
down_revision = "817e90e9bab4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.add_column(sa.Column("theme_id", sa.String(), nullable=True))
        batch_op.drop_column("theme_index")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.add_column(sa.Column("theme_index", sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column("theme_id")

    # ### end Alembic commands ###
