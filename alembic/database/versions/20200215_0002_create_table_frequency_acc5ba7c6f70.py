"""Create Table Frequency

Revision ID: acc5ba7c6f70
Revises: 
Create Date: 2020-02-15 15:40:40.399071
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
revision = 'acc5ba7c6f70'
down_revision = None
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
CREATE  TABLE   Frequency (
         ID                 {xdb['int08'] :15} NOT NULL  CONSTRAINT Frequency_PK    PRIMARY KEY {xdb['autoinc']} {xdb['comment']} 'The Primary Key'   
        --
        ,Name               {xdb['txt08'] :15} NOT NULL  {xdb['comment']} 'Name of the frequency'
        ,Minutes            {xdb['int32'] :15} NOT NULL  {xdb['comment']} 'The number of minutes for this frequency'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
         --
        ,CONSTRAINT Frequency_ID_CK         CHECK(  ID BETWEEN 0 AND 8 )
        ,CONSTRAINT Frequency_Minutes_CK    CHECK(  Minutes >= 0 )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE UNIQUE INDEX Frequency_Name_UK1      ON  Frequency( Name )
"""
    context.execute( sql_text )

    # Seed the table.
    if  db == 'mssql':
        context.execute("SET IDENTITY_INSERT Frequency ON" )
    op.bulk_insert(
        table(      'Frequency'
            ,column('ID'        ,sa.SmallInteger)
            ,column('Name'      ,sa.String())
            ,column('Minutes'   ,sa.Integer)
        ) 
        ,[   {'ID': 0 ,'Name': 'Manual'   ,'Minutes': 0     }
            ,{'ID': 1 ,'Name': 'Minute'   ,'Minutes': 1     }
            ,{'ID': 2 ,'Name': 'Hour'     ,'Minutes': 60    }
            ,{'ID': 3 ,'Name': 'Day'      ,'Minutes': 1440  }
            ,{'ID': 4 ,'Name': 'Week'     ,'Minutes': 10080 }
            ,{'ID': 5 ,'Name': 'Month'    ,'Minutes': 43200 }
            ,{'ID': 6 ,'Name': 'Quarter'  ,'Minutes': 129600}
            ,{'ID': 7 ,'Name': 'Semester' ,'Minutes': 172800}
            ,{'ID': 8 ,'Name': 'Annual'   ,'Minutes': 525600}
        ]
    )
    if  db == 'mssql':
        context.execute("SET IDENTITY_INSERT Frequency OFF" )

def downgrade():
    context.execute( "DROP  TABLE  Frequency" )
