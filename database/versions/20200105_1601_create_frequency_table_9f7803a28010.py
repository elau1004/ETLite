"""Create Frequency Table

Revision ID: 9f7803a28010
Revises: d57a7a482f48
Create Date: 2020-01-05 15:59:35.148784
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '9f7803a28010'
down_revision = 'd57a7a482f48'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE   Frequency(
         ID                 INTEGER       NOT NULL  CHECK(  ID  BETWEEN 0 AND 8 )
        ,Name               VARCHAR(8)    NOT NULL
        ,Duration_Minutes   INTEGER       NOT NULL
        --
        ,Updated_On         TIMESTAMP     NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;

ALTER   TABLE         Frequency
ADD     CONSTRAINT    Frequency_CPK PRIMARY KEY (  ID  )
;

INSERT    INTO
Frequency(ID    ,Name       ,Duration_Minutes )
SELECT    0     ,'Manual'   ,0              UNION ALL
SELECT    1     ,'Minute'   ,1              UNION ALL
SELECT    2     ,'Hour'     ,60             UNION ALL
SELECT    3     ,'Day'      ,60*24          UNION ALL
SELECT    4     ,'Week'     ,60*24*7        UNION ALL
SELECT    5     ,'Month'    ,60*24*30       UNION ALL
SELECT    6     ,'Quarter'  ,60*24*30*3     UNION ALL
SELECT    7     ,'Semester' ,60*24*30*4     UNION ALL
SELECT    8     ,'Annual'   ,60*24*365
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
