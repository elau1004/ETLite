"""Create Job Run Import File Table

Revision ID: 994671298367
Revises: b90b3cda2041
Create Date: 2020-01-05 16:14:11.555251
"""

from   alembic import op
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '994671298367'
down_revision = 'b90b3cda2041'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Implement your DB object creation.
    """
         ID                     INTEGER     NOT NULL  DEFAULT NEXTVAL('JobRun_Seq') CHECK( ID >= 0 )
        ,JobRunID               INTEGER     NOT NULL
        ,BatchNo                INTEGER     NOT NULL              CHECK(  BatchNo   >=  0 )
        ,StatusID               INTEGER     NOT NULL  DEFAULT 3   CHECK(  StatusID  NOT IN(1,2) AND StatusID<= 99 ) --  3=Pending
        ,Path                   VARCHAR(128)
        ,MD5                    VARBINARY(16)
        ,Count                  INTEGER
        ,Remark                 VARCHAR(1024)
        --
        ,Updated_On             TIMESTAMP     NOT NULL  DEFAULT CURRENT_TIMESTAMP
    """
    pass


def downgrade():
    # TODO: Implement your DB object destruction.
    pass
