"""Create Table Job Run Metric

Revision ID: 8da2a5812ba2
Revises: f540cc84a360
Create Date: 2020-02-15 15:40:45.962656
"""
# pylint: disable=maybe-no-member

from    alembic import context
from    alembic import op
from    importlib.machinery import SourceFileLoader
import  os
import  pathlib
import  sqlalchemy  as sa
from    sqlalchemy     import create_engine
from    sqlalchemy.sql import table, column, func


# revision identifiers, used by Alembic.
revision = '8da2a5812ba2'
down_revision = 'f540cc84a360'
branch_labels = None
depends_on = None


# NOTE: Need more precise control over the physical cross DB table design.
config  = context.config
db:str  = context.get_context().dialect.name
url:str = config.get_main_option("sqlalchemy.url")
engine  = create_engine( url )

# Dynamically load config module and assign ETLite Cross DB mapping to a locxal variable.
_path2cfg = str(sorted(pathlib.Path(os.getcwd()).glob( '**/xdb_config.py' )).pop())
# pylint: disable=no-value-for-parameter
xdb = SourceFileLoader( 'xdb_config' ,_path2cfg ).load_module().xdb_map[db]

def upgrade():
    sql_text  = f"""
CREATE  TABLE   Job_Run_Metric (
         ID                 {xdb['int32'] :15} NOT NULL  CONSTRAINT Job_Run_Metric_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Job_Run_ID         {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'A grouping/batch number assigned to this job run.'
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.'
        ,Stats              {xdb['json']  :15} NOT NULL  {xdb['comment']} 'A generic json to capture addition metrics.'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
        --
        ,CONSTRAINT Job_Run_Metric_ID_CK           CHECK(  ID > 0 )
        --
        ,CONSTRAINT Job_Run_Metric_Job_Run_FK      FOREIGN KEY( Job_Run_ID  ) REFERENCES Job_Run( ID )
        ,CONSTRAINT Job_Run_Metric_Data_Set_FK     FOREIGN KEY( Data_Set_ID ) REFERENCES Data_Set( ID )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE UNIQUE INDEX Job_Run_Metric_UK1      ON  Job_Run_Metric( Job_Run_ID )    --  1:1
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE        INDEX Job_Run_Metric_UK2      ON  Job_Run_Metric( Data_Set_ID )
"""
    context.execute( sql_text )

    sql_text  = f"""
CREATE  VIEW    Job_Run_Metric_View
AS
SELECT  rm.ID
       ,rm.Job_Run_ID
       ,rm.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,rm.Stats
       ,rm.Updated_On
FROM    Job_Run_Metric      AS  rm
JOIN    Data_Set            As  ds  ON  ds.ID   =   rm.Data_Set_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW  Job_Run_Metric_View" )
    context.execute( "DROP  TABLE Job_Run_Metric" )
