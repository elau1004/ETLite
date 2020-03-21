"""Create Table Data Set Profile

Revision ID: 0f5887fb18e4
Revises: 8da2a5812ba2
Create Date: 2020-02-15 15:40:46.850170
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
revision = '0f5887fb18e4'
down_revision = '8da2a5812ba2'
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
CREATE  TABLE   Data_Set_Profile (
         ID                 {xdb['int32'] :15} NOT NULL  CONSTRAINT Data_Set_Profile_PK PRIMARY KEY {xdb['clstr0']} {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized column for querying.'
        ,Status_ID          {xdb['int08'] :15} NOT NULL  DEFAULT 2    {xdb['comment']} 'Foreign key to the status.  Default to enabled.'
        ,Field_Seq          {xdb['int08'] :15} NOT NULL  {xdb['comment']} 'The order of the field in the file/table.'
        ,Field_Name         {xdb['txt64'] :15} NOT NULL  {xdb['comment']} 'The name of the field.'
        ,Data_Type          {xdb['txt08'] :15} NOT NULL  {xdb['comment']} 'The data type of the field. DATE, DATETIME, INTEGER, FLOAT, STRING ,TIME'
        ,do_Count           {xdb['bit1']  :15} {xdb['comment']} 'Boolean flag to enable/disable Count    aggregation.'
        ,do_Blank           {xdb['bit1']  :15} {xdb['comment']} 'Boolean flag to enable/disable Blank    aggregation.'
        ,do_Distinct        {xdb['bit1']  :15} {xdb['comment']} 'Boolean flag to enable/disable Distinct aggregation.'
        ,do_Average         {xdb['bit1']  :15} {xdb['comment']} 'Boolean flag to enable/disable Average  aggregation.'
        ,do_Median          {xdb['bit0']  :15} {xdb['comment']} 'Boolean flag to enable/disable Median   aggregation.'
        ,do_Minimum         {xdb['bit1']  :15} {xdb['comment']} 'Boolean flag to enable/disable Minimum  aggregation.'
        ,do_Maximum         {xdb['bit1']  :15} {xdb['comment']} 'Boolean flag to enable/disable Maximum  aggregation.'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Data_Set_Profile_ID_CK         CHECK(  ID BETWEEN 1 AND 32767 )
        ,CONSTRAINT Data_Set_Profile_Field_Seq_CK  CHECK(  Field_Seq BETWEEN 1 AND 255 )
        ,CONSTRAINT Data_Set_Profile_Data_Type_CK  CHECK(  Upper(Data_Type) IN('INTEGER' ,'FLOAT' ,'DATETIME' ,'DATE' ,'TIME' ,'STRING') )
         --
        ,CONSTRAINT Data_Set_Profile_Data_Set_FK   FOREIGN KEY( Data_Set_ID ) REFERENCES Data_Set( ID )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  UNIQUE {xdb['clstr1']}INDEX  Data_Set_Profile_UK1  ON  Data_Set_Profile( Data_Set_ID ,Field_Seq )
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  UNIQUE INDEX  Data_Set_Profile_UK2  ON  Data_Set_Profile( Data_Set_ID ,Field_Name )
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  VIEW    Data_Set_Profile_View
AS
SELECT  pf.ID
       ,pf.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,pf.Status_ID
       ,st.Name             AS  Status_Name
       ,pf.Field_Seq
       ,pf.Field_Name
       ,pf.Data_Type
       ,pf.do_Count
       ,pf.do_Blank
       ,pf.do_Distinct
       ,pf.do_Average
       ,pf.do_Median
       ,pf.do_Minimum
       ,pf.do_Maximum
       ,pf.Updated_On
FROM    Data_Set_Profile    AS  pf
JOIN    Data_Set            AS  ds  ON  ds.ID   =   pf.Data_Set_ID
JOIN    Status              AS  st  ON  st.ID   =   pf.Status_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW  Data_Set_Profile_View" )
    context.execute( "DROP  TABLE Data_Set_Profile" )
