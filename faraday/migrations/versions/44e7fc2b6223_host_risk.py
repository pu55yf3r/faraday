"""Host risk

Revision ID: 44e7fc2b6223
Revises: 9f826327658a
Create Date: 2024-01-03 14:05:02.910346+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44e7fc2b6223'
down_revision = '9f826327658a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('host', sa.Column('risk', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('host', 'risk')
    # ### end Alembic commands ###
