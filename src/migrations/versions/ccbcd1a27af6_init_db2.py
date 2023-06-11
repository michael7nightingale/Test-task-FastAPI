"""Init db2

Revision ID: ccbcd1a27af6
Revises: 
Create Date: 2023-06-11 12:19:53.553407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccbcd1a27af6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
            sa.Column('id', sa.String(length=100), nullable=False),
            sa.Column('username', sa.String(length=40), nullable=True),
            sa.Column('first_name', sa.String(length=40), nullable=True),
            sa.Column('last_name', sa.String(length=40), nullable=True),
            sa.Column('email', sa.String(length=50), nullable=True),
            sa.Column('password', sa.String(length=200), nullable=True),
            sa.Column('last_login', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('date_join', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('is_superuser', sa.Boolean(), nullable=True),
            sa.Column('is_staff', sa.Boolean(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username')
    )
    op.create_table('employees',
            sa.Column('id', sa.String(length=100), nullable=False),
            sa.Column('user_id', sa.String(), nullable=True),
            sa.Column('salary', sa.Integer(), nullable=True),
            sa.Column('promotion_date', sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employees')
    op.drop_table('users')
    # ### end Alembic commands ###
