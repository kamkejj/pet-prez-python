"""Create slogans table

Revision ID: 002
Revises: 001
Create Date: 2025-03-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create slogans table
    op.create_table('slogans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('slogan', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    # Add an index on user_id for better performance
    op.create_index('idx_slogans_user_id', 'slogans', ['user_id'])


def downgrade():
    # Drop slogans table
    op.drop_index('idx_slogans_user_id', table_name='slogans')
    op.drop_table('slogans')
