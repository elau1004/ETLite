"""Create Table Data Set

Revision ID: 7a670e1241eb
Revises: 444326c53f71
Create Date: 2020-02-15 15:40:43.684121
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '7a670e1241eb'
down_revision = '444326c53f71'
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
        'Data_Set'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Code'               ,sa.String(8)   ,nullable=False )
        ,sa.Column('Description'        ,sa.String(64)  ,nullable=False )
        ,sa.Column('Status_ID'          ,sa.SmallInteger,nullable=False ,server_default='2')    # Enabled
        ,sa.Column('Parent_ID'          ,sa.SmallInteger,nullable=True  )
        ,sa.Column('Exec_Sequence'      ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('Data_Vendor_ID'     ,sa.SmallInteger,nullable=False )
        ,sa.Column('Run_Frequency_ID'   ,sa.SmallInteger,nullable=False ,server_default='3' )   # Daily
        ,sa.Column('Run_Frequency_Value',sa.Integer     ,nullable=False ,server_default='1' )
        ,sa.Column('Data_From'          ,sa.DateTime(timezone=True)     )
        ,sa.Column('Data_Upto'          ,sa.DateTime(timezone=True)     )
        ,sa.Column('Last_Ran_On'        ,sa.DateTime(timezone=True)     )
        ,sa.Column('Work_in_Progress'   ,sa.SmallInteger,nullable=False ,server_default='1' )
#       ,sa.Column('Work_in_Progress'   ,??             ,nullable=False )
        ,sa.Column('Lock_Expire_After'  ,sa.SmallInteger,nullable=False ,server_default='120' ) # 2 hours.
        ,sa.Column('Source_URI'         ,sa.String(128) ,nullable=True  )
        ,sa.Column('Stage_URI'          ,sa.String(128) ,nullable=True  )
        ,sa.Column('Stage_View'         ,sa.String(64)  ,nullable=True  )
        ,sa.Column('Target_URI'         ,sa.String(128) ,nullable=True  )
        ,sa.Column('Next_Run_No'        ,sa.Integer     ,nullable=False ,server_default='101' )
        ,sa.Column('Profiled_to_Run_No' ,sa.Integer     ,nullable=True  )
        ,sa.Column('Verified_to_Run_No' ,sa.Integer     ,nullable=True  )
        ,sa.Column('Average_Duration'   ,sa.Integer     ,nullable=True  )
        ,sa.Column('OnError_Contact'    ,sa.String(128) ,nullable=True  )
        ,sa.Column('OnSuccess_Contact'  ,sa.String(128) ,nullable=True  )
        ,sa.Column('Remark'             ,sa.String      ,nullable=True  )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 32767'           ,name='ID')
        ,sa.CheckConstraint( 'Status_ID BETWEEN 1 AND 2'        ,name='Status_ID'  )
        ,sa.CheckConstraint( 'Exec_Sequence BETWEEN 1 AND 255'  ,name='Exec_Sequence')
        ,sa.CheckConstraint( 'Length( Code ) <= 8'              ,name='Code')
        ,sa.CheckConstraint( 'Lock_Expire_After > 0'            ,name='Lock_Expire_After')
        ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID']  )
        ,sa.ForeignKeyConstraint(['Parent_ID']  ,['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Data_Vendor_ID']   ,['Data_Vendor.ID'] ,ondelete='CASCADE')
        ,sa.ForeignKeyConstraint(['Run_Frequency_ID'] ,['Frequency.ID'])
        #
        ,sa.Index('Data_Set_UK1' ,'Code'    ,unique=True)
        #
        ,sqlite_autoincrement=True
    )

def downgrade():
    op.drop_table('Data_Set')
