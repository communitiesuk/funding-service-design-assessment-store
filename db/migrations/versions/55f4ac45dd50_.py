"""Empty message.

Revision ID: 55f4ac45dd50
Revises: eecdd097df78
Create Date: 2024-11-20 21:54:37.346479

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "55f4ac45dd50"
down_revision = "eecdd097df78"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("assessment_flag", schema=None) as batch_op:
        batch_op.add_column(sa.Column("field_ids", postgresql.ARRAY(sa.String(length=256)), nullable=True))
        batch_op.add_column(sa.Column("is_change_request", sa.Boolean(), nullable=True))


def downgrade():
    with op.batch_alter_table("assessment_flag", schema=None) as batch_op:
        batch_op.drop_column("is_change_request")
        batch_op.drop_column("field_ids")
