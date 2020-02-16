"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


dt_updated_on = sa.Column(
                    'Updated_On'
                    ,sa.DateTime(timezone=True)
                    ,nullable=False
                    ,server_default=func.current_timestamp()
                    ,comment='The audit timestamp when this row was last updated'
                )

def upgrade():
    # TODO: Implement your DB object creation.
    # SEE:  https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column
    # SEE:  https://alembic.sqlalchemy.org/en/latest/api/operations.html#operation-objects
    ${upgrades if upgrades else "pass"}

def downgrade():
    # TODO: Implement your DB object destruction.
    # SEE:  https://alembic.sqlalchemy.org/en/latest/api/operations.html#operation-objects
    ${downgrades if downgrades else "pass"}
