"""Extended suggestion field

Revision ID: a508d833e981
Revises: be6cecacef38
Create Date: 2018-09-07 13:30:11.417623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a508d833e981'
down_revision = 'be6cecacef38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # ### end Alembic commands ###

    op.alter_column('ConsultingServicesTouchPoint', 'q6',
                    existing_type=sa.String(length=255),
                    type_=sa.String(length=3000))

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # ### end Alembic commands ###

    op.alter_column('ConsultingServicesTouchPoint', 'q6',
                    existing_type=sa.String(length=3000),
                    type_=sa.String(length=255))
