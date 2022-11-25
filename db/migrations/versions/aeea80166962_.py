"""empty message

Revision ID: aeea80166962
Revises: 190bf5378715
Create Date: 2022-11-25 11:00:57.109714

"""
import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_extension import PGExtension
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "aeea80166962"
down_revision = "190bf5378715"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "asset_type", postgresql.ENUM(name="assesttype"), nullable=True
            )
        )
        batch_op.create_index(
            batch_op.f("ix_assessment_records_asset_type"),
            ["asset_type"],
            unique=False,
        )

    public_pg_trgm = PGExtension(schema="public", signature="pg_trgm")
    op.drop_entity(public_pg_trgm)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    public_pg_trgm = PGExtension(schema="public", signature="pg_trgm")
    op.create_entity(public_pg_trgm)

    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_assessment_records_asset_type"))
        batch_op.drop_column("asset_type")

    # ### end Alembic commands ###
