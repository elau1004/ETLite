"""Create Table Job Run File

Revision ID: f540cc84a360
Revises: 387bcafcfbb3
Create Date: 2020-02-15 15:40:45.176644
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'f540cc84a360'
down_revision = '387bcafcfbb3'
branch_labels = None
depends_on = None


config = context.config
engine = create_engine( config.get_main_option("sqlalchemy.url") )

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
        ,sa.Column('Data_Set_ID'    ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
#       ,sa.Column('Status_ID'      ,sa.SmallInteger,nullable=False )
        ,sa.Column('File_URI'       ,sa.String      ,nullable=False ,comment='The file to ingest the data set from.')
        ,sa.Column('Line_Count'     ,sa.Integer                     ,comment='The number of lines in this file akin to "wc -l"')
        ,sa.Column('MD5'            ,sa.Binary(16)                  ,comment='The file MD5 checksum to detact doplicated content.')
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'              ,name='ID')
        ,sa.CheckConstraint( 'Length( MD5 ) = 16'   ,name='MD5')
        #
        ,sa.ForeignKeyConstraint(['Job_Run_ID'] ,['Job_Run.ID'])
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
#       ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID'])
        #
        ,sa.Index('Job_Run_Import_File_UK1' ,'MD5'          ,unique=True  )
        ,sa.Index('Job_Run_Import_File_K1'  ,'Job_Run_ID'   ,unique=False )
#       ,sa.Index('Job_Run_Import_File_K2'  ,'Data_Set_ID'  ,unique=False )
        #
        ,sqlite_autoincrement=True
    )

    sql_view  = """
CREATE  VIEW    Job_Run_Import_File_View
AS
SELECT  if.ID
       ,if.Job_Run_ID
       ,if.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,if.File_URI
       ,if.Line_Count
       ,if.MD5
       ,if.Updated_On
FROM    Job_Run_Import_File AS  if
JOIN    Data_Set            As  ds  ON  ds.ID   =   if.Data_Set_ID
"""
    with engine.connect() as conn:
        conn.execute( sql_view )


def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Job_Run_Import_File_View" )

    op.drop_table('Job_Run_Import_File')
