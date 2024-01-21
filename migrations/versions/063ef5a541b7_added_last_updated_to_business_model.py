"""added last_updated to Business model

Revision ID: 063ef5a541b7
Revises: 00cb12d384d0
Create Date: 2023-12-02 15:16:08.900267

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '063ef5a541b7'
down_revision = '00cb12d384d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new_business_submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_business_id', sa.Integer(), nullable=True),
    sa.Column('submission_type', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('address1', sa.String(length=255), nullable=False),
    sa.Column('address2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('zip', sa.String(length=20), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('instagram', sa.String(length=100), nullable=True),
    sa.Column('facebook', sa.String(length=100), nullable=True),
    sa.Column('x', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('offers_mugs', sa.Boolean(), nullable=True),
    sa.Column('accepts_personal_mug', sa.Boolean(), nullable=True),
    sa.Column('wifi', sa.Boolean(), nullable=True),
    sa.Column('sufficient_outlets', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('submitter_name', sa.String(length=255), nullable=False),
    sa.Column('submitter_email', sa.String(length=100), nullable=False),
    sa.Column('message_to_admin', sa.Text(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('update_business_submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_business_id', sa.Integer(), nullable=True),
    sa.Column('submission_type', sa.String(length=10), nullable=True),
    sa.Column('submission_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('address1', sa.String(length=255), nullable=True),
    sa.Column('address2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('zip', sa.String(length=20), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('instagram', sa.String(length=100), nullable=True),
    sa.Column('facebook', sa.String(length=100), nullable=True),
    sa.Column('x', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('offers_mugs', sa.Boolean(), nullable=True),
    sa.Column('accepts_personal_mug', sa.Boolean(), nullable=True),
    sa.Column('wifi', sa.Boolean(), nullable=True),
    sa.Column('sufficient_outlets', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('submitter_name', sa.String(length=255), nullable=False),
    sa.Column('submitter_email', sa.String(length=100), nullable=False),
    sa.Column('message_to_admin', sa.Text(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('business', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.DateTime(), nullable=True))
        batch_op.drop_column('work_friendly')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('business', schema=None) as batch_op:
        batch_op.add_column(sa.Column('work_friendly', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_column('last_updated')

    op.drop_table('update_business_submission')
    op.drop_table('new_business_submission')
    # ### end Alembic commands ###