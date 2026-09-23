"""Initial database schema

Revision ID: 20260921_001
Revises: 
Create Date: 2026-09-21 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260921_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='creator'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_id', 'users', ['id'])

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
    )
    op.create_index('ix_tags_name', 'tags', ['name'])
    op.create_index('ix_tags_id', 'tags', ['id'])

    # Create media_assets table
    op.create_table(
        'media_assets',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('mime_type', sa.String(100), nullable=False),
        sa.Column('ocr_text', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('owner_id', sa.String(36), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_media_assets_id', 'media_assets', ['id'])

    # Create asset_tags join table
    op.create_table(
        'asset_tags',
        sa.Column('asset_id', sa.String(36), primary_key=True),
        sa.Column('tag_id', sa.String(36), primary_key=True),
        sa.ForeignKeyConstraint(['asset_id'], ['media_assets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    )

    # Create asset_comments table
    op.create_table(
        'asset_comments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('asset_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], ['media_assets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(100), nullable=False),
        sa.Column('resource_id', sa.String(36), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    )


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('asset_comments')
    op.drop_table('asset_tags')
    op.drop_table('media_assets')
    op.drop_table('tags')
    op.drop_table('users')
