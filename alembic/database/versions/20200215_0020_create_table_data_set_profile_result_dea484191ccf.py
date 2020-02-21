"""Create Table Data Set Profile Result

Revision ID: dea484191ccf
Revises: 0f5887fb18e4
Create Date: 2020-02-15 15:40:47.742684
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'dea484191ccf'
down_revision = '0f5887fb18e4'
branch_labels = None
depends_on = None


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

def downgrade():
    op.drop_table('Data_Set_Profile_Result')
