"""empty message

Revision ID: 817e90e9bab4
Revises: 409915dc382e
Create Date: 2022-12-16 15:10:13.337229

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "817e90e9bab4"
down_revision = "409915dc382e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "comments",
        sa.Column("comment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("application_id", postgresql.UUID(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("sub_criteria_id", sa.String(), nullable=True),
        sa.Column(
            "comment_type",
            postgresql.ENUM("COMMENT", name="commenttype"),
            nullable=True,
        ),
        sa.Column("theme_index", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["assessment_records.application_id"],
            name=op.f("fk_comments_application_id_assessment_records"),
        ),
        sa.PrimaryKeyConstraint("comment_id", name=op.f("pk_comments")),
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comments")
    # ### end Alembic commands ###
