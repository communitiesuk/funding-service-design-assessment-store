"""Empty message.

Revision ID: 99ad87a4f888
Revises: 78d40ab26730
Create Date: 2023-01-06 13:22:23.467188

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "99ad87a4f888"
down_revision = "78d40ab26730"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "location_json_blob",
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=True,
            )
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_column("location_json_blob")

    # ### end Alembic commands ###
