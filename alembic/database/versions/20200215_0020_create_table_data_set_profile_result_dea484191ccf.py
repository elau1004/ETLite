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
#       ,sa.Column('Field_Name'     ,sa.String(64)  ,nullable=False )
        ,sa.Column('Aggregate_Type' ,sa.String(64)  ,nullable=False )
        ,sa.Column('Count'          ,sa.BigInteger  ,nullable=True  )
        ,sa.Column('Value_Int'      ,sa.BigInteger  ,nullable=True  )
        ,sa.Column('Value_Flt'      ,sa.Float       ,nullable=True  )
        ,sa.Column('Value_Dtm'      ,sa.DateTime    ,nullable=True  )
        ,sa.Column('Value_Str'      ,sa.String      ,nullable=True  )
        ,dt_updated_on
        #
        ,sa.CheckConstraint(    'ID >= 1'                       ,name='ID'  )
        ,sa.CheckConstraint(    'Field_Seq BETWEEN 1 AND 255'   ,name='Field_Seq' )
        ,sa.ForeignKeyConstraint(['Job_Run_ID'] ,['Job_Run.ID']  )
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        #
        ,sa.Index('Data_Set_Profile_Result_UK1' ,'Data_Set_ID' ,'Field_Seq' ,unique=True)
    )

def downgrade():
    op.drop_table('Data_Set_Profile_Result')
