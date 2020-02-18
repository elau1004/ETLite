"""Create Table Job Run File

Revision ID: f540cc84a360
Revises: 387bcafcfbb3
Create Date: 2020-02-15 15:40:45.176644
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'f540cc84a360'
down_revision = '387bcafcfbb3'
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
        'Job_Run_Import_File'
        ,sa.Column('ID'             ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Job_Run_ID'     ,sa.Integer     ,nullable=False )
        ,sa.Column('Data_Set_ID'    ,sa.SmallInteger,nullable=False )
        ,sa.Column('Status_ID'      ,sa.SmallInteger,nullable=False )
        ,sa.Column('File_URI'       ,sa.String      ,nullable=False )
        ,sa.Column('Line_Count'     ,sa.Integer     )
        ,sa.Column('MD5'            ,sa.Binary(16)  )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'              ,name='ID')
        ,sa.CheckConstraint( 'Length( MD5 ) = 16'   ,name='MD5')
        #
        ,sa.ForeignKeyConstraint(['Job_Run_ID'] ,['Job_Run.ID'])
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID'])
        #
        ,sa.Index('Job_Run_Import_File_UK1' ,'MD5'          ,unique=True  )
        ,sa.Index('Job_Run_Import_File_K1'  ,'Job_Run_ID'   ,unique=False )
        ,sa.Index('Job_Run_Import_File_K2'  ,'Data_Set_ID'  ,unique=False )
        #
        ,sqlite_autoincrement=True
    )

def downgrade():
    op.drop_table('Job_Run_Import_File')
