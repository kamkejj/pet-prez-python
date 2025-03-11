"""Add pet_name and pet_species columns to users table

Revision ID: 003
Revises: 002
Create Date: 2025-03-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Add pet_name and pet_species columns to users table
    op.add_column('users', sa.Column('pet_name', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('pet_species', sa.String(50), nullable=True))


def downgrade():
    # Drop pet_name and pet_species columns from users table
    op.drop_column('users', 'pet_species')
    op.drop_column('users', 'pet_name')
