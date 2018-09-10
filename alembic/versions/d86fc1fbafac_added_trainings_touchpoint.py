"""Added Trainings touchpoint

Revision ID: d86fc1fbafac
Revises: 73f4e4d302a9
Create Date: 2018-09-10 21:13:38.621270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd86fc1fbafac'
down_revision = '73f4e4d302a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TrainingsTouchpoint',
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
    sa.Column('q4', sa.String(length=3000), nullable=True),
    sa.Column('agr_prepared', sa.DateTime(), nullable=True),
    sa.Column('agr_updated', sa.DateTime(), nullable=True),
    sa.Column('survey_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('lfdn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TrainingsTouchpoint')
    # ### end Alembic commands ###
