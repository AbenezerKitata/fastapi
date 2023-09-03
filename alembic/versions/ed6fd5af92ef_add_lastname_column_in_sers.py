"""add lastname column in sers

Revision ID: ed6fd5af92ef
Revises: 0497272c0bc9
Create Date: 2023-09-03 13:22:12.009005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed6fd5af92ef'
down_revision: Union[str, None] = '0497272c0bc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lastName', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lastName')
    # ### end Alembic commands ###
