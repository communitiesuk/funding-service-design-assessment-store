"""Empty message.

Revision ID: 4bdc171458b2
Revises: 6ad072a15e50
Create Date: 2023-06-30 15:53:26.608073

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "4bdc171458b2"
down_revision = "6ad072a15e50"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE flagstatus ADD VALUE 'QA_COMPLETED'")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE flagstatus RENAME TO flagstatus_old")
    op.execute("CREATE TYPE flagstatus AS ENUM ('RAISED', 'STOPPED', 'RESOLVED')")
    op.execute("ALTER TABLE flag_update ALTER COLUMN status TYPE flagstatus USING status::text::flagstatus")
    op.execute(
        "ALTER TABLE assessment_flag ALTER COLUMN latest_status TYPE flagstatus USING latest_status::text::flagstatus"
    )
    op.execute("DROP TYPE flagstatus_old")
    # ### end Alembic commands ###
