"""Create Table Validation Rule

Revision ID: 3652e714353c
Revises: dea484191ccf
Create Date: 2020-02-15 15:40:48.630197
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '3652e714353c'
down_revision = 'dea484191ccf'
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
        'Validation_Rule'
        ,sa.Column('ID'                 ,sa.SmallInteger,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False )
        ,sa.Column('Parent_ID'          ,sa.SmallInteger,nullable=True  )
        ,sa.Column('Code'               ,sa.String(32)  ,nullable=False )
        ,sa.Column('Description'        ,sa.String(64)  ,nullable=False )
        ,sa.Column('Status_ID'          ,sa.SmallInteger,nullable=False ,server_default='2' )    # Enabled
        ,sa.Column('Assert_Order'       ,sa.SmallInteger,nullable=False ,server_default='1' )    # Enabled
        ,sa.Column('Run_Frequency_ID'   ,sa.SmallInteger,nullable=False ,server_default='3' )   # Daily
        ,sa.Column('Run_Frequency_Value',sa.Integer     ,nullable=False ,server_default='1' )
        ,sa.Column('Threshold_Type'     ,sa.String(1)   ,nullable=True  ,server_default='P' )
        ,sa.Column('Warn_Top_Limit'     ,sa.Float       ,nullable=True  )
        ,sa.Column('Warn_Bot_Limit'     ,sa.Float       ,nullable=True  )
        ,sa.Column('Error_Top_Limit'    ,sa.Float       ,nullable=True  )
        ,sa.Column('Error_Bot_Limit'    ,sa.Float       ,nullable=True  )
        ,sa.Column('Fatal_Top_Limit'    ,sa.Float       ,nullable=True  )
        ,sa.Column('Fatal_Bot_Limit'    ,sa.Float       ,nullable=True  )
        ,sa.Column('Expect_Metric_SQL'  ,sa.String      ,nullable=True  )
        ,sa.Column('Actual_Metric_SQL'  ,sa.String      ,nullable=True  )
        ,sa.Column('Last_Validated_On'  ,sa.DateTime(timezone=True) ,nullable=True  )
        ,sa.Column('Last_Failed_On'     ,sa.DateTime(timezone=True) ,nullable=True  )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'                  ,name='ID')
        ,sa.CheckConstraint( 'Length( Code ) <= 32'     ,name='Code')
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Parent_ID']  ,['Validation_Rule.ID'])
        ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID'])
        ,sa.ForeignKeyConstraint(['Run_Frequency_ID'] ,['Frequency.ID'])
        #
        ,sa.Index('Validatino_Rule_UK1' ,'Code' ,unique=True)
    )

def downgrade():
    op.drop_table('Validation_Rule')
