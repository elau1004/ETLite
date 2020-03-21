"""Create Table Job Run

Revision ID: 387bcafcfbb3
Revises: 7a670e1241eb
Create Date: 2020-02-15 15:40:44.429133
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
revision = '387bcafcfbb3'
down_revision = '7a670e1241eb'
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
    sql_text = f"""
CREATE  TABLE   Job_Run (
         ID                 {xdb['int32'] :15} NOT NULL  CONSTRAINT Job_Run_PK PRIMARY KEY {xdb['clstr0']} {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Run_No             {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'A grouping/batch number assigned to this job run.'
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.'
        ,Status_ID          {xdb['int08'] :15} NOT NULL  {xdb['comment']} 'The state this job is currently in.'
        ,Data_From          {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The incremental starting date/time for the last successful ETL execution.'
        ,Data_Upto          {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The incremental ending date/time (not inclusive) the last successful ETL execution.'
        ,Ran_From           {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The UTC datetime the ETL job last started on.'
        ,Ran_Upto           {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The UTC datetime the ETL job last ended on'
        ,Total_Count        {xdb['int32'] :15}     NULL  {xdb['comment']} 'Raw count from the processed dataset.'
        ,Unique_Count       {xdb['int32'] :15}     NULL  {xdb['comment']} 'Raw count from the processed dataset.'
        ,Ingest_Count       {xdb['int32'] :15}     NULL  {xdb['comment']} 'Raw count from the processed dataset.'
        ,Error_Count        {xdb['int16'] :15}     NULL  {xdb['comment']} 'Raw count from the processed dataset.'
        ,Files_Count        {xdb['int08'] :15}     NULL  {xdb['comment']} 'Raw count from the processed dataset.'
        ,Deleted_Count      {xdb['int32'] :15}     NULL  {xdb['comment']} 'Raw count from the processed dataset.'
        ,Extra_Count_       {xdb['int32'] :15}     NULL  {xdb['comment']} 'Reserved for the future.'
        ,Remark             {xdb['txt128']:15}     NULL  {xdb['comment']} 'Remark specific to this job run.'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Job_Run_ID_CK           CHECK(  ID > 0 )
        ,CONSTRAINT Job_Run_Status_FK       FOREIGN KEY( Status_ID   ) REFERENCES Status( ID )
        ,CONSTRAINT Job_Run_Data_Set_FK     FOREIGN KEY( Data_Set_ID ) REFERENCES Data_Set( ID )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  UNIQUE  {xdb['clstr1']}INDEX  Job_Run_UK1          ON  Job_Run( Data_Set_ID ,Run_No )
"""
    context.execute( sql_text )

    sql_text = """
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
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW   Job_Run_View" )
    context.execute( "DROP  TABLE  Job_Run" )
