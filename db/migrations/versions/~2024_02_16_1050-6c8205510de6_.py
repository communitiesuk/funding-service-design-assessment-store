"""Empty message.

Revision ID: 6c8205510de6
Revises: 3d9f0c0345ae
Create Date: 2024-02-16 10:50:21.677064

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6c8205510de6"
down_revision = "3d9f0c0345ae"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    insert_query = sa.text(
        "INSERT INTO assessment_round(round_id, scoring_system)VALUES (:uuid, :scoring_system) RETURNING round_id;"
    )

    params = {
        "uuid": "33726b63-efce-4749-b149-20351346c76e",
        "scoring_system": "OneToFive",
    }
    connection.execute(insert_query, params)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    delete_query = sa.text("DELETE FROM assessment_round WHERE round_id = :uuid;")
    params = {
        "uuid": "33726b63-efce-4749-b149-20351346c76e",
    }
    connection.execute(delete_query, params)
    # ### end Alembic commands ###
