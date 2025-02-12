"""add_setup_complete_column

Revision ID: 50f67af6ca23
Revises: d093ba44db3a
Create Date: 2025-01-04 00:41:17.961571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50f67af6ca23'
down_revision: Union[str, None] = 'd093ba44db3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('setup_state', sa.Column('setup_complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('setup_state', 'setup_complete')
    # ### end Alembic commands ###
