"""empty message

Revision ID: 482f385dd1ee
Revises: 342b7a05b923
Create Date: 2023-10-27 12:46:04.648090

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "482f385dd1ee"
down_revision = "342b7a05b923"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "scoring_system",
        sa.Column("round_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "scoring_system",
            postgresql.ENUM(
                "OneToFive", "ZeroToThree", name="scoring_system_enum"
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("round_id", name=op.f("pk_scoring_system")),
    )

    op.bulk_insert(
        sa.Table(
            "scoring_system",
            sa.MetaData(),
            sa.Column("round_id", sa.String(), nullable=False),
            sa.Column("scoring_system", sa.String(length=255), nullable=False),
        ),
        [
            {
                "round_id": "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762",
                "scoring_system": "OneToFive",
            },
            {
                "round_id": "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7",
                "scoring_system": "OneToFive",
            },
            {
                "round_id": "888aae3d-7e2c-4523-b9c1-95952b3d1644",
                "scoring_system": "OneToFive",
            },
            {
                "round_id": "0059aad4-5eb5-11ee-8c99-0242ac120002",
                "scoring_system": "OneToFive",
            },
            {
                "round_id": "fc7aa604-989e-4364-98a7-d1234271435a",
                "scoring_system": "OneToFive",
            },
            {
                "round_id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
                "scoring_system": "OneToFive",
            },
            {
                "round_id": "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
                "scoring_system": "OneToFive",
            },
        ],
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("scoring_system")
    op.execute("DROP TYPE scoring_system_enum;")
    # ### end Alembic commands ###
