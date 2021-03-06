"""empty message

Revision ID: e4090d29d2a2
Revises: aa9613df0958
Create Date: 2017-07-15 21:10:43.180000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4090d29d2a2'
down_revision = 'aa9613df0958'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(length=20), nullable=True))
    op.create_unique_constraint(None, 'user', ['password'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'password')
    # ### end Alembic commands ###
