"""empty message

Revision ID: 8479aba91742
Revises:
Create Date: 2022-06-15 17:23:46.149898

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "8479aba91742"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assessment",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("compliance_status", sa.Text(), nullable=True),
        sa.Column("application_id", sa.Text(), nullable=True),
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
