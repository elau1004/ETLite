"""Create Table Data Set Profile

Revision ID: 0f5887fb18e4
Revises: 8da2a5812ba2
Create Date: 2020-02-15 15:40:46.850170
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa



# revision identifiers, used by Alembic.
revision = '0f5887fb18e4'
down_revision = '8da2a5812ba2'
branch_labels = None
depends_on = None


config = context.config
engine = create_engine( config.get_main_option("sqlalchemy.url") )

dt_updated_on = sa.Column(
                    'Updated_On'
                    ,sa.DateTime(timezone=True)
                    ,nullable=False
                    ,server_default=func.current_timestamp()
                    ,comment='The audit timestamp when this row was last updated'
                )

def upgrade():
    op.create_table(
        'Data_Set_Profile'
        ,sa.Column('ID'             ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Data_Set_ID'    ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Status_ID'      ,sa.SmallInteger,nullable=False ,server_default='2' )   # Enabled
        ,sa.Column('Field_Seq'      ,sa.SmallInteger,nullable=False ,server_default='1' ,comment='The order of the field in the file/table.')
        ,sa.Column('Field_Name'     ,sa.String(64)  ,nullable=False ,comment='The name of the field.')
        ,sa.Column('Data_Type'      ,sa.String(8)   ,nullable=False ,comment='The data type pof the field.')
        ,sa.Column('do_Count'       ,sa.Boolean(name='do_Count')    ,nullable=False ,server_default='1' )
        ,sa.Column('do_Blank'       ,sa.Boolean(name='do_Blank')    ,nullable=False ,server_default='1' )
        ,sa.Column('do_Distinct'    ,sa.Boolean(name='do_Distinct') ,nullable=False ,server_default='1' )
        ,sa.Column('do_Average'     ,sa.Boolean(name='do_Average')  ,nullable=False ,server_default='1' )
        ,sa.Column('do_Median'      ,sa.Boolean(name='do_Median')   ,nullable=False ,server_default='0' )
        ,sa.Column('do_Minimum'     ,sa.Boolean(name='do_Minimum')  ,nullable=False ,server_default='1' )
        ,sa.Column('do_Maximum'     ,sa.Boolean(name='do_Maximum')  ,nullable=False ,server_default='1' )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 32767'       ,name='ID')
        ,sa.CheckConstraint( 'Field_Seq BETWEEN 1 AND 255'  ,name='Field_Seq' )
        ,sa.CheckConstraint( "Upper(Data_Type) IN('INTEGER' ,'REAL' ,'DATETIME' ,'DATE' ,'TIME')"
                                                            ,name='Data_Type')
        ,sa.CheckConstraint( 'Status_ID BETWEEN 1 AND 2'    ,name='Status_ID' )
        #
        ,sa.ForeignKeyConstraint(['Data_Set_ID']  ,['Data_Set.ID']  )
        #
        ,sa.Index('Data_Set_Profile_UK1' ,'Data_Set_ID' ,'Field_Seq'    ,unique=True)
        ,sa.Index('Data_Set_Profile_UK2' ,'Data_Set_ID' ,'Field_Name'   ,unique=True)
    )

    sql_view  = """
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
JOIN    Data_Set            As  ds  ON  ds.ID   =   pf.Data_Set_ID
JOIN    Status              AS  st  ON  st.ID   =   pf.Status_ID
"""
    with engine.connect() as conn:
        conn.execute( sql_view )


def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Data_Set_Profile_View" )

    op.drop_table('Data_Set_Profile')
