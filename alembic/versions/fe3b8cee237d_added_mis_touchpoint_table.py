"""Added MIS Touchpoint table

Revision ID: fe3b8cee237d
Revises: 923ea26fba14
Create Date: 2018-10-10 19:59:11.188331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe3b8cee237d'
down_revision = '923ea26fba14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('MISTouchpoint',
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
    sa.Column('NKI1', sa.Integer(), nullable=True),
    sa.Column('NKI2', sa.Integer(), nullable=True),
    sa.Column('TradeKPI', sa.Integer(), nullable=True),
    sa.Column('ImprovementsText', sa.String(length=3000), nullable=True),
    sa.Column('agr_prepared', sa.DateTime(), nullable=True),
    sa.Column('agr_updated', sa.DateTime(), nullable=True),
    sa.Column('survey_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('lfdn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('MISTouchpoint')
    # ### end Alembic commands ###