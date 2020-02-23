"""Create Table Validation Result

Revision ID: 99bc72a4d986
Revises: 3652e714353c
Create Date: 2020-02-15 15:40:49.517711
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '99bc72a4d986'
down_revision = '3652e714353c'
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
        'Validation_Result'
        ,sa.Column('ID'                 ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Validation_Rule_ID' ,sa.SmallInteger,nullable=False ,comment='Foreign Key to the Validation Rule table.')
        ,sa.Column('Job_Run_ID'         ,sa.Integer     ,nullable=False ,comment='Foreign key to the Job Run table.')
        ,sa.Column('Data_Set_ID'        ,sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Severity_ID'        ,sa.SmallInteger,nullable=False ,server_default='4' )   # Info
        ,sa.Column('Expect_Int'         ,sa.BigInteger  )
        ,sa.Column('Actual_Int'         ,sa.BigInteger  )
        ,sa.Column('Expect_Flt'         ,sa.Float( 53 ) )
        ,sa.Column('Actual_Flt'         ,sa.Float( 53 ) )
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
        #
        ,sqlite_autoincrement=True
    )

    sql_view  = """
CREATE  VIEW    Validation_Result_View
AS
SELECT  vs.ID
       ,vs.Validation_Rule_ID
       ,vr.Code             AS  Validation_Rule_Code
       ,vs.Job_Run_ID
       ,jr.Run_No           AS  Job_Run_No
       ,vs.Data_Set_ID
       ,ds.Code             AS  Data_Set_Code
       ,vs.Severity_ID
       ,sv.Name             AS  Severity_Name
       ,vs.Expect_Int
       ,vs.Actual_Int
       ,vs.Expect_Flt
       ,vs.Actual_Flt
       ,vs.Expect_Dtm
       ,vs.Actual_Dtm
       ,vs.Updated_On
FROM    Validation_Result   AS  vs
JOIN    Data_Set            AS  ds  ON  ds.ID   =   vs.Data_Set_ID
JOIN    Job_Run             AS  jr  ON  jr.ID   =   vs.Job_Run_ID
JOIN    Severity            AS  sv  ON  sv.ID   =   vs.Severity_ID
JOIN    Validation_Rule     AS  vr  ON  vr.ID   =   vs.Validation_Rule_ID
"""
    with engine.connect() as conn:
        conn.execute( sql_view )


def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Validation_Result_View" )

    op.drop_table('Validation_Result')
