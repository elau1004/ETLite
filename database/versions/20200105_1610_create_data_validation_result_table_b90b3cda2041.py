"""Create Data Validation Result Table

Revision ID: b90b3cda2041
Revises: d5099e547182
Create Date: 2020-01-05 16:02:45.187705
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'b90b3cda2041'
down_revision = 'd5099e547182'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     DataAssertionResult(
        ID                    INTEGER             NOT   NULL  CHECK(  ID  >=  0 )   DEFAULT NEXTVAL('DataAssertionResult_Seq')
        ,JobRunID              INTEGER             NOT   NULL
        ,AssertionRuleID       INTEGER             NOT   NULL
        ,KeyValue              VARCHAR(100)              NULL
        ,ExpectValue           FLOAT               NOT   NULL
        ,ActualValue           FLOAT               NOT   NULL
        --  Instance Values
        ,ThresholdType         CHAR(1)             NOT   NULL  CHECK(  ThresholdType IN('A','S','P') ) --  A=Absolute ,S=Stadard Deviation ,P=Percentage
        ,WarningPositiveLimit  FLOAT                     NULL
        ,WarningNegativeLimit  FLOAT                     NULL
        ,ErrorPositiveLimit    FLOAT                     NULL
        ,ErrorNegativeLimit    FLOAT                     NULL
        ,FatalPositiveLimit    FLOAT                     NULL
        ,FatalNegativeLimit    FLOAT                     NULL
        ,ExpectMetricSQL       TEXT                      NULL
        ,ActualMetricSQL       TEXT                      NULL
        --
        ,CreatedOn             TIMESTAMP           NOT   NULL  DEFAULT CURRENT_TIMESTAMP
        ,Updated_On            TIMESTAMP           NOT   NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE       DataAssertionResult
ADD     CONSTRAINT  DataAssertionResult_CPK PRIMARY KEY(  ID  )
;
ALTER   TABLE       DataAssertionResult
ADD     CONSTRAINT  DataAssertionResult_FK1 FOREIGN KEY(  JobRunID  )
        REFERENCES  JobRun( ID )
        ON  DELETE  CASCADE
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
