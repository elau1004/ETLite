"""Create Table Job Run

Revision ID: 387bcafcfbb3
Revises: 7a670e1241eb
Create Date: 2020-02-15 15:40:44.429133
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '387bcafcfbb3'
down_revision = '7a670e1241eb'
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
        'Job_Run'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Run_No'             ,sa.Integer     ,nullable=False ,comment='A grouping/batch number assigned to this job run.')
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Status_ID'          ,sa.SmallInteger,nullable=False ,comment='The state this job is currently in.')
        ,sa.Column('Data_From'          ,sa.DateTime(    timezone=True ),comment='The incremental starting date/time for the last successful ETL execution.')
        ,sa.Column('Data_Upto'          ,sa.DateTime(    timezone=True ),comment='The incremental ending date/time (not inclusive) the last successful ETL execution.')
        ,sa.Column('Ran_From'           ,sa.DateTime(    timezone=True ),comment='The UTC datetime the ETL job last started on.')
        ,sa.Column('Ran_Upto'           ,sa.DateTime(    timezone=True ),comment='The UTC datetime the ETL job last ended on')
        ,sa.Column('Total_Count'        ,sa.Integer                     ,comment='Raw count from the processed dataset.' )
        ,sa.Column('Unique_Count'       ,sa.Integer                     ,comment='Raw count from the processed dataset.' )
        ,sa.Column('Ingest_Count'       ,sa.Integer                     ,comment='Raw count from the processed dataset.' )
        ,sa.Column('Error_Count'        ,sa.Integer                     ,comment='Raw count from the processed dataset.' )
        ,sa.Column('Files_Count'        ,sa.SmallInteger                ,comment='Raw count from the processed dataset.' )
        ,sa.Column('Extra_Count_'       ,sa.Integer                     ,comment='Resevrsed for the future.' )
        ,sa.Column('Remark'             ,sa.String                      ,comment='Remark specific to this job run.' )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'          ,name='ID' )
        ,sa.CheckConstraint( 'Status_ID >= 3'   ,name='Status_ID'  )
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

    sql_view  = """
CREATE  VIEW    Job_Run_View
AS
SELECT  jr.ID
       ,jr.Run_No
       ,jr.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,jr.Status_ID
       ,st.Name             AS  Status_Name
       ,jr.Data_From
       ,jr.Data_Upto
       ,jr.Ran_From
       ,jr.Ran_Upto
       ,jr.Total_Count
       ,jr.Unique_Count
       ,jr.Ingest_Count
       ,jr.Error_Count
       ,jr.Files_Count
       ,jr.Remark
       ,jr.Updated_On
FROM    Job_Run     AS  jr
JOIN    Data_Set    As  ds  ON  ds.ID   =   jr.Data_Set_ID
JOIN    Status      AS  st  ON  st.ID   =   ds.Status_ID
"""
    with engine.connect() as conn:
        conn.execute( sql_view )


def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Job_Run_View" )

    op.drop_table('Job_Run')
