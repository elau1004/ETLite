"""Create Table Job Run Profile Result

Revision ID: dea484191ccf
Revises: 0f5887fb18e4
Create Date: 2020-02-15 15:40:47.742684
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
revision = 'dea484191ccf'
down_revision = '0f5887fb18e4'
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
CREATE  TABLE   Job_Run_Profile_Result (
         ID                 {xdb['int32'] :15} NOT NULL  CONSTRAINT Job_Run_Profile_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Job_Run_ID         {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'Foreign Key to Job_Run table.'
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.'
        ,Profile_ID         {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'Foreign Key to Data_Set_Profile table.'
        ,Field_Seq          {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.'
        ,Record_Count       {xdb['int64'] :15}     NULL  {xdb['comment']} 'Total raw count for this field in the data set for this job run.')
        ,Blank_Count        {xdb['int64'] :15}     NULL  {xdb['comment']} 'Total null values for this field in the data set for this job run.')
        ,Distinct_Count     {xdb['int64'] :15}     NULL  {xdb['comment']} 'Total distinct values for this field in the data set for this job run.')
        ,Average_NumValue   {xdb['real']  :15}     NULL  {xdb['comment']} 'The average aggregated number.'
        ,Median_NumValue    {xdb['real']  :15}     NULL  {xdb['comment']} 'The median  aggregated number.'
        ,Minimum_NumValue   {xdb['real']  :15}     NULL  {xdb['comment']} 'The minimum aggregated number.'
        ,Maximum_NumValue   {xdb['real']  :15}     NULL  {xdb['comment']} 'The maxinum aggregated number.'
        ,Average_DtmValue   {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The average aggregated datetime. # SEE: https://www.bennadel.com/blog/175-ask-ben-averaging-date-time-stamps-in-sql.htm'
        ,Median_DtmValue    {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The median  aggregated datetime. #  SEE: https://www.bennadel.com/blog/175-ask-ben-averaging-date-time-stamps-in-sql.htm'
        ,Minimum_DtmValue   {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The minimum aggregated datetime.'
        ,Maximum_DtmValue   {xdb['utcdtm']:15}     NULL  {xdb['comment']} 'The maxinum aggregated datetime.'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Job_Run_Profile_Result_ID_CK        CHECK(  ID >= 1 )
        ,CONSTRAINT Job_Run_Profile_Result_Field_Seq_CK CHECK(  Field_Seq BETWEEN 1 AND 255 )
         --
        ,CONSTRAINT Job_Run_Profile_Result_Job_Run_FK   FOREIGN KEY( Job_Run_ID )  REFERENCES Job_Run( ID )
        ,CONSTRAINT Job_Run_Profile_Result_Data_Set_FK  FOREIGN KEY( Data_Set_ID ) REFERENCES Data_Set( ID )
        ,CONSTRAINT Job_Run_Profile_Result_Profile_FK   FOREIGN KEY( Profile_ID )  REFERENCES Data_Set_Profile( ID )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE UNIQUE INDEX Job_Run_Profile_Result_UK1  ON  Job_Run_Profile_Result( Job_Run_ID ,Field_Seq )
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  VIEW    Job_Run_Profile_Result_View
AS
SELECT  pr.ID
       ,pr.Job_Run_ID
       ,jr.Run_No           AS  Job_Run_No
       ,pr.Profile_ID
       ,pr.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,pr.Field_Seq
       ,pf.Field_Name
       ,pr.Record_Count
       ,pr.Blank_Count
       ,pr.Distinct_Count
       ,pr.Average_NumValue
       ,pr.Median_NumValue
       ,pr.Minimum_NumValue
       ,pr.Maximum_NumValue
       ,pr.Average_DtmValue
       ,pr.Median_DtmValue
       ,pr.Minimum_DtmValue
       ,pr.Maximum_DtmValue
       ,pr.Updated_On
FROM    Job_Run_Profile_Result  AS  pr
JOIN    Job_Run                 AS  jr  ON  jr.ID       =   pr.Job_Run_ID
JOIN    Data_Set                AS  ds  ON  ds.ID       =   pr.Data_Set_ID
JOIN    Data_Set_Profile        AS  pf  ON  pf.ID       =   pr.Profile_ID
                                        AND pf.Field_Seq=   pr.Field_Seq
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW  Job_Run_Profile_Result_View" )
    context.execute( "DROP  TABLE Job_Run_Profile_Result" )
