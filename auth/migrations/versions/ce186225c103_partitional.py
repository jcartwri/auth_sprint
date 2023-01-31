"""partitional

Revision ID: ce186225c103
Revises: e7565649e1d9
Create Date: 2022-11-18 20:05:29.020597

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ce186225c103'
down_revision = 'e7565649e1d9'
branch_labels = None
depends_on = None


def downgrade():
    op.drop_table('history_tablet')
    op.drop_table('history_mobile')
    op.drop_table('history_web')
    op.drop_table('history_bot')
    op.drop_table('history_test')


def upgrade():
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_tablet" PARTITION OF "history" FOR VALUES IN ('tablet')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('web')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_bot" PARTITION OF "history" FOR VALUES IN ('bot')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_test" PARTITION OF "history" FOR VALUES IN ('test')"""
    )
