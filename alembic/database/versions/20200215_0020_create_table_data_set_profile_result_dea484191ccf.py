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
        ,sa.Column('ID'             ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Job_Run_ID'     ,sa.Integer     ,nullable=False )
        ,sa.Column('Data_Set_ID'    ,sa.SmallInteger,nullable=False )
        ,sa.Column('Field_Seq'      ,sa.SmallInteger,nullable=False ,server_default='1' )
#       ,sa.Column('Aggregate_Type' ,sa.String(64)  ,nullable=False )
        ,sa.Column('Record_Count'   ,sa.BigInteger  ,nullable=False )
        ,sa.Column('Blank_Count'    ,sa.BigInteger  ,nullable=False )
        ,sa.Column('Distinct_Count' ,sa.BigInteger  ,nullable=False )
        #
        ,sa.Column('Average_IntType',sa.BigInteger  )
        ,sa.Column('Median_IntType' ,sa.BigInteger  )
        ,sa.Column('Minimum_IntType',sa.BigInteger  )
        ,sa.Column('Maximum_IntType',sa.BigInteger  )
        ,sa.Column('Average_FltType',sa.Float       )
        ,sa.Column('Median_FltType' ,sa.Float       )
        ,sa.Column('Minimum_FltType',sa.Float       )
        ,sa.Column('Maximum_FltType',sa.Float       )
        ,sa.Column('Average_DtmType',sa.DateTime    )
        ,sa.Column('Median_DtmType' ,sa.DateTime    )
        ,sa.Column('Minimum_DtmType',sa.DateTime    )
        ,sa.Column('Maximum_DtmType',sa.DateTime    )
        ,dt_updated_on
        #
        ,sa.CheckConstraint(    'ID >= 1'                       ,name='ID'  )
        ,sa.CheckConstraint(    'Field_Seq BETWEEN 1 AND 255'   ,name='Field_Seq' )
        #
        ,sa.ForeignKeyConstraint(['Job_Run_ID'] ,['Job_Run.ID']  )
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Data_Set_ID'                 ,'Field_Seq']
                                ,['Data_Set_Profile.Data_Set_ID','Data_Set_Profile.Field_Seq'])
        #
        ,sa.Index('Data_Set_Profile_Result_UK1' ,'Data_Set_ID' ,'Field_Seq' ,unique=True)
    )

def downgrade():
    op.drop_table('Data_Set_Profile_Result')
