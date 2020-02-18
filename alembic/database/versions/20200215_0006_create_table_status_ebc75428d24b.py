"""Create Table Status

Revision ID: ebc75428d24b
Revises: b5dfefe70528
Create Date: 2020-02-15 15:40:42.184098
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'ebc75428d24b'
down_revision = 'b5dfefe70528'
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
        'Status'
        ,sa.Column('ID'             ,sa.SmallInteger    ,nullable=False ,comment='The Primary Key'  ,primary_key=True )
        ,sa.Column('Name'           ,sa.String(32)      ,nullable=False ,comment='Name of the severity' )
        ,sa.Column('is_Active'      ,sa.Boolean(False)  ,nullable=False ,comment='Flag to enable/disable this row' ,server_default='1' )
        ,sa.Column('is_Terminal'    ,sa.Boolean(False)  ,nullable=False ,comment='Indicate terminal state that cannot be transition out of' ,server_default='0' )
        ,sa.Column('Display_Order'  ,sa.SmallInteger    ,nullable=True  ,comment='The order to displa in UI')
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 0 AND 255' ,name='ID')
        ,sa.UniqueConstraint('Name'                 ,name='Status_UK1')
        #
        ,sa.Index('Status_UK1'  ,'Name' ,unique=True)
    )

    _table = table(
        'Status'
        ,column('ID'            ,sa.SmallInteger)
        ,column('Name'          ,sa.String(32)  )
        ,column('is_Active'     ,sa.Boolean     )
        ,column('is_Terminal'   ,sa.Boolean     )
        ,column('Display_Order' ,sa.SmallInteger)

    )

    op.bulk_insert(
        _table
        ,[   {'ID': 0   ,'Name': 'Errored'      ,"is_Active": True ,"is_Terminal": True  ,"Display_Order": 0 }
            ,{'ID': 1   ,'Name': 'Disabled'     ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 1 }
            ,{'ID': 2   ,'Name': 'Enabled'      ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 2 }
            ,{'ID': 3   ,'Name': 'Pending'      ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 3 }
            ,{'ID': 4   ,'Name': 'Ready'        ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 4 }
            ,{'ID': 5   ,'Name': 'Cancelling'   ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 5 }
            ,{'ID': 6   ,'Name': 'Cancelled'    ,"is_Active": True ,"is_Terminal": True  ,"Display_Order": 6 }
            ,{'ID': 7   ,'Name': 'Completing'   ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 7 }
            ,{'ID': 8   ,'Name': 'Completed'    ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 8 }
            #  Extraction phase
            ,{'ID': 11  ,'Name': 'Authenticating',"is_Active":True ,"is_Terminal": False ,"Display_Order": 11}
            ,{'ID': 12  ,'Name': 'Authenticated',"is_Active": True ,"is_Terminal": False ,"Display_Order": 12}
            ,{'ID': 13  ,'Name': 'Requesting'   ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 13}
            ,{'ID': 14  ,'Name': 'Requested'    ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 14}
            ,{'ID': 15  ,'Name': 'Checking'     ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 15}
            ,{'ID': 16  ,'Name': 'Checked'      ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 16}
            ,{'ID': 17  ,'Name': 'Paginating'   ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 17}
            ,{'ID': 18  ,'Name': 'Paginated'    ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 18}
            ,{'ID': 19  ,'Name': 'Querying'     ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 19}
            ,{'ID': 20  ,'Name': 'Queried'      ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 20}
            ,{'ID': 21  ,'Name': 'Staging'      ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 21}
            ,{'ID': 22  ,'Name': 'Staged'       ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 22}
            ,{'ID': 23  ,'Name': 'Formatting'   ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 23}
            ,{'ID': 24  ,'Name': 'Formatted'    ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 24}
            #  Ingestion phase
            ,{'ID': 31  ,'Name': 'Importing'    ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 31}
            ,{'ID': 32  ,'Name': 'Imported'     ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 32}
            ,{'ID': 33  ,'Name': 'Profiling'    ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 33}
            ,{'ID': 34  ,'Name': 'Profiled'     ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 34}
            #  Certification phase
            ,{'ID': 41  ,'Name': 'Validating'   ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 41}
            ,{'ID': 42  ,'Name': 'Validated'    ,"is_Active": True ,"is_Terminal": True  ,"Display_Order": 42}
            ,{'ID': 43  ,'Name': 'Failing'      ,"is_Active": True ,"is_Terminal": False ,"Display_Order": 43}
            ,{'ID': 44  ,'Name': 'Failed'       ,"is_Active": True ,"is_Terminal": True  ,"Display_Order": 44}
        ,]
    )

def downgrade():
    op.drop_table('Status')
