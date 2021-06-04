"""empty message

Revision ID: b1911f24cdf9
Revises: 88c5b49a9e52
Create Date: 2021-05-14 09:01:35.729438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1911f24cdf9'
down_revision = '88c5b49a9e52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('childs', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comment', 'comment', ['childs'], ['parent_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'childs')
    # ### end Alembic commands ###
