"""Create Table Data Vendor

Revision ID: 444326c53f71
Revises: ebc75428d24b
Create Date: 2020-02-15 15:40:42.936610
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '444326c53f71'
down_revision = 'ebc75428d24b'
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
        'Data_Vendor'
        ,sa.Column('ID'         ,sa.Integer     ,nullable=False ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Code'       ,sa.String(8)   ,nullable=False )
        ,sa.Column('Status_ID'  ,sa.SmallInteger,nullable=False ,server_default='2')    # Enabled
        ,sa.Column('Name'       ,sa.String(128) ,nullable=False )
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 32767'   ,name='ID')
        ,sa.CheckConstraint( 'Status_ID BETWEEN 1 AND 2',name='Status_ID')
        ,sa.CheckConstraint( 'Length( Code )<=8'        ,name='Code')
        ,sa.ForeignKeyConstraint(['Status_ID']  ,['Status.ID']  )
        #
        ,sa.Index('Data_Vendor_UK1' ,'Code' ,unique=True)
        #
        ,sqlite_autoincrement=True
    )


def downgrade():
    op.drop_table('Data_Vendor')
