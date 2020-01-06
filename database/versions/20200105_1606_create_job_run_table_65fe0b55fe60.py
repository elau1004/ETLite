"""Create Job Run Table

Revision ID: 65fe0b55fe60
Revises: f5e03b54e402
Create Date: 2020-01-05 15:59:57.969635
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '65fe0b55fe60'
down_revision = 'f5e03b54e402'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE     JobRun(
         ID                     INTEGER     NOT NULL  DEFAULT NEXTVAL('JobRun_Seq') CHECK( ID >= 0 )
        ,JobID                  INTEGER     NOT NULL
        ,BatchNo                INTEGER     NOT NULL              CHECK(  BatchNo   >=  0 )
        ,StatusID               INTEGER     NOT NULL  DEFAULT 3   CHECK(  StatusID  NOT IN(1,2) AND StatusID<= 99 ) --  3=Pending
        --
        ,FileCount              INTEGER
        ,ErrorCount             INTEGER
        ,RejectedCount          INTEGER
        ,ExpectedCount          INTEGER
        ,CopiedInCount          INTEGER       --
        ,FormattedCount         INTEGER
        ,ImportedCount          INTEGER
        --
        ,CopyingInRate          FLOAT         --  Rows per second.  The throughput of copying data from S3.
        ,FormattingRate         FLOAT         --  Rows per second.  The throughput of MapReducing the raw input files.
        ,ImportingRate          FLOAT         --  Rows per second.  The throughput of loading the Impala/Hive tables.
        ,ProfilingRate          FLOAT         --  Rows per second.  The throughput of collecting the data profile aggregates.
        ,ImportingRate          FLOAT         --  Rows per second.  The throughput of importing formatted data into parquet.
        ,ExportingRate          FLOAT         --  Rows per second.  The throughput of exporting data out for other 3rd party system.
        ,CopyingOutRate         FLOAT         --  Rows per second.  The throughput of copying data back to S3.
        --
        ,RunFrom                TIMESTAMP     NOT NULL  DEFAULT     CURRENT_TIMESTAMP
        ,RunUpto                TIMESTAMP
        --
        ,MiscType               VARCHAR(32)
        ,Miscellaneous          VARCHAR(4096)
        ,Updated_On             TIMESTAMP     NOT NULL  DEFAULT     CURRENT_TIMESTAMP
        --
        ,Remark                 VARCHAR(1024)
)
;
ALTER   TABLE       JobRun
ADD     CONSTRAINT  JobRun_PK   PRIMARY KEY(  ID  )
;
ALTER   TABLE       JobRun
ADD     CONSTRAINT  JobRun_FK1  FOREIGN KEY(  JobID         )
        REFERENCES  Job( ID )
        ON  DELETE  CASCADE
;
ALTER   TABLE       JobRun
ADD     CONSTRAINT  JobRun_FK2  FOREIGN KEY(  StatusID      ) REFERENCES  Status( ID )
;
CREATE  UNIQUE  INDEX JobRun_UK1        ON    JobRun( JobID ,BatchNo )
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
