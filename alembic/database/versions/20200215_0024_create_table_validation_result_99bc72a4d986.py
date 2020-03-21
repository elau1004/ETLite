"""Create Table Validation Result

Revision ID: 99bc72a4d986
Revises: 3652e714353c
Create Date: 2020-02-15 15:40:49.517711
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
revision = '99bc72a4d986'
down_revision = '3652e714353c'
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
CREATE  TABLE   Validation_Result (
         ID                 {xdb['int32'] :15} NOT NULL  CONSTRAINT Validation_Result_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Validation_Rule_ID {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Foreign Key to the Validation Rule table.'
        ,Job_Run_ID         {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'Foreign key to the Job Run table.'
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.'
        ,Severity_ID        {xdb['int08'] :15} NOT NULL  DEFAULT 4 {xdb['comment']} 'Foreign key to the Severity table. server_default='4' )   # Info
        ,Expect_Int         {xdb['int64'] :15}     NULL  {xdb['comment']} 'The expected integer value.'
        ,Actual_Int         {xdb['int64'] :15}     NULL  {xdb['comment']} 'The actual   integer value.'
        ,Expect_Flt         {xdb['real']  :15}     NULL  {xdb['comment']} 'The expected float value.'
        ,Actual_Flt         {xdb['real']  :15}     NULL  {xdb['comment']} 'The actual   float  value.'
        ,Expect_Dtm         {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The expected datetime value.'
        ,Actual_Dtm         {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The actual   datetime value.'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Validation_Result_ID_CK     CHECK(  ID >= 1 )
         --
        ,CONSTRAINT Validation_Result_Validation_FK     FOREIGN KEY( Validation_Rule_ID) REFERENCES Validation_Rule( ID )
        ,CONSTRAINT Validation_Result_Job_Run_FK        FOREIGN KEY( Job_Run_ID        ) REFERENCES Job_Run( ID )
        ,CONSTRAINT Validation_Result_Data_Set_FK       FOREIGN KEY( Data_Set_ID       ) REFERENCES Data_Set( ID )
        ,CONSTRAINT Validation_Result_Severity_FK       FOREIGN KEY( Severity_ID       ) REFERENCES Severity( ID )
)
"""
    context.execute( sql_text )

    sql_text = """
CREATE UNIQUE INDEX Validation_Result_UK1   ON  Validation_Result( Job_Run_ID ,Validation_Rule_ID )
"""
    context.execute( sql_text )

    sql_text = """
CREATE  VIEW    Validation_Result_View
AS
SELECT  vs.ID
       ,vs.Validation_Rule_ID
       ,vr.Code             AS  Validation_Rule_Code
       ,vs.Job_Run_ID
       ,jr.Run_No           AS  Job_Run_No
       ,vs.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,vs.Severity_ID
       ,sv.Name             AS  Severity_Name
       ,vs.Expect_Int
       ,vs.Actual_Int
       ,vs.Expect_Flt
       ,vs.Actual_Flt
       ,vs.Expect_Dtm
       ,vs.Actual_Dtm
       ,vs.Updated_On
FROM    Validation_Result   AS  vs
JOIN    Data_Set            AS  ds  ON  ds.ID   =   vs.Data_Set_ID
JOIN    Job_Run             AS  jr  ON  jr.ID   =   vs.Job_Run_ID
JOIN    Severity            AS  sv  ON  sv.ID   =   vs.Severity_ID
JOIN    Validation_Rule     AS  vr  ON  vr.ID   =   vs.Validation_Rule_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW  Validation_Result_View" )
    context.execute( "DROP  TABLE Validation_Result" )
