"""Create Table Job Run

Revision ID: 387bcafcfbb3
Revises: 7a670e1241eb
Create Date: 2020-02-15 15:40:44.429133
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '387bcafcfbb3'
down_revision = '7a670e1241eb'
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
        'Job_Run'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Run_No'             ,sa.Integer     ,nullable=False )
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False )
        ,sa.Column('Status_ID'          ,sa.SmallInteger,nullable=False )
        ,sa.Column('Data_From'          ,sa.DateTime(    timezone=True ))
        ,sa.Column('Data_Upto'          ,sa.DateTime(    timezone=True ))
        ,sa.Column('Ran_From'           ,sa.DateTime(    timezone=True ))
        ,sa.Column('Ran_Upto'           ,sa.DateTime(    timezone=True ))
        ,sa.Column('Total_Count'        ,sa.Integer     )
        ,sa.Column('Extra_Count_'       ,sa.Integer     )
        ,sa.Column('Unique_Count'       ,sa.Integer     )
        ,sa.Column('Ingest_Count'       ,sa.Integer     )
        ,sa.Column('Error_Count'        ,sa.Integer     )
        ,sa.Column('Files_Count'        ,sa.SmallInteger)
        ,sa.Column('Remark'             ,sa.String      )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 32767'   ,name='ID'  )
        #
        ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID']  )
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'] ,ondelete='CASCADE')
        #
        ,sa.Index('Job_Run_UK1' ,'Run_No'       ,'Data_Set_ID'              ,unique=True)
        ,sa.Index('Job_Run_UK2' ,'Data_Set_ID'  ,'Run_No'                   ,unique=True)
        ,sa.Index('Job_Run_UK3' ,'Status_ID'    ,'Data_Set_ID'  ,'Ran_From' ,unique=True)
        #
        ,sqlite_autoincrement=True
    )

def downgrade():
    op.drop_table('Job_Run')