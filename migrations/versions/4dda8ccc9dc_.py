"""empty message

Revision ID: 4dda8ccc9dc
Revises: None
Create Date: 2015-02-18 15:07:28.372334

"""

# revision identifiers, used by Alembic.
revision = '4dda8ccc9dc'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=255), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    ### end Alembic commands ###
