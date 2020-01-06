"""Create Data Validation Rule Table

Revision ID: d5099e547182
Revises: 9e7613856bdc
Create Date: 2020-01-05 16:00:15.226900
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'd5099e547182'
down_revision = '9e7613856bdc'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     DataAssertionRule(
        ID                       INTEGER             NOT   NULL  CHECK(  ID  >=  0 )   DEFAULT NEXTVAL('DataAssertionRule_Seq')
        ,JobID                    INTEGER             NOT   NULL
        ,ParentRuleID             INTEGER                   NULL
        ,Code                     VARCHAR(64)         NOT   NULL
        ,Name                     VARCHAR(128)        NOT   NULL
        ,StatusID                 INTEGER             NOT   NULL  DEFAULT  2    CHECK(  StatusID                 IN(     0,1,2)      )
        ,ForJobRunStatusID        INTEGER                   NULL                CHECK(  ForJobRunStatusID        IN( NULL ,11,19,31  ))  --  PreChecking, PostChecking, Validating
        ,AssertOrder              INTEGER             NOT   NULL  DEFAULT 32    CHECK(  AssertOrder              BETWEEN 0 AND 10000   )
        ,FrequencyID              INTEGER             NOT   NULL  DEFAULT  3    CHECK(  FrequencyID              IN(     2,3,4,5,6,7,8)) --  2=hourly ,3=daily ,4=weekly ,5=monthly ,6=quarterly ,7=semester ,8=anually
        ,FrequencyValue           INTEGER             NOT   NULL  DEFAULT  1    CHECK(  FrequencyValue           BETWEEN 1 AND 59    )
        ,ThresholdType            CHAR(1)                   NULL  DEFAULT 'P'   CHECK(  ThresholdType            IN( NULL,'A','S','P'))  --  A=Absolute ,S=Stadard Deviation ,P=Percentage
        ,WarningPositiveLimit     FLOAT                     NULL  DEFAULT  0.02 CHECK(  WarningPositiveLimit     IS  NULL  OR  WarningPositiveLimit  >=0)  --  +2%
        ,WarningNegativeLimit     FLOAT                     NULL  DEFAULT -0.02 CHECK(  WarningNegativeLimit     IS  NULL  OR  WarningNegativeLimit  <=0)  --  -2%
        ,ErrorPositiveLimit       FLOAT                     NULL  DEFAULT  0.05 CHECK(  ErrorPositiveLimit       IS  NULL  OR  ErrorPositiveLimit    >=0)  --  +5%
        ,ErrorNegativeLimit       FLOAT                     NULL  DEFAULT -0.05 CHECK(  ErrorNegativeLimit       IS  NULL  OR  ErrorNegativeLimit    <=0)  --  -5%
        ,FatalPositiveLimit       FLOAT                     NULL  DEFAULT  0.08 CHECK(  FatalPositiveLimit       IS  NULL  OR  FatalPositiveLimit    >=0)  --  +8%
        ,FatalNegativeLimit       FLOAT                     NULL  DEFAULT -0.08 CHECK(  FatalNegativeLimit       IS  NULL  OR  FatalNegativeLimit    <=0)  --  -8%
        ,DataSourceType           CHAR(1)             NOT   NULL  DEFAULT 'P'   CHECK(  DataSourceType           IN('P','I','H','D', 'O','S','R')       )  --  P=Postgres, I=Impala, H=Hive, D=DB2, O=Oracle, S=SQL-Server, R=Presto
        ,DataSourceTypeExpected   CHAR(1)             NOT   NULL  DEFAULT 'P'   CHECK(  DataSourceTypeExpected   IN('P','I','H','D', 'O','S','R')       )  --  P=Postgres, I=Impala, H=Hive, D=DB2, O=Oracle, S=SQL-Server, R=Presto
        ,MetricReturnType         CHAR(1)             NOT   NULL  DEFAULT 'S'   CHECK(  MetricReturnType         IN('S','K')                            )  --  S=Single Value, K = Key/Value (multiple records)
        ,ExpectMetricSQL          TEXT                      NULL
        ,ActualMetricSQL          TEXT                      NULL
--             ,DataColumnID             INTEGER                   NULL
        --
        ,LastValidatedOn          TIMESTAMP
        ,LastFailedOn             TIMESTAMP
        ,LastAlertedOn            TIMESTAMP
        --
        ,Updated_On               TIMESTAMP           NOT   NULL  DEFAULT  CURRENT_TIMESTAMP
)
;
ALTER   TABLE       DataAssertionRule
ADD     CONSTRAINT  DataAssertionRule_CPK PRIMARY KEY(  ID  )
;
ALTER   TABLE       DataAssertionRule
ADD     CONSTRAINT  DataAssertionRule_FK2 FOREIGN KEY( StatusID )
         REFERENCES  Status(  ID  )
;
ALTER   TABLE       DataAssertionRule
ADD     CONSTRAINT  DataAssertionRule_FK3 FOREIGN KEY(  FrequencyID   )
        REFERENCES  Frequency(  ID  )
;
ALTER   TABLE       DataAssertionRule
ADD     CONSTRAINT  DataAssertionRule_FK1 FOREIGN KEY(  JobID         )
        REFERENCES  Job(  ID  )
        ON  DELETE  CASCADE
;

CREATE UNIQUE INDEX DataAssertionRule_UK1 ON  DataAssertionRule(  JobID ,AssertOrder  )
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
