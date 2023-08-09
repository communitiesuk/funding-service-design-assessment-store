"""empty message

Revision ID: 222a1c3b6321
Revises: 55dcd4abf66a
Create Date: 2023-08-08 11:13:18.177809

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "222a1c3b6321"
down_revision = "55dcd4abf66a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("flags")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table(
        "flags",
        sa.Column(
            "flag_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "justification", sa.TEXT(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "flag_type",
            postgresql.ENUM(
                "FLAGGED",
                "STOPPED",
                "QA_COMPLETED",
                "RESOLVED",
                name="flagtype",
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "application_id",
            postgresql.UUID(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "date_created",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "user_id", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "sections_to_flag",
            postgresql.ARRAY(sa.VARCHAR(length=256)),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["assessment_records.application_id"],
            name="fk_flags_application_id_assessment_records",
        ),
        sa.PrimaryKeyConstraint("flag_id", name="pk_flags"),
    )
    # ### end Alembic commands ###
