"""Create Severity Table

Revision ID: d57a7a482f48
Revises: 1fa82c1a0f90
Create Date: 2020-01-05 15:59:22.892596
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'd57a7a482f48'
down_revision = '1fa82c1a0f90'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     Severity(
         ID             INTEGER       NOT NULL  CHECK(  ID  BETWEEN 1 AND 5 )
        ,Name           VARCHAR(16)   NOT NULL
        ,Description    VARCHAR(128)  NOT NULL
        ,Updated_On     TIMESTAMP     NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE         Severity
ADD     CONSTRAINT    Severity_CPK  PRIMARY KEY (  ID  )
;

INSERT    INTO
Severity( ID  ,Name             ,Description  )
SELECT    1   ,'Critical'       ,'Functionality is affected.'                                     UNION ALL
SELECT    2   ,'Error'          ,'An error condition exists and functionality could be affected.' UNION ALL
SELECT    3   ,'Warning'        ,'Functionality could be affected.'                               UNION ALL
SELECT    4   ,'Information'    ,'General information about system operations.'                   UNION ALL
SELECT    5   ,'Debug'          ,'Debugging trace.'                                               
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
