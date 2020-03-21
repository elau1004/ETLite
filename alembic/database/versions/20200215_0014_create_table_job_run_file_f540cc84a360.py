"""Create Table Job Run File

Revision ID: f540cc84a360
Revises: 387bcafcfbb3
Create Date: 2020-02-15 15:40:45.176644
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
revision = 'f540cc84a360'
down_revision = '387bcafcfbb3'
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
CREATE  TABLE   Job_Run_Import_File (
         ID                 {xdb['int32'] :15} NOT NULL  CONSTRAINT Job_Run_Import_PK PRIMARY KEY {xdb['clstr0']} {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Job_Run_ID         {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'Foreign key to Job run.'
        ,Data_Set_ID        {xdb['int16'] :15} NOT NULL  {xdb['comment']} 'Denormalized foreign key column for querying.')
        ,File_URI           {xdb['txt64'] :15} NOT NULL  {xdb['comment']} 'The file URI to ingest the data set from.')
        ,Line_Count         {xdb['int32'] :15}     NULL  {xdb['comment']} 'The number of lines in this file akin to "wc -l"')
        ,MD5                {xdb['bin16'] :15}     NULL  {xdb['comment']} 'The file MD5 checksum to detact duplicated content regardless of file name.')
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Job_Run_Import_File_ID_CK   CHECK(  ID > 0 )
        ,CONSTRAINT Job_Run_Import_File_MD5_CK  CHECK(  {xdb['len']}( MD5 ) = 16 )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  {xdb['clstr1']}INDEX   Job_Run_Import_File_K1      ON  Job_Run_Import_File( Data_Set_ID ,Job_Run_ID )
"""
    context.execute( sql_text )

    sql_text = """
CREATE  VIEW    Job_Run_Import_File_View
AS
SELECT  jf.ID
       ,jf.Job_Run_ID
       ,jf.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,jf.File_URI
       ,jf.Line_Count
       ,jf.MD5
       ,jf.Updated_On
FROM    Job_Run_Import_File AS  jf
JOIN    Data_Set            AS  ds  ON  ds.ID   =   jf.Data_Set_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW  Job_Run_Import_File_View" )
    context.execute( "DROP  TABLE Job_Run_Import_File" )
