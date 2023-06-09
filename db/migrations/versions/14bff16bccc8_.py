"""empty message

Revision ID: 14bff16bccc8
Revises: 30d27919f1d8
Create Date: 2023-06-09 10:57:20.927960

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "14bff16bccc8"
down_revision = "30d27919f1d8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flags", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "sections_to_flag",
                postgresql.ARRAY(sa.String(length=256)),
                nullable=True,
            )
        )

    op.execute(
        "UPDATE flags SET sections_to_flag = string_to_array(section_to_flag, ',');"
    )

    with op.batch_alter_table("flags", schema=None) as batch_op:
        batch_op.drop_column("section_to_flag")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flags", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "section_to_flag",
                sa.TEXT(),
                autoincrement=False,
                nullable=True,
            )
        )

    op.execute(
        "UPDATE flags SET section_to_flag = array_to_string(sections_to_flag, ', ')"
    )

    with op.batch_alter_table("flags", schema=None) as batch_op:
        batch_op.drop_column("sections_to_flag")

    # ### end Alembic commands ###
