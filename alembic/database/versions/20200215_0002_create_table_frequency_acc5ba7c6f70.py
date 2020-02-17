"""Create Table Frequency

Revision ID: acc5ba7c6f70
Revises: 
Create Date: 2020-02-15 15:40:40.399071
"""
# pylint: disable=maybe-no-member

from   alembic import op
from   sqlalchemy.sql import table, column, func
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'acc5ba7c6f70'
down_revision = None
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
        'Frequency'
        ,sa.Column('ID'     ,sa.SmallInteger,nullable=False ,comment='The Primary Key'  ,primary_key=True )
        ,sa.Column('Name'   ,sa.String(8)   ,nullable=False ,comment='Name of the frequency')
        ,sa.Column('Minutes',sa.Integer     ,nullable=False ,comment='The number of minutes for this frequency')
        ,dt_updated_on
        ,sa.CheckConstraint( 'ID BETWEEN 0 AND 8'   ,name='ID')
        ,sa.UniqueConstraint('Name'                 ,name='Frequency_UK1')
        #
        ,sa.Index('Frequency_UK1' ,'Name' ,unique=True)
    )

    _table = table(
        'Frequency'
        ,column('ID'        ,sa.SmallInteger)
        ,column('Name'      ,sa.String())
        ,column('Minutes'   ,sa.Integer)
    )
 
    op.bulk_insert(
        _table
        ,[   {'ID': 0 ,'Name': 'Manual'   ,'Minutes': 0    }
            ,{'ID': 1 ,'Name': 'Minute'   ,'Minutes': 1    }
            ,{'ID': 2 ,'Name': 'Hour'     ,'Minutes': 60   }
            ,{'ID': 3 ,'Name': 'Day'      ,'Minutes': 1440 }
            ,{'ID': 4 ,'Name': 'Week'     ,'Minutes': 10080}
            ,{'ID': 5 ,'Name': 'Month'    ,'Minutes': 43200}
            ,{'ID': 6 ,'Name': 'Quarter'  ,'Minutes': 129600}
            ,{'ID': 7 ,'Name': 'Semester' ,'Minutes': 172800}
            ,{'ID': 8 ,'Name': 'Annual'   ,'Minutes': 525600}
        ]
    )

def downgrade():
    op.drop_table('Frequency')
