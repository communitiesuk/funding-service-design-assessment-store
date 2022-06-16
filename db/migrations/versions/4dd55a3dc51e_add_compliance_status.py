"""add compliance status

Revision ID: 4dd55a3dc51e
Revises: ba5e693514cd
Create Date: 2022-06-16 14:33:46.499742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dd55a3dc51e'
down_revision = 'ba5e693514cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment', sa.Column('compliance_status', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assessment', 'compliance_status')
    # ### end Alembic commands ###
