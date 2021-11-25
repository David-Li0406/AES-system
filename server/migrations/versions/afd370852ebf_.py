"""empty message

Revision ID: afd370852ebf
Revises: 
Create Date: 2020-07-15 21:12:48.067787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afd370852ebf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('verification_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('effective_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_verification_codes_email'), 'verification_codes', ['email'], unique=True)
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commit_time', sa.DateTime(), nullable=False),
    sa.Column('article_title', sa.String(length=100), nullable=False),
    sa.Column('article_content', sa.Text(), nullable=False),
    sa.Column('total_score', sa.Float(), nullable=False),
    sa.Column('vocabulary_level', sa.Float(), nullable=False),
    sa.Column('title_relativity', sa.Float(), nullable=False),
    sa.Column('incorrect_score', sa.Float(), nullable=False),
    sa.Column('sentence_difficulty', sa.Float(), nullable=False),
    sa.Column('article_comment', sa.Text(), nullable=True),
    sa.Column('suggestion', sa.Text(), nullable=True),
    sa.Column('hsk1', sa.Integer(), nullable=False),
    sa.Column('hsk2', sa.Integer(), nullable=False),
    sa.Column('hsk3', sa.Integer(), nullable=False),
    sa.Column('hsk4', sa.Integer(), nullable=False),
    sa.Column('hsk5', sa.Integer(), nullable=False),
    sa.Column('hsk6', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_records_commit_time'), 'records', ['commit_time'], unique=False)
    op.create_table('wrongchars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('origin_text', sa.String(length=20), nullable=False),
    sa.Column('origin_text_html', sa.String(length=300), nullable=False),
    sa.Column('correct_text', sa.String(length=20), nullable=False),
    sa.Column('correct_text_html', sa.String(length=300), nullable=False),
    sa.Column('origin_start_index', sa.String(length=80), nullable=True),
    sa.Column('origin_end_index', sa.String(length=80), nullable=True),
    sa.Column('correct_start_index', sa.String(length=80), nullable=True),
    sa.Column('correct_end_index', sa.String(length=80), nullable=True),
    sa.Column('create_time', sa.String(length=50), nullable=False),
    sa.Column('update_time', sa.String(length=50), nullable=False),
    sa.Column('problem_type_zh', sa.String(length=50), nullable=False),
    sa.Column('problem_type_en', sa.String(length=50), nullable=False),
    sa.Column('paragraph_index', sa.String(length=30), nullable=False),
    sa.Column('sentence_index', sa.String(length=30), nullable=False),
    sa.Column('problem_status', sa.Integer(), nullable=False),
    sa.Column('corpus_id', sa.Integer(), nullable=False),
    sa.Column('token_array', sa.String(length=50), nullable=True),
    sa.Column('token_str', sa.String(length=200), nullable=False),
    sa.Column('token_strs', sa.String(length=500), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['record_id'], ['records.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wrongchars_corpus_id'), 'wrongchars', ['corpus_id'], unique=False)
    op.create_index(op.f('ix_wrongchars_correct_end_index'), 'wrongchars', ['correct_end_index'], unique=False)
    op.create_index(op.f('ix_wrongchars_correct_start_index'), 'wrongchars', ['correct_start_index'], unique=False)
    op.create_index(op.f('ix_wrongchars_correct_text'), 'wrongchars', ['correct_text'], unique=False)
    op.create_index(op.f('ix_wrongchars_correct_text_html'), 'wrongchars', ['correct_text_html'], unique=False)
    op.create_index(op.f('ix_wrongchars_create_time'), 'wrongchars', ['create_time'], unique=False)
    op.create_index(op.f('ix_wrongchars_origin_end_index'), 'wrongchars', ['origin_end_index'], unique=False)
    op.create_index(op.f('ix_wrongchars_origin_start_index'), 'wrongchars', ['origin_start_index'], unique=False)
    op.create_index(op.f('ix_wrongchars_origin_text'), 'wrongchars', ['origin_text'], unique=False)
    op.create_index(op.f('ix_wrongchars_origin_text_html'), 'wrongchars', ['origin_text_html'], unique=False)
    op.create_index(op.f('ix_wrongchars_paragraph_index'), 'wrongchars', ['paragraph_index'], unique=False)
    op.create_index(op.f('ix_wrongchars_problem_status'), 'wrongchars', ['problem_status'], unique=False)
    op.create_index(op.f('ix_wrongchars_problem_type_en'), 'wrongchars', ['problem_type_en'], unique=False)
    op.create_index(op.f('ix_wrongchars_problem_type_zh'), 'wrongchars', ['problem_type_zh'], unique=False)
    op.create_index(op.f('ix_wrongchars_sentence_index'), 'wrongchars', ['sentence_index'], unique=False)
    op.create_index(op.f('ix_wrongchars_token_array'), 'wrongchars', ['token_array'], unique=False)
    op.create_index(op.f('ix_wrongchars_token_str'), 'wrongchars', ['token_str'], unique=False)
    op.create_index(op.f('ix_wrongchars_token_strs'), 'wrongchars', ['token_strs'], unique=False)
    op.create_index(op.f('ix_wrongchars_update_time'), 'wrongchars', ['update_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wrongchars_update_time'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_token_strs'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_token_str'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_token_array'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_sentence_index'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_problem_type_zh'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_problem_type_en'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_problem_status'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_paragraph_index'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_origin_text_html'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_origin_text'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_origin_start_index'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_origin_end_index'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_create_time'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_correct_text_html'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_correct_text'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_correct_start_index'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_correct_end_index'), table_name='wrongchars')
    op.drop_index(op.f('ix_wrongchars_corpus_id'), table_name='wrongchars')
    op.drop_table('wrongchars')
    op.drop_index(op.f('ix_records_commit_time'), table_name='records')
    op.drop_table('records')
    op.drop_index(op.f('ix_verification_codes_email'), table_name='verification_codes')
    op.drop_table('verification_codes')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###