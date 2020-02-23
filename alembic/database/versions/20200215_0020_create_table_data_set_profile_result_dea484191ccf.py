"""Create Table Data Set Profile Result

Revision ID: dea484191ccf
Revises: 0f5887fb18e4
Create Date: 2020-02-15 15:40:47.742684
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'dea484191ccf'
down_revision = '0f5887fb18e4'
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
        'Data_Set_Profile_Result'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Job_Run_ID'         ,sa.Integer     ,nullable=False ,comment='Foreign Key to Job_Run table.')
        ,sa.Column('Data_Set_Profile_ID',sa.SmallInteger,nullable=False ,comment='Foreign Key to Data_Set_Profile table.')
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Field_Seq'          ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Record_Count'       ,sa.BigInteger  ,nullable=False ,comment='Total raw count for this field in the data set for this job run.')
        ,sa.Column('Blank_Count'        ,sa.BigInteger  ,nullable=False ,comment='Total null values for this field in the data set for this job run.')
        ,sa.Column('Distinct_Count'     ,sa.BigInteger  ,nullable=False ,comment='Total distinct values for this field in the data set for this job run.')
        #
        ,sa.Column('Average_NumValue'   ,sa.Float( 53 ) )   # SQL-Server to use 8 bytes.
        ,sa.Column('Median_NumValue'    ,sa.Float( 53 ) )   # SQL-Server to use 8 bytes.
        ,sa.Column('Minimum_NumValue'   ,sa.Float( 53 ) )   # SQL-Server to use 8 bytes.
        ,sa.Column('Maximum_NumValue'   ,sa.Float( 53 ) )   # SQL-Server to use 8 bytes.
        #
        ,sa.Column('Average_DtmValue'   ,sa.DateTime    )   # SEE: https://www.bennadel.com/blog/175-ask-ben-averaging-date-time-stamps-in-sql.htm
        ,sa.Column('Median_DtmValue'    ,sa.DateTime    )   # SEE: https://www.bennadel.com/blog/175-ask-ben-averaging-date-time-stamps-in-sql.htm
        ,sa.Column('Minimum_DtmValue'   ,sa.DateTime    )
        ,sa.Column('Maximum_DtmValue'   ,sa.DateTime    )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'  ,name='ID' )
        #
        ,sa.ForeignKeyConstraint(['Job_Run_ID'] ,['Job_Run.ID'] )
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Data_Set_Profile_ID'] ,['Data_Set_Profile.ID'] )
        #
        ,sqlite_autoincrement=True
    )

    sql_view  = """
CREATE  VIEW    Data_Set_Profile_Result_View
AS
SELECT  pr.ID
       ,pr.Job_Run_ID
       ,jr.Run_No           AS  Job_Run_No
       ,pr.Data_Set_Profile_ID
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
FROM    Data_Set_Profile_Result AS  pr
JOIN    Data_Set                AS  ds  ON  ds.ID       =   pr.Data_Set_ID
JOIN    Job_Run                 AS  jr  ON  jr.ID       =   pr.Job_Run_ID
JOIN    Data_Set_Profile        AS  pf  ON  pf.ID       =   pr.Data_Set_Profile_ID
                                        AND pf.Field_Seq=   pr.Field_Seq
"""
    with engine.connect() as conn:
        conn.execute( sql_view )


def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Data_Set_Profile_Result_View" )

    op.drop_table('Data_Set_Profile_Result')
