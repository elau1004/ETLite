"""Create Table Job Run Metric

Revision ID: 8da2a5812ba2
Revises: f540cc84a360
Create Date: 2020-02-15 15:40:45.962656
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '8da2a5812ba2'
down_revision = 'f540cc84a360'
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
        'Job_Run_Metric'
        ,sa.Column('ID'         ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Job_Run_ID' ,sa.Integer     ,nullable=False ,comment='Foreign key to the Job Run table..')
        ,sa.Column('Data_Set_ID',sa.SmallInteger,nullable=False ,comment='Denormalized column for querying.')
        ,sa.Column('Stats'      ,sa.JSON        ,nullable=False ,comment='A generic json to capture addition metrics.')
        ,dt_updated_on
        #
        ,sa.CheckConstraint(    'ID >= 1'       ,name='ID')
        #
        ,sa.ForeignKeyConstraint(['Job_Run_ID'] ,['Job_Run.ID'])
        ,sa.ForeignKeyConstraint(['Data_Set_ID'],['Data_Set.ID'])
        #
        ,sa.Index('Job_Run_Metric_UK1'  ,'Job_Run_ID'   ,unique=True)
        ,sa.Index('Job_Run_Metric_K1'   ,'Data_Set_ID'  ,unique=False)
    )

def downgrade():
    op.drop_table('Job_Run_Metric')
