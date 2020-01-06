"""Create Job Run Data Profile Table

Revision ID: 9e7613856bdc
Revises: 65fe0b55fe60
Create Date: 2020-01-05 16:00:08.414296
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '9e7613856bdc'
down_revision = '65fe0b55fe60'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     JobRunDataAgg(
         ID                    BIGINT              NOT NULL  DEFAULT NEXTVAL('JobRunDataAgg_Seq')
        ,JobRunID              INTEGER             NOT NULL
        ,ProfileID             INTEGER                 NULL  DEFAULT 0
        ,KeyName               VARCHAR(64)             NULL
        ,SubKey                VARCHAR(128)            NULL
        ,DataColumnID          INTEGER                 NULL
--      ,SeverityID            INTEGER                 NULL  CHECK(  SeverityID  IN( NULL, 3, 4, 5, 7 )) --  3=Critical, 4=Error, 5=Warning, 7=Information
        ,Counts                BIGINT              NOT NULL
        ,Blanks                BIGINT              NOT NULL
        ,Distincts             BIGINT
        ,IntMedian             BIGINT
        ,IntAverage            BIGINT
        ,IntStdDev             BIGINT
        ,IntMinimum            BIGINT
        ,IntMaximum            BIGINT
        ,SLnMedian             INTEGER
        ,SLnAverage            INTEGER
        ,SLnStdDev             INTEGER
        ,SLnMinimum            INTEGER
        ,SLnMaximum            INTEGER
        ,DtmMedian             TIMESTAMP
        ,DtmAverage            TIMESTAMP
        ,DayStdDev             INTEGER
        ,DtmMinimum            TIMESTAMP
        ,DtmMaximum            TIMESTAMP
        --
        ,Updated_On            TIMESTAMP           NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE       JobRunDataAgg
ADD     CONSTRAINT  JobRunDataAgg_CPK PRIMARY KEY( ID )
;
ALTER   TABLE       JobRunDataAgg
ADD     CONSTRAINT  JobRunDataAgg_FK1 FOREIGN KEY( JobRunID )
        REFERENCES  JobRun( ID )
        ON  DELETE  CASCADE
;
CREATE  INDEX       JobRunDataAgg_K1  ON    JobRunDataAgg( JobRunID ,ProfileID )
;

CREATE  TABLE     JobRunDataDist(
         ID                    BIGINT              NOT NULL  DEFAULT NEXTVAL('JobRunDataDist_Seq')
        ,JobRunID              INTEGER             NOT NULL
        ,ProfileID             INTEGER                 NULL  DEFAULT 0
        ,KeyName               VARCHAR(64)             NULL
        ,SubKey                VARCHAR(128)            NULL
        ,DataColumnID          INTEGER                 NULL
        ,Counts                BIGINT              NOT NULL
        ,ValueInt              BIGINT
        ,ValueStr              VARCHAR(1024)
        ,ValueDtTm             TIMESTAMP
        ,ValueReal             REAL
        --
        ,Updated_On            TIMESTAMP           NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE       JobRunDataDist
ADD     CONSTRAINT  JobRunDataDist_CPK  PRIMARY KEY(  ID  )
;
ALTER   TABLE       JobRunDataDist
ADD     CONSTRAINT  JobRunDataDist_FK1  FOREIGN KEY( JobRunID )
        REFERENCES  JobRun( ID )
        ON  DELETE  CASCADE
;
CREATE  INDEX       JobRunDataDist_K1   ON  JobRunDataDist( JobRunID  )
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
