"""Create Table Severity

Revision ID: b5dfefe70528
Revises: acc5ba7c6f70
Create Date: 2020-02-15 15:40:41.309085
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'b5dfefe70528'
down_revision = 'acc5ba7c6f70'
branch_labels = None
depends_on = None


dt_updated_on = sa.Column(
                    'Updated_On'
                    ,sa.DateTime(timezone=True)
                    ,nullable=False
                    ,server_default=func.current_timestamp()
                    ,comment='The audit timestamp when this row was last updated'
                )

def upgrade():
    op.create_table(
        'Severity'
        ,sa.Column('ID'         ,sa.SmallInteger,nullable=False ,comment='The Primary Key'  ,primary_key=True )
        ,sa.Column('Name'       ,sa.String(12)  ,nullable=False ,comment='Name of the severity' )
        ,sa.Column('Description',sa.String(128) ,nullable=False ,comment='Description of the severity'  )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 5'   ,name='ID')
        #
        ,sa.Index('Severity_UK1' ,'Name' ,unique=True)
    )

    _table = table(
        'Severity'
        ,column('ID'            ,sa.SmallInteger)
        ,column('Name'          ,sa.String())
        ,column('Description'   ,sa.String())
    )
 
    op.bulk_insert(
        _table
        ,[   {'ID': 1 ,'Name': 'Critical'   ,'Description': 'Functionality is affected.' }
            ,{'ID': 2 ,'Name': 'Error'      ,'Description': 'An error condition exists and functionality could be affected.' }
            ,{'ID': 3 ,'Name': 'Warning'    ,'Description': 'Functionality could be affected.' }
            ,{'ID': 4 ,'Name': 'Information','Description': 'General information about system operations.' }
            ,{'ID': 5 ,'Name': 'Debug'      ,'Description': 'Debugging trace.' }
        ,]
    )

def downgrade():
    op.drop_table('Severity')
