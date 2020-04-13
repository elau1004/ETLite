"""Create Table Validation Rule

Revision ID: 3652e714353c
Revises: dea484191ccf
Create Date: 2020-02-15 15:40:48.630197
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
revision = '3652e714353c'
down_revision = 'dea484191ccf'
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
CREATE  TABLE   Validation_Rule (
         ID                 {xdb['int16'] :15} NOT NULL  CONSTRAINT Validation_Rule_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Code               {xdb['txt64'] :15} NOT NULL  {xdb['comment']} 
        ,Parent_ID          {xdb['int16'] :15}     NULL  {xdb['comment']} 'The parent rule that is tpo be inherited down to this row.')
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.')
        ,Status_ID          {xdb['int08'] :15} NOT NULL  DEFAULT 2      {xdb['comment']} 'Foreign key to the status.  Default to enabled.'
        ,Description        {xdb['txt128']:15} NOT NULL  {xdb['comment']} 'Description of this rule.'
        ,Assert_Order       {xdb['int16'] :15} NOT NULL  DEFAULT 1      {xdb['comment']} 'Placement order in the validation sequence.'
        ,Run_Frequency_ID   {xdb['int08'] :15} NOT NULL  DEFAULT 3      {xdb['comment']} 'The frequency to validate this job run result.  Default to Daily.'
        ,Frequency_Interval {xdb['int32'] :15} NOT NULL  DEFAULT 1      {xdb['comment']} 'The frequency interval to validate this job run result.' )
        ,Threshold_Type     {xdb['chr01'] :15} NOT NULL  {xdb['comment']} 'A=Absolute ,S=Stadard Deviation ,P=Percentage'
        ,Warn_Top_Limit     {xdb['real']  :15} NOT NULL  DEFAULT  0.02  {xdb['comment']} 'Upper threshold to trigger a warning notification.'
        ,Warn_Bot_Limit     {xdb['real']  :15} NOT NULL  DEFAULT -0.02  {xdb['comment']} 'Lower threshold to trigger a warning notification.'
        ,Error_Top_Limit    {xdb['real']  :15} NOT NULL  DEFAULT  0.03  {xdb['comment']} 'Upper threshold to trigger a error notification.'
        ,Error_Bot_Limit    {xdb['real']  :15} NOT NULL  DEFAULT -0.03  {xdb['comment']} 'Lower threshold to trigger a error notification.'
        ,Fatal_Top_Limit    {xdb['real']  :15} NOT NULL  DEFAULT  0.05  {xdb['comment']} 'Upper threshold to trigger a fatal notification.'
        ,Fatal_Bot_Limit    {xdb['real']  :15} NOT NULL  DEFAULT -0.05  {xdb['comment']} 'Lower threshold to trigger a fatal notification.'
        ,Expect_Metric_SQL  {xdb['txtmax']:15} NOT NULL  {xdb['comment']} 'The SQL query to generate the expected metric.'
        ,Actual_Metric_SQL  {xdb['txtmax']:15} NOT NULL  {xdb['comment']} 'The SQL query to generate the actual metric.'
        ,Last_Validated_On  {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'Hint to where the last successfully validated job run ID.'
        ,Last_Failed_On     {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'Hint to where the last failed job run ID.'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Validation_Rule_ID_CK        CHECK(  ID BETWEEN 1 AND 32767 )
        ,CONSTRAINT Validation_Rule_Order_CK     CHECK(  Assert_Order >= 1 )
        ,CONSTRAINT Validation_Rule_Freq_Int_CK  CHECK(  Frequency_Interval BETWEEN 1 AND 59 )
        ,CONSTRAINT Validation_Rule_Threshold_CK CHECK(  Threshold_Type IN(NULL,'A','S','P') )
        ,CONSTRAINT Validation_Rule_Warn_Top_CK  CHECK(  Warn_Top_Limit  >= 0 )
        ,CONSTRAINT Validation_Rule_Warn_Bot_CK  CHECK(  Warn_Bot_Limit  <= 0 )
        ,CONSTRAINT Validation_Rule_Error_Top_CK CHECK(  Error_Top_Limit >= 0 )
        ,CONSTRAINT Validation_Rule_Error_Bot_CK CHECK(  Error_Bot_Limit <= 0 )
        ,CONSTRAINT Validation_Rule_Fatal_Top_CK CHECK(  Fatal_Top_Limit >= 0 )
        ,CONSTRAINT Validation_Rule_Fatal_Bot_CK CHECK(  Fatal_Bot_Limit <= 0 )
         --
        ,CONSTRAINT Validation_Rule_Data_Set_FK  FOREIGN KEY( Data_Set_ID     ) REFERENCES Data_Set( ID )
        ,CONSTRAINT Validation_Rule_Parent_FK    FOREIGN KEY( Parent_ID       ) REFERENCES Validation_Rule( ID )
        ,CONSTRAINT Validation_Rule_Status_FK    FOREIGN KEY( Status_ID       ) REFERENCES Status( ID )
        ,CONSTRAINT Validation_Rule_Frequency_FK FOREIGN KEY( Run_Frequency_ID) REFERENCES Frequency( ID )
)
"""
    context.execute( sql_text )

    sql_text = """
CREATE UNIQUE INDEX Validation_Rule_UK1     ON  Validation_Rule( Code )
"""
    context.execute( sql_text )

    sql_text = """
CREATE  VIEW    Validation_Rule_View
AS
SELECT  vr.ID
       ,vr.Code
       ,vr.Parent_ID
       ,pr.Code             AS  Parent_Code
       ,pr.Parent_ID        AS  Grand_Parent_ID
       ,gp.Code             AS  Grand_Parent_Code
       ,vr.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,vr.Status_ID
       ,st.Name             AS  Status_Name
       ,vr.Description
       ,vr.Assert_Order
       ,vr.Run_Frequency_ID
       ,hz.Name             AS  Frequency_Name
       ,vr.Frequency_Interval
       ,vr.Threshold_Type
       ,vr.Warn_Top_Limit
       ,vr.Warn_Bot_Limit
       ,vr.Error_Top_Limit
       ,vr.Error_Bot_Limit
       ,vr.Fatal_Top_Limit
       ,vr.Fatal_Bot_Limit
       ,vr.Expect_Metric_SQL
       ,vr.Actual_Metric_SQL
       ,vr.Last_Validated_On
       ,vr.Last_Failed_On
       ,vr.Updated_On
FROM    Validation_Rule     AS  vr
LEFT    OUTER
JOIN    Validation_Rule     AS  pr  ON  pr.ID   =   vr.Parent_ID    -- Parent
LEFT    OUTER
JOIN    Validation_Rule     AS  gp  ON  pr.ID   =   vr.Parent_ID    -- Grand-parent
JOIN    Data_Set            As  ds  ON  ds.ID   =   vr.Data_Set_ID
JOIN    Status              AS  st  ON  st.ID   =   vr.Status_ID
JOIN    Frequency           AS  hz  ON  hz.ID   =   vr.Run_Frequency_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW  Validation_Rule_View" )
    context.execute( "DROP  TABLE Validation_Rule" )
