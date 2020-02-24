"""Create Table Data Set

Revision ID: 7a670e1241eb
Revises: 444326c53f71
Create Date: 2020-02-15 15:40:43.684121
"""
# pylint: disable=maybe-no-member

from   alembic import context
from   alembic import op
from   sqlalchemy.sql import table, column, func
from   sqlalchemy     import create_engine
import sqlalchemy  as sa


# revision identifiers, used by Alembic.
revision = '7a670e1241eb'
down_revision = '444326c53f71'
branch_labels = None
depends_on = None


config = context.config
engine = create_engine( config.get_main_option("sqlalchemy.url") )

dt_updated_on = sa.Column(
                    'Updated_On'
                    ,sa.DateTime(timezone=True)
                    ,nullable=False
                    ,server_default=func.current_timestamp()
                    ,comment='The audit timestamp when this row was last updated'
                )

def upgrade():
    op.create_table(
        'Data_Set'
        ,sa.Column('ID'                 ,sa.Integer     ,primary_key=True ,autoincrement=101 ,mssql_identity_start=101 )
        ,sa.Column('Code'               ,sa.String(8)                                           ,comment='An unique nmemonic to identify a row.')
        ,sa.Column('Parent_ID'          ,sa.SmallInteger                                        ,comment='The parent container that this row is grouped under.')
        ,sa.Column('Status_ID'          ,sa.SmallInteger,server_default='2')    # Enabled
        ,sa.Column('Data_Vendor_ID'     ,sa.SmallInteger,nullable=False )
        ,sa.Column('Description'        ,sa.String(128)                                         ,comment='A descriptive explaination of the data set.')
        ,sa.Column('Exec_Sequence'      ,sa.SmallInteger,nullable=False ,server_default='1'     ,comment='The order to execute the ETL job for this data set.')
        ,sa.Column('Run_Frequency_ID'   ,sa.SmallInteger,nullable=False ,server_default='3'     ,comment='The frequency to process this data set.')   # Daily
        ,sa.Column('Frequency_Interval' ,sa.Integer     ,nullable=False ,server_default='1'     ,comment='The frequency interval to process this data set.' )
        ,sa.Column('Data_From'          ,sa.DateTime(    timezone=True )                        ,comment='The incremental starting date/time for the last successful ETL execution.')
        ,sa.Column('Data_Upto'          ,sa.DateTime(    timezone=True )                        ,comment='The incremental ending date/time (not inclusive) the last successful ETL execution.')
        ,sa.Column('Last_Ran_From'      ,sa.DateTime(    timezone=True )                        ,comment='The UTC datetime the ETL job last started on.')
        ,sa.Column('Last_Ran_Upto'      ,sa.DateTime(    timezone=True )                        ,comment='The UTC datetime the ETL job last ended on')
        ,sa.Column('Work_in_Progress'   ,sa.Boolean(name='Work_in_Progress') ,nullable=False    ,server_default='0'
                                                                                                ,comment='A falg to indicate is a job for this data set is currently executing.')
        ,sa.Column('Lock_Expire_After'  ,sa.SmallInteger,nullable=False ,server_default='60'    ,comment='A time out duration to expire a lock job.')   # 1 hours.
        ,sa.Column('Source_URI'         ,sa.String(128)                                         ,comment='The source of the dataset to extract from.')
        ,sa.Column('Stage_URI'          ,sa.String(128)                                         ,comment='The temporary staging area/file for the extracted dataset.')
        ,sa.Column('Stage_View'         ,sa.String(64)                                          ,comment='The view to query the data from the staging area to be persisted into the target destination.')
        ,sa.Column('Target_URI'         ,sa.String(128)                                         ,comment='The target destination for the transformed data from the source.')
        ,sa.Column('Next_Run_No'        ,sa.Integer     ,nullable=False ,server_default='101'   ,comment='A grouping/batch number to group all the records together for the next job run.')
        ,sa.Column('Profiled_to_Run_No' ,sa.Integer                                             ,comment='An optimization hint to profile the data set from this point onwards.')
        ,sa.Column('Verified_to_Run_No' ,sa.Integer                                             ,comment='An optimization hint to verify  the data set from this point onwards.')
        ,sa.Column('Average_Duration'   ,sa.Integer                                             ,comment='An average duration for quick reference without re-aggregating it.')
        ,sa.Column('OnError_Contact'    ,sa.String(128)                                         ,comment='Notify this list if job failed.')
        ,sa.Column('OnSuccess_Contact'  ,sa.String(128)                                         ,comment='Notify this list if job completed succussfully.')
        ,sa.Column('Remark'             ,sa.String                                              ,comment='General remark.')
        ,dt_updated_on
        #
        ,sa.CheckConstraint( 'ID BETWEEN 1 AND 32767'               ,name='ID')
        ,sa.CheckConstraint( 'Status_ID BETWEEN 1 AND 2'            ,name='Status_ID'  )
        ,sa.CheckConstraint( 'Exec_Sequence BETWEEN 1 AND 255'      ,name='Exec_Sequence')
        ,sa.CheckConstraint( 'Length( Code ) <= 8'                  ,name='Code')
        ,sa.CheckConstraint( 'Frequency_Interval BETWEEN 1 AND 59'  ,name='Frequency_Value')
        ,sa.CheckConstraint( 'Lock_Expire_After > 0'                ,name='Lock_Expire_After')
        #
        ,sa.ForeignKeyConstraint(['Status_ID']          ,['Status.ID']  )
        ,sa.ForeignKeyConstraint(['Parent_ID']          ,['Data_Set.ID'])
        ,sa.ForeignKeyConstraint(['Data_Vendor_ID']     ,['Data_Vendor.ID'] ,ondelete='CASCADE')
        ,sa.ForeignKeyConstraint(['Run_Frequency_ID']   ,['Frequency.ID'])
        #
        ,sa.Index('Data_Set_UK1' ,'Code'    ,unique=True)
        #
        ,sqlite_autoincrement=True
    )

    sql_view  = """
CREATE  VIEW    Data_Set_View
AS
SELECT  ds.ID
       ,ds.Code
       ,ds.Parent_ID
       ,pr.Code             AS  Parent_Code
       ,ds.Status_ID
       ,st.Name             AS  Status_Name
       ,ds.Data_Vendor_ID
       ,dv.Code             AS  Vendor_Code
       ,ds.Description
       ,pr.Description      AS  ParentDesc
       ,ds.Exec_Sequence
       ,ds.Run_Frequency_ID
       ,hz.Name             AS  Frequency_Name
       ,ds.Frequency_Interval
       ,ds.Data_From
       ,ds.Data_Upto
       ,ds.Last_Ran_From
       ,ds.Last_Ran_Upto
       ,ds.Work_in_Progress
       ,ds.Lock_Expire_After
       ,ds.Source_URI
       ,ds.Stage_URI
       ,ds.Stage_View
       ,ds.Target_URI
       ,ds.Next_Run_No
       ,ds.Profiled_to_Run_No
       ,ds.Verified_to_Run_No
       ,ds.Average_Duration
       ,ds.OnError_Contact
       ,ds.OnSuccess_Contact
       ,ds.Remark
       ,ds.Updated_On
FROM    Data_Set    AS  ds
LEFT    OUTER
JOIN    Data_Set    AS  pr  ON  pr.ID   =   ds.Parent_ID
JOIN    Data_Vendor AS  dv  ON  dv.ID   =   ds.Data_Vendor_ID
JOIN    Frequency   AS  hz  ON  hz.ID   =   ds.Run_Frequency_ID
JOIN    Status      AS  st  ON  st.ID   =   ds.Status_ID
"""
    with engine.connect() as conn:
        conn.execute( sql_view )

def downgrade():
    with engine.connect() as conn:
        conn.execute( "DROP  VIEW  Data_Set_View" )

    op.drop_table('Data_Set')
