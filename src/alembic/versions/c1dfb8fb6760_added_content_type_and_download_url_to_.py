"""Added Content-Type and download_url to image table

Revision ID: c1dfb8fb6760
Revises: fc5ee0979713
Create Date: 2023-02-23 17:26:03.358106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c1dfb8fb6760"
down_revision = "fc5ee0979713"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("images", sa.Column("content_type", sa.String(), nullable=True))
    op.add_column("images", sa.Column("download_url", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("images", "download_url")
    op.drop_column("images", "content_type")
    # ### end Alembic commands ###
