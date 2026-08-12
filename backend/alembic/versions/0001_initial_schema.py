"""initial schema"""
import sqlalchemy as sa

from alembic import op

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users', sa.Column('id', sa.String(), primary_key=True), sa.Column('email', sa.String(), nullable=False), sa.Column('password_hash', sa.String(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint('email'))
    op.create_index('ix_users_email','users',['email'])
    op.create_table('sessions', sa.Column('id', sa.String(), primary_key=True), sa.Column('user_id', sa.String(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False), sa.Column('token_hash', sa.String(), nullable=False, unique=True), sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))
    op.create_index('ix_sessions_token_hash','sessions',['token_hash']); op.create_index('ix_sessions_user_id','sessions',['user_id']); op.create_index('ix_sessions_expires_at','sessions',['expires_at'])
    op.create_table('files', sa.Column('id', sa.String(), primary_key=True), sa.Column('owner_id', sa.String(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False), sa.Column('original_filename', sa.String(), nullable=False), sa.Column('storage_filename', sa.String(), nullable=False, unique=True), sa.Column('storage_path', sa.String(), nullable=False), sa.Column('mime_type', sa.String(), nullable=False), sa.Column('detected_file_type', sa.String(), nullable=False), sa.Column('size_bytes', sa.Integer(), nullable=False), sa.Column('visibility', sa.String(), nullable=False), sa.Column('checksum', sa.String(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("visibility in ('private','public')"), sa.CheckConstraint('size_bytes >= 0'))
    op.create_index('ix_files_owner_id','files',['owner_id']); op.create_index('ix_files_owner_visibility','files',['owner_id','visibility']); op.create_index('ix_files_owner_created_at','files',['owner_id','created_at']); op.create_index('ix_files_checksum','files',['checksum'])
    op.create_table('share_links', sa.Column('id', sa.String(), primary_key=True), sa.Column('file_id', sa.String(), sa.ForeignKey('files.id', ondelete='CASCADE'), nullable=False), sa.Column('token_hash', sa.String(), nullable=False, unique=True), sa.Column('created_at', sa.DateTime(timezone=True), nullable=False), sa.Column('expires_at', sa.DateTime(timezone=True)), sa.Column('revoked_at', sa.DateTime(timezone=True)))
    op.create_index('ix_share_links_file_id','share_links',['file_id']); op.create_index('ix_share_links_token_hash','share_links',['token_hash']); op.create_index('ix_share_links_active','share_links',['file_id','revoked_at','expires_at'])
    op.create_table('rate_limit_events', sa.Column('id', sa.String(), primary_key=True), sa.Column('key', sa.String(), nullable=False), sa.Column('action', sa.String(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))
    op.create_index('ix_rate_limit_key_action_created','rate_limit_events',['key','action','created_at'])

def downgrade():
    op.drop_table('rate_limit_events'); op.drop_table('share_links'); op.drop_table('files'); op.drop_table('sessions'); op.drop_table('users')
