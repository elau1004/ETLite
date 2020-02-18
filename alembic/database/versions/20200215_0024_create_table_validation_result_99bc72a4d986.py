"""Create Table Validation Result

Revision ID: 99bc72a4d986
Revises: 3652e714353c
Create Date: 2020-02-15 15:40:49.517711
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '99bc72a4d986'
down_revision = '3652e714353c'
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
        'Validation_Result'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Validation_Rule_ID' ,sa.SmallInteger,nullable=False )
        ,sa.Column('Job_Run_ID'         ,sa.Integer     ,nullable=False )
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False )
        ,sa.Column('Severity_ID'        ,sa.SmallInteger,nullable=False ,server_default='4' )   # Info
        ,sa.Column('Expect_Int'         ,sa.BigInteger  )
        ,sa.Column('Actual_Int'         ,sa.BigInteger  )
        ,sa.Column('Expect_Flt'         ,sa.Float       )
        ,sa.Column('Actual_Flt'         ,sa.Float       )
        ,sa.Column('Expect_Dtm'         ,sa.DateTime    )
        ,sa.Column('Actual_Dtm'         ,sa.DateTime    )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'  ,name='ID' )
        #
        ,sa.ForeignKeyConstraint(['Validation_Rule_ID'] ,['Validation_Rule.ID'])
        ,sa.ForeignKeyConstraint(['Job_Run_ID']         ,['Job_Run.ID'] )
        ,sa.ForeignKeyConstraint(['Data_Set_ID']        ,['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Severity_ID']        ,['Severity.ID'])
        #
        ,sa.Index('Validation_Result_UK1' ,'Job_Run_ID' ,'Validation_Rule_ID'   ,unique=True)
    )

def downgrade():
    op.drop_table('Validation_Result')
