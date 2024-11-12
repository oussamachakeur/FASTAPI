"""create user table

Revision ID: f36c27099fc7
Revises: 5a8b272724bb
Create Date: 2024-11-11 15:50:36.614553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f36c27099fc7'
down_revision: Union[str, None] = '5a8b272724bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users' , sa.Column('id' , sa.Integer() , nullable= False , primary_key=True)
                    ,sa.Column('email' , sa.String() , nullable= False) 
                    ,sa.Column('password' , sa.String() ,nullable= False))


def downgrade() -> None:
    op.drop_table("users")