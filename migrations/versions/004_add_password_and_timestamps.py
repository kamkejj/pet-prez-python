"""Add password and timestamps

Revision ID: 004
Revises: 003
Create Date: 2025-03-11

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Add password column to users table
    op.add_column('users', sa.Column('password', sa.String(255), nullable=True))

    # Set default password for existing users (should be changed after migration)
    op.execute("UPDATE users SET password = 'changeme' WHERE password IS NULL")

    # Make password column not nullable after setting defaults
    op.alter_column('users', 'password', nullable=False)

    # Add timestamps
    op.add_column('users', sa.Column('created_at', sa.DateTime, nullable=True,
                                     server_default=sa.text('NOW()')))
    op.add_column('slogans', sa.Column('created_at', sa.DateTime, nullable=True,
                                       server_default=sa.text('NOW()')))


def downgrade():
    # Drop timestamp columns
    op.drop_column('slogans', 'created_at')
    op.drop_column('users', 'created_at')

    # Drop password column
    op.drop_column('users', 'password')