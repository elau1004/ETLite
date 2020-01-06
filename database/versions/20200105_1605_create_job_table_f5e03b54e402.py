"""Create Job Table

Revision ID: f5e03b54e402
Revises: d1f9343c9775
Create Date: 2020-01-05 15:59:51.491036
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = 'f5e03b54e402'
down_revision = 'd1f9343c9775'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     Job(
         ID                     INTEGER       NOT NULL  CHECK(  ID  >=10  )
        ,Code                   VARCHAR(32)   NOT NULL
        ,Description            VARCHAR(128)  NOT NULL
        ,ParentJobID            INTEGER
        ,StatusID               INTEGER       NOT NULL  DEFAULT 2           CHECK(  StatusID              IN(0,1,2,3)     ) --  Staging is a transient status that data set is not completely processed.
        ,SourceEntity           VARCHAR(128)      NULL
        ,TargetEntity           VARCHAR(128)      NULL
        ,NextBatchNo            INTEGER       NOT NULL  DEFAULT 101         CHECK(  NextBatchNo           >  0            )
        ,WorkInProgress         BOOLEAN       NOT NULL  DEFAULT FALSE   --  CHECK(  WorkInProgress        IN(0,1)         ) --  0=No ,1=Yes
        ,LockTimeOutAfter       INTEGER       NOT NULL  DEFAULT 59          CHECK(  LockTimeOutAfter      >  0            )
        ,RunFrequencyID         INTEGER       NOT NULL  DEFAULT 3       --  Daily
        ,RunFrequencyValue      INTEGER       NOT NULL  DEFAULT 1           CHECK(  RunFrequencyValue     >  0            )
        ,RanOn                  TIMESTAMP
        --
        ,UptoErroredJobRunID    INTEGER                                     CHECK(  UptoErroredJobRunID   IS  NULL  OR  UptoErroredJobRunID   > 0 )
        ,UptoVerifiedJobRunID   INTEGER                                     CHECK(  UptoVerifiedJobRunID  IS  NULL  OR  UptoVerifiedJobRunID  > 0 )
        ,AvgDurationMin         INTEGER                                     CHECK(  AvgDurationMin        IS  NULL  OR  AvgDurationMin        > 0 )
        ,Remark                 VARCHAR(1024)
        --
        ,Updated_On             TIMESTAMP     NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE         Job
ADD     CONSTRAINT    Job_CPK   PRIMARY KEY( ID )
;
ALTER   TABLE         Job
ADD     CONSTRAINT    Job_FK1   FOREIGN KEY( StatusID       ) REFERENCES  Status(   ID )
;
ALTER   TABLE         Job
ADD     CONSTRAINT    Job_FK2   FOREIGN KEY( RunFrequencyID ) REFERENCES  Frequency(ID )
;
CREATE  UNIQUE  INDEX Job_UK1   ON  Job(  UPPER( Code ))
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
