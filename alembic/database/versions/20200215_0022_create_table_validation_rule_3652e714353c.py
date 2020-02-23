"""Create Table Validation Rule

Revision ID: 3652e714353c
Revises: dea484191ccf
Create Date: 2020-02-15 15:40:48.630197
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '3652e714353c'
down_revision = 'dea484191ccf'
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
        'Validation_Rule'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Code'               ,sa.String(64)  ,nullable=False )
        ,sa.Column('Parent_ID'          ,sa.SmallInteger,nullable=True  ,comment='The parent rule that is tpo be inherited down to this row.')
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Status_ID'          ,sa.SmallInteger,nullable=False ,server_default= '2'    )   # Enabled
        ,sa.Column('Description'        ,sa.String(128) ,nullable=False )
        ,sa.Column('Assert_Order'       ,sa.SmallInteger,nullable=False ,server_default= '1'    )   # Enabled
        ,sa.Column('Run_Frequency_ID'   ,sa.SmallInteger,nullable=False ,server_default='3'     ,comment='The frequency to validate this data set.')   # Daily
        ,sa.Column('Frequency_Interval' ,sa.Integer     ,nullable=False ,server_default='1'     ,comment='The frequency interval to validate this data set.' )
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
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 32767'               ,name='ID')
        ,sa.CheckConstraint( 'Assert_Order >= 1'                    ,name='Assert_Order'    )
        ,sa.CheckConstraint( 'Frequency_Interval BETWEEN 1 AND 59'  ,name='Frequency_Value' )
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
        ,sa.Index('Validation_Rule_UK1' ,'Code' ,unique=True)
        #
        ,sqlite_autoincrement=True
    )

    sql_view  = """
CREATE  VIEW    Validation_Rule_View
AS
SELECT  vr.ID
       ,vr.Code
       ,vr.Parent_ID
       ,pr.Code             AS  Parent_Code
       ,vr.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,vr.Status_ID
       ,st.Name             AS  Status_Name
       ,vr.Description
       ,vr.Assert_Order
       ,vr.Run_Frequency_ID
       ,hz.Name             AS  Frequency_Name
       ,vr.Frequency_Interval
       ,vr.Threshold_Type
       ,vr.Warn_Top_Limit
       ,vr.Warn_Bot_Limit
       ,vr.Error_Top_Limit
       ,vr.Error_Bot_Limit
       ,vr.Fatal_Top_Limit
       ,vr.Fatal_Bot_Limit
       ,vr.Expect_Metric_SQL
       ,vr.Actual_Metric_SQL
       ,vr.Last_Validated_On
       ,vr.Last_Failed_On
       ,vr.Updated_On
FROM    Validation_Rule     AS  vr
LEFT    OUTER
JOIN    Validation_Rule     AS  pr  ON  pr.ID   =   ds.Parent_ID
JOIN    Data_Set            As  ds  ON  ds.ID   =   vr.Data_Set_ID
JOIN    Status              AS  st  ON  st.ID   =   vr.Status_ID
JOIN    Frequency           AS  hz  ON  hz.ID   =   vr.Run_Frequency_ID
"""
    with engine.connect() as conn:
        conn.execute( sql_view )


def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Validation_Rule_View" )

    op.drop_table('Validation_Rule')
