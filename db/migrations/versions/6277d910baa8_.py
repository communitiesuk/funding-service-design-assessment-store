"""Empty message.

Revision ID: 6277d910baa8
Revises: ea9b2ccebd34
Create Date: 2023-07-12 11:09:23.553438

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "6277d910baa8"
down_revision = "ea9b2ccebd34"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.execute("ALTER TYPE flagstatus RENAME TO flagstatus_old")
    op.execute("CREATE TYPE flagstatus AS ENUM ('RAISED', 'STOPPED', 'RESOLVED')")
    op.execute("ALTER TABLE flag_update ALTER COLUMN status TYPE flagstatus USING status::text::flagstatus")
    op.execute(
        "ALTER TABLE assessment_flag ALTER COLUMN latest_status TYPE flagstatus USING latest_status::text::flagstatus"
    )
    op.execute("DROP TYPE flagstatus_old")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE flagstatus ADD VALUE 'QA_COMPLETED'")

    # ### end Alembic commands ###
