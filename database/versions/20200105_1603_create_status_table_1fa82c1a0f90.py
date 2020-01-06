"""Create Status Table

Revision ID: 1fa82c1a0f90
Revises: 
Create Date: 2020-01-05 15:59:00.821757
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '1fa82c1a0f90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
CREATE  TABLE   Status(
         ID             INTEGER       NOT NULL  CHECK(  ID  BETWEEN 0 AND 99)
        ,Name           VARCHAR(16)   NOT NULL
        ,isTerminal     BOOLEAN       NOT NULL  DEFAULT FALSE
        --
        ,Updated_On     TIMESTAMP     NOT NULL  DEFAULT CURRENT_TIMESTAMP
)
;
ALTER   TABLE         Status
ADD     CONSTRAINT    Status_CPK  PRIMARY KEY (  ID  )
;

INSERT  INTO
Status( ID  , Names )
SELECT  0   ,'Errored'          UNION ALL --  
SELECT  1   ,'Disabled'         UNION ALL --  
SELECT  2   ,'Enabled'          UNION ALL --  
SELECT  3   ,'Pending'          UNION ALL --  
SELECT  4   ,'Cancelled'        UNION ALL --  
SELECT  5   ,'Completing'       UNION ALL
SELECT  6   ,'Completed'        UNION ALL
--  Extraction phase
SELECT  11  ,'Authenticating'   UNION ALL -- 
SELECT  12  ,'Authenticated'    UNION ALL -- 
SELECT  13  ,'Requesting'       UNION ALL -- 
SELECT  14  ,'Requested'        UNION ALL -- 
SELECT  15  ,'Checking'         UNION ALL -- 
SELECT  16  ,'Checked'          UNION ALL -- 
SELECT  17  ,'Paginating'       UNION ALL -- 
SELECT  18  ,'Paginated'        UNION ALL -- 
SELECT  19  ,'Querying'         UNION ALL --  
SELECT  20  ,'Queried'          UNION ALL --  
SELECT  21  ,'Staging'          UNION ALL --  
SELECT  22  ,'Staged'           UNION ALL --  
SELECT  23  ,'Formatting'       UNION ALL --  
SELECT  24  ,'Formatted'        UNION ALL --  
--  Ingestion phase     
SELECT  31  ,'Importing'        UNION ALL --  
SELECT  32  ,'Imported'         UNION ALL --  
SELECT  33  ,'Profiling'        UNION ALL --  
SELECT  34  ,'Profiled'         UNION ALL --  
SELECT  35  ,'Completing'       UNION ALL --  
SELECT  36  ,'Completed'        UNION ALL --  
--  Certification phase
SELECT  41  ,'Validating'       UNION ALL --  
SELECT  42  ,'Validated'        UNION ALL --  
SELECT  43  ,'Failing'          UNION ALL --  
SELECT  44  ,'Failed'           UNION ALL --  
;
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
