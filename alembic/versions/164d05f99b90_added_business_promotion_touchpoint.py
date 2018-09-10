"""Added Business Promotion touchpoint

Revision ID: 164d05f99b90
Revises: d86fc1fbafac
Create Date: 2018-09-10 21:31:50.136905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '164d05f99b90'
down_revision = 'd86fc1fbafac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('BusinessPromotionTouchpoint',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('lfdn', sa.Integer(), nullable=True),
    sa.Column('project_number', sa.Integer(), nullable=True),
    sa.Column('subproject_number', sa.String(length=15), nullable=True),
    sa.Column('client_number', sa.Integer(), nullable=True),
    sa.Column('client_name', sa.String(length=200), nullable=True),
    sa.Column('p_spec', sa.Integer(), nullable=True),
    sa.Column('assignment_type', sa.String(length=20), nullable=True),
    sa.Column('business_area', sa.String(length=50), nullable=True),
    sa.Column('project_cc', sa.Integer(), nullable=True),
    sa.Column('q1', sa.Integer(), nullable=True),
    sa.Column('q2', sa.Integer(), nullable=True),
    sa.Column('q3', sa.Integer(), nullable=True),
    sa.Column('q4', sa.Integer(), nullable=True),
    sa.Column('q5', sa.Integer(), nullable=True),
    sa.Column('q6', sa.Integer(), nullable=True),
    sa.Column('q7', sa.Integer(), nullable=True),
    sa.Column('q8', sa.String(length=3000), nullable=True),
    sa.Column('agr_prepared', sa.DateTime(), nullable=True),
    sa.Column('agr_updated', sa.DateTime(), nullable=True),
    sa.Column('survey_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('lfdn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('BusinessPromotionTouchpoint')
    # ### end Alembic commands ###