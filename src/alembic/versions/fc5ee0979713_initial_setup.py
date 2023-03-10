"""initial setup

Revision ID: fc5ee0979713
Revises: 
Create Date: 2023-02-23 03:21:38.089663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fc5ee0979713"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(), nullable=False),
        sa.Column("enable_detection", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_images_id"), "images", ["id"], unique=False)
    op.create_table(
        "tags",
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "image_tag_junction",
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.Column("tag_name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["image_id"],
            ["images.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_name"],
            ["tags.name"],
        ),
        sa.PrimaryKeyConstraint("image_id", "tag_name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("image_tag_junction")
    op.drop_table("tags")
    op.drop_index(op.f("ix_images_id"), table_name="images")
    op.drop_table("images")
    # ### end Alembic commands ###
