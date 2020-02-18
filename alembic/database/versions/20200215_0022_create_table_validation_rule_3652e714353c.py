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
        ,sa.Column('Code'               ,sa.String(64)  ,nullable=False )
        ,sa.Column('Description'        ,sa.String(128) ,nullable=False )
        ,sa.Column('Status_ID'          ,sa.SmallInteger,nullable=False ,server_default= '2'    )   # Enabled
        ,sa.Column('Assert_Order'       ,sa.SmallInteger,nullable=False ,server_default= '1'    )   # Enabled
        ,sa.Column('Run_Frequency_ID'   ,sa.SmallInteger,server_default= '3'    )   # Daily
        ,sa.Column('Run_Frequency_Value',sa.Integer     ,server_default= '1'    )
        ,sa.Column('Threshold_Type'     ,sa.String(1)   ,server_default= 'P'    )   # A=Absolute ,S=Stadard Deviation ,P=Percentage
        ,sa.Column('Warn_Top_Limit'     ,sa.Float       ,server_default= '0.02' )
        ,sa.Column('Warn_Bot_Limit'     ,sa.Float       ,server_default='-0.02' )
        ,sa.Column('Error_Top_Limit'    ,sa.Float       ,server_default= '0.03' )
        ,sa.Column('Error_Bot_Limit'    ,sa.Float       ,server_default='-0.03' )
        ,sa.Column('Fatal_Top_Limit'    ,sa.Float       ,server_default= '0.05' )
        ,sa.Column('Fatal_Bot_Limit'    ,sa.Float       ,server_default='-0.05' )
        ,sa.Column('Expect_Metric_SQL'  ,sa.Text )
        ,sa.Column('Actual_Metric_SQL'  ,sa.Text )
        ,sa.Column('Last_Validated_On'  ,sa.DateTime(    timezone=True ))
        ,sa.Column('Last_Failed_On'     ,sa.DateTime(    timezone=True ))
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID >= 1'                              ,name='ID'              )
        ,sa.CheckConstraint( 'Assert_Order >= 1'                    ,name='Assert_Order'    )
        ,sa.CheckConstraint( 'Run_Frequency_Value BETWEEN 1 AND 59' ,name='Frequency_Value' )
        ,sa.CheckConstraint( "Threshold_Type IN(NULL,'A','S','P')"  ,name='Threshold_Type'  )
        ,sa.CheckConstraint ('Warn_Top_Limit  >= 0'                 ,name='Warn_Top_Limit'  )
        ,sa.CheckConstraint ('Warn_Bot_Limit  <= 0'                 ,name='Warn_Bot_Limit'  )
        ,sa.CheckConstraint ('Error_Top_Limit >= 0'                 ,name='Error_Top_Limit' )
        ,sa.CheckConstraint ('Error_Bot_Limit <= 0'                 ,name='Error_Bot_Limit' )
        ,sa.CheckConstraint ('Fatal_Top_Limit >= 0'                 ,name='Fatal_Top_Limit' )
        ,sa.CheckConstraint ('Fatal_Bot_Limit <= 0'                 ,name='Fatal_Bot_Limit' )
        #
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Parent_ID']  ,['Validation_Rule.ID'])
        ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID'])
        ,sa.ForeignKeyConstraint(['Run_Frequency_ID'] ,['Frequency.ID'])
        #
        ,sa.Index('Validatino_Rule_UK1' ,'Code' ,unique=True)
    )

def downgrade():
    op.drop_table('Validation_Rule')
