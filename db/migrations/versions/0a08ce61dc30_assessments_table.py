"""assessments table

Revision ID: 0a08ce61dc30
Revises:
Create Date: 2022-06-09 09:52:08.808584

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "0a08ce61dc30"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assessment",
        sa.Column("id", sa.Text(length=36), nullable=False),
        sa.Column("application_id", sa.Text(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assessment_application_id"),
        "assessment",
        ["application_id"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_assessment_application_id"), table_name="assessment"
    )
    op.drop_table("assessment")
    # ### end Alembic commands ###
