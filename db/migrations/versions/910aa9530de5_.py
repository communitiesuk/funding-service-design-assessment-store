"""Empty message.

Revision ID: 910aa9530de5
Revises:
Create Date: 2022-11-21 13:53:40.212689

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "910aa9530de5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assessment_records",
        sa.Column("application_id", postgresql.UUID(), nullable=False),
        sa.Column("short_id", sa.String(length=255), nullable=False),
        sa.Column("type_of_application", sa.String(length=255), nullable=False),
        sa.Column("project_name", sa.String(length=255), nullable=False),
        sa.Column("funding_amount_requested", sa.Float(), nullable=False),
        sa.Column("round_id", postgresql.UUID(), nullable=False),
        sa.Column("fund_id", postgresql.UUID(), nullable=False),
        sa.Column(
            "language",
            postgresql.ENUM("en", "cy", name="language"),
            nullable=True,
        ),
        sa.Column(
            "workflow_status",
            postgresql.ENUM(
                "NOT_STARTED",
                "IN_PROGRESS",
                "SUBMITTED",
                "COMPLETED",
                name="status",
            ),
            nullable=True,
        ),
        sa.Column(
            "jsonb_blob",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "application_json_md5",
            sa.TEXT(),
            sa.Computed("md5(CAST(jsonb_blob AS TEXT))", persisted=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("application_id", name=op.f("pk_assessment_records")),
    )
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.create_index(
            "ix_application_id_hash",
            ["application_id"],
            unique=False,
            postgresql_using="hash",
        )
        batch_op.create_index(
            "ix_application_jsonb",
            ["jsonb_blob"],
            unique=False,
            postgresql_ops={"jsonb_blob": "jsonb_path_ops"},
            postgresql_using="gin",
        )
        batch_op.create_index(
            "ix_application_round_fund_id",
            ["round_id", "fund_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_fund_id"),
            ["fund_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_funding_amount_requested"),
            ["funding_amount_requested"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_project_name"),
            ["project_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_round_id"),
            ["round_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_type_of_application"),
            ["type_of_application"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_workflow_status"),
            ["workflow_status"],
            unique=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_assessment_records_workflow_status"))
        batch_op.drop_index(batch_op.f("ix_assessment_records_type_of_application"))
        batch_op.drop_index(batch_op.f("ix_assessment_records_round_id"))
        batch_op.drop_index(batch_op.f("ix_assessment_records_project_name"))
        batch_op.drop_index(batch_op.f("ix_assessment_records_funding_amount_requested"))
        batch_op.drop_index(batch_op.f("ix_assessment_records_fund_id"))
        batch_op.drop_index("ix_application_round_fund_id")
        batch_op.drop_index(
            "ix_application_jsonb",
            postgresql_ops={"jsonb_blob": "jsonb_path_ops"},
            postgresql_using="gin",
        )
        batch_op.drop_index("ix_application_id_hash", postgresql_using="hash")

    op.drop_table("assessment_records")

    op.execute(
        """
    DROP TYPE status;
    """
    )

    op.execute(
        """
    DROP TYPE language;
    """
    )
    # ### end Alembic commands ###
