"""Empty message.

Revision ID: 4bd13b6df99b
Revises: 5d3468e62492
Create Date: 2024-05-03 16:45:58.017724

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4bd13b6df99b"
down_revision = "5d3468e62492"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    insert_query = sa.text(
        "INSERT INTO assessment_round(round_id, scoring_system)VALUES (:uuid, :scoring_system) RETURNING round_id;"
    )

    params = {
        "uuid": "27ab26c2-e58e-4bfe-917d-64be10d16496",
        "scoring_system": "OneToFive",
    }
    connection.execute(insert_query, params)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    delete_query = sa.text("DELETE FROM assessment_round WHERE round_id = :uuid;")
    params = {
        "uuid": "27ab26c2-e58e-4bfe-917d-64be10d16496",
    }
    connection.execute(delete_query, params)
    # ### end Alembic commands ###
