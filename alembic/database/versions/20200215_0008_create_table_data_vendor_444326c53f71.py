"""Create Table Data Vendor

Revision ID: 444326c53f71
Revises: ebc75428d24b
Create Date: 2020-02-15 15:40:42.936610
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
revision = '444326c53f71'
down_revision = 'ebc75428d24b'
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
CREATE  TABLE   Data_Vendor (
         ID                 {xdb['int16'] :15} NOT NULL  CONSTRAINT Vendor_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Code               {xdb['txt08'] :15} NOT NULL  {xdb['comment']} 'Unique mnemonic of the data vendor'
        ,Status_ID          {xdb['int08'] :15} NOT NULL  DEFAULT 2    {xdb['comment']} 'Foreign key to the status.  Default to enabled.'
        ,Name               {xdb['txt64'] :15} NOT NULL  {xdb['comment']} 'Name of the data vendor'
        --
        ,Updated_On         {xdb['utcupd']:52} {xdb['comment']} 'The audit timestamp when this row was last updated'
        --
        ,CONSTRAINT Data_Vendor_ID_CK       CHECK(  ID BETWEEN 1 AND 1024 )
        ,CONSTRAINT Data_Vendor_Status_CK   CHECK(  Status_ID BETWEEN 1 AND 2 )
        --
        ,CONSTRAINT Data_Vendors_Status_FK  FOREIGN KEY( Status_ID ) REFERENCES Status( ID )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE UNIQUE INDEX Data_Vendor_Code_UK1    ON  Data_Vendor( Code )
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE  VIEW    Data_Vendor_View
AS
SELECT  dv.ID
       ,dv.Code
       ,dv.Status_ID
       ,st.Name     AS  Status
       ,dv.Name
       ,dv.Updated_On
FROM    Data_Vendor AS  dv
JOIN    Status      AS  st  ON  st.ID   =   dv.Status_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW   Data_Vendor_View" )
    context.execute( "DROP  TABLE  Data_Vendor" )
