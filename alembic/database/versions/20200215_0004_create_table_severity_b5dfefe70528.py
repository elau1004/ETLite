"""Create Table Severity

Revision ID: b5dfefe70528
Revises: acc5ba7c6f70
Create Date: 2020-02-15 15:40:41.309085
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
revision = 'b5dfefe70528'
down_revision = 'acc5ba7c6f70'
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
CREATE  TABLE   Severity (
         ID                 {xdb['int08'] :15} NOT NULL  CONSTRAINT Severity_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Name               {xdb['txt16'] :15} NOT NULL  {xdb['comment']} 'Name of the severity'
        ,Description        {xdb['txt64'] :15} NOT NULL  {xdb['comment']} 'Description of the severity'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Severity_ID_CK          CHECK(  ID BETWEEN 1 AND 5 )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE UNIQUE INDEX Severity_Name_UK1       ON  Severity( Name )
"""
    context.execute( sql_text )

    # Seed the table.
    if  db == 'mssql':
        context.execute("SET IDENTITY_INSERT Severity ON" )
    op.bulk_insert(
        table(      'Severity'
            ,column('ID'            ,sa.SmallInteger)
            ,column('Name'          ,sa.String())
            ,column('Description'   ,sa.String())
        )
        ,[   {'ID': 1 ,'Name': 'Critical'   ,'Description': 'Functionality is affected.' }
            ,{'ID': 2 ,'Name': 'Error'      ,'Description': 'An error condition exists and functionality could be affected.' }
            ,{'ID': 3 ,'Name': 'Warning'    ,'Description': 'Functionality could be affected.' }
            ,{'ID': 4 ,'Name': 'Information','Description': 'General information about system operations.' }
            ,{'ID': 5 ,'Name': 'Debug'      ,'Description': 'Debugging trace.' }
        ,]
    )
    if  db == 'mssql':
        context.execute("SET IDENTITY_INSERT Severity OFF" )

def downgrade():
    context.execute( "DROP  TABLE  Severity" )
