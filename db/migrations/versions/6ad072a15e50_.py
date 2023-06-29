"""empty message

Revision ID: 6ad072a15e50
Revises: 14bff16bccc8
Create Date: 2023-06-27 16:39:06.293214

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6ad072a15e50"
down_revision = "14bff16bccc8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assessment_flag",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "application_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column(
            "latest_status",
            postgresql.ENUM(
                "RAISED", "STOPPED", "RESOLVED", name="flagstatus"
            ),
            nullable=True,
        ),
        sa.Column("latest_allocation", sa.String(), nullable=True),
        sa.Column(
            "sections_to_flag",
            postgresql.ARRAY(sa.String(length=256)),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["assessment_records.application_id"],
            name=op.f("fk_assessment_flag_application_id_assessment_records"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_flag")),
    )
    op.create_table(
        "flag_update",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "assessment_flag_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("justification", sa.String(), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "RAISED", "STOPPED", "RESOLVED", name="flagstatus"
            ),
            nullable=True,
        ),
        sa.Column("allocation", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["assessment_flag_id"],
            ["assessment_flag.id"],
            name=op.f("fk_flag_update_assessment_flag_id_assessment_flag"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_flag_update")),
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("flag_update")
    op.drop_table("assessment_flag")
    sa.Enum(name="flagstatus").drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
