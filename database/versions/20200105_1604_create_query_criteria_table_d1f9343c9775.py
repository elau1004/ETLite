"""Create Query Criteria Table

Revision ID: d1f9343c9775
Revises: 9f7803a28010
Create Date: 2020-01-05 15:59:43.377411
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'd1f9343c9775'
down_revision = '9f7803a28010'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     Query_Criteria(
        ID              INTEGER       NOT NULL  DEFAULT NEXTVAL('QueryCriteria_Seq')  CHECK( ID >= 0 )
        ,KeyName        VARCHAR(64)   NOT NULL
        ,SubKey         VARCHAR(128)      NULL
        ,Type           CHAR(1)       NOT NULL            CHECK(  Type      IN('E','I') ) --  E=Exclude, I=Include
        ,StatusID       INTEGER       NOT NULL  DEFAULT 2 CHECK(  StatusID  IN( 1 , 2 ) ) --  1=Disable, 2=Enabled
        ,EntityID       INTEGER
        ,ValueInt       BIGINT
        ,ValueStr       VARCHAR(1024)
        ,ValueDtTm      TIMESTAMP
        ,ValueReal      REAL
        --
        ,Updated_On     TIMESTAMP     NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE         Query_Criteria
ADD     CONSTRAINT    Query_Criteria_CPK  PRIMARY KEY( ID )
;
ALTER   TABLE         Query_Criteria
ADD     CONSTRAINT    Query_Criteria_FK1  FOREIGN KEY( StatusID ) REFERENCES  Status( ID )
;
CREATE  UNIQUE  INDEX Query_Criteria_UK1  ON  Query_Criteria(  KeyName, SubKey, Type   ,ValueInt ,ValueStr ,ValueDtTm, ValueReal  )
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
