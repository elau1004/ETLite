"""Create Table Data Set Profile

Revision ID: 0f5887fb18e4
Revises: 8da2a5812ba2
Create Date: 2020-02-15 15:40:46.850170
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '0f5887fb18e4'
down_revision = '8da2a5812ba2'
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
        'Data_Set_Profile'
        ,sa.Column('ID'             ,sa.Integer     ,nullable=False ,autoincrement=101 ,primary_key=True)
        ,sa.Column('Data_Set_ID'    ,sa.SmallInteger,nullable=False )
        ,sa.Column('Field_Seq'      ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('Field_Name'     ,sa.String(64)  ,nullable=False )
        ,sa.Column('Data_Type'      ,sa.String(32)  ,nullable=False )
        ,sa.Column('Status_ID'      ,sa.SmallInteger,nullable=False ,server_default='2' )   # Enabled
        ,sa.Column('do_Count'       ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('do_Distinct'    ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('do_Null'        ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('do_Average'     ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('do_Median'      ,sa.SmallInteger,nullable=False ,server_default='0' )
        ,sa.Column('do_Minimum'     ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('do_Maximum'     ,sa.SmallInteger,nullable=False ,server_default='1' )
        ,sa.Column('do_Length'      ,sa.SmallInteger,nullable=False ,server_default='0' )
        ,sa.Column('do_Sum'         ,sa.SmallInteger,nullable=False ,server_default='0' )
        ,dt_updated_on
        #
        ,sa.CheckConstraint(    'ID >= 1'                       ,name='ID'  )
        ,sa.CheckConstraint(    'Field_Seq BETWEEN 1 AND 255'   ,name='Field_Seq' )
        ,sa.CheckConstraint(    'Status_ID BETWEEN 1 AND 2'     ,name='Status_ID' )
        ,sa.UniqueConstraint(   'Data_Set_ID'     , 'Field_Seq' )
        ,sa.UniqueConstraint(   'Data_Set_ID'     , 'Field_Name')
        ,sa.ForeignKeyConstraint(['Data_Set_ID']  ,['Data_Set.ID']  )
        # Not creating indices for this small table.
    )

def downgrade():
    op.drop_table('Data_Set_Profile')
