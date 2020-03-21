"""Create Table Data Set

Revision ID: 7a670e1241eb
Revises: 444326c53f71
Create Date: 2020-02-15 15:40:43.684121
"""
# pylint: disable=maybe-no-member

from    alembic import context
from    alembic import op
from    importlib.machinery import SourceFileLoader
import  os
import  pathlib
import  sqlalchemy  as sa
from    sqlalchemy     import create_engine
from    sqlalchemy.sql import table, column, func

# revision identifiers, used by Alembic.
revision = '7a670e1241eb'
down_revision = '444326c53f71'
branch_labels = None
depends_on = None


# NOTE: Need more precise control over the physical cross DB table design.
config  = context.config
db:str  = context.get_context().dialect.name
url:str = config.get_main_option("sqlalchemy.url")
engine  = create_engine( url )

# Dynamically load config module and assign ETLite Cross DB mapping to a locxal variable.
_path2cfg = str(sorted(pathlib.Path(os.getcwd()).glob( '**/xdb_config.py' )).pop())
# pylint: disable=no-value-for-parameter
xdb = SourceFileLoader( 'xdb_config' ,_path2cfg ).load_module().xdb_map[db]


def upgrade():
    sql_text = f"""
CREATE  TABLE   Data_Set (
         ID                 {xdb['int16'] :15} NOT NULL  CONSTRAINT Data_Set_PK PRIMARY KEY {xdb['autoinc']}   {xdb['comment']} 'The Primary Key'   
        --
        ,Code               {xdb['txt08'] :15} NOT NULL             {xdb['comment']} 'An unique nmemonic to identify a row.'
        ,Parent_ID          {xdb['int16'] :15} NOT NULL             {xdb['comment']} 'The parent data set that this row is grouped under.'
        ,Status_ID          {xdb['int08'] :15} NOT NULL  DEFAULT 2  {xdb['comment']} 'Foreign key to the status.  Default to enabled.'
        ,Data_Vendor_ID     {xdb['int16'] :15} NOT NULL             {xdb['comment']} 'Foreign key to the Data Vendor.'
        ,Description        {xdb['txt128']:15} NOT NULL             {xdb['comment']} 'A descriptive explaination of the data set.'
        ,Exec_Sequence      {xdb['int08'] :15} NOT NULL  DEFAULT 1  {xdb['comment']} 'The order to execute the ETL job for this data set.'
        ,Run_Frequency_ID   {xdb['int08'] :15} NOT NULL  DEFAULT 3  {xdb['comment']} 'The frequency to process this data set.  Default to Daily.'
        ,Frequency_Interval {xdb['int16'] :15} NOT NULL  DEFAULT 1  {xdb['comment']} 'The frequency interval to process this data set.'
        ,Data_From          {xdb['utcdtm']:15}     NULL             {xdb['comment']} 'The incremental starting date/time for the last successful ETL execution.'
        ,Data_Upto          {xdb['utcdtm']:15}     NULL             {xdb['comment']} 'The incremental ending date/time (not inclusive) the last successful ETL execution.'
        ,Last_Ran_From      {xdb['utcdtm']:15}     NULL             {xdb['comment']} 'The UTC datetime the ETL job last started on.'
        ,Last_Ran_Upto      {xdb['utcdtm']:15}     NULL             {xdb['comment']} 'The UTC datetime the ETL job last ended on.'
        ,Work_in_Progress   {xdb['bit0']                       :34} {xdb['comment']} 'A flag to indicate if a job for this data set is currently executing.'
        ,Lock_Expire_After  {xdb['int16'] :15} NOT NULL  DEFAULT 60 {xdb['comment']} 'A time out duration to expire a lock job.  Default to 1 hour.'
        ,Source_URI         {xdb['txt128']:15}     NULL             {xdb['comment']} 'The source of the dataset to extract from.'
        ,Stage_URI          {xdb['txt128']:15}     NULL             {xdb['comment']} 'The temporary staging area/file for the extracted dataset.'
        ,Stage_View         {xdb['txt64'] :15}     NULL             {xdb['comment']} 'The view to query the data from the staging area to be persisted into the target destination.'
        ,Target_URI         {xdb['txt128']:15}     NULL             {xdb['comment']} 'The target destination for the transformed data from the source.'
        ,Next_Run_No        {xdb['int32'] :15} NOT NULL  DEFAULT 10 {xdb['comment']} 'A grouping/batch number to group all the records together for the next job run.'
        ,Profiled_to_Run_No {xdb['int32'] :15}     NULL             {xdb['comment']} 'An optimization hint to profile the data set from this point onwards.'
        ,Verified_to_Run_No {xdb['int32'] :15}     NULL             {xdb['comment']} 'An optimization hint to verify  the data set from this point onwards.'
        ,Average_Duration   {xdb['int32'] :15}     NULL             {xdb['comment']} 'An average duration for quick reference without re-aggregating it.'
        ,OnError_Contact    {xdb['txt64'] :15}     NULL             {xdb['comment']} 'Notify this list if job failed.'
        ,OnSuccess_Contact  {xdb['txt64'] :15}     NULL             {xdb['comment']} 'Notify this list if job completed succussfully.'
        ,Remark             {xdb['txt128']:15}     NULL             {xdb['comment']} 'General remark.'
        --
        ,Updated_On         {xdb['utcupd']                     :52} {xdb['comment']} 'The audit timestamp when this row was last updated'
        --
        ,CONSTRAINT Data_Set_ID_CK          CHECK(  ID BETWEEN 1 AND 2048 )
        ,CONSTRAINT Data_Set_Status_CK      CHECK(  Status_ID BETWEEN 1 AND 2 )
        ,CONSTRAINT Data_Set_Exec_Seq_CK    CHECK(  Exec_Sequence BETWEEN 1 AND 255 )
        ,CONSTRAINT Data_Set_Interval_CK    CHECK(  Frequency_Interval BETWEEN 1 AND 59 )
        ,CONSTRAINT Data_Set_Lock_Expire_CK CHECK(  Lock_Expire_After > 0 )
        --
        ,CONSTRAINT Data_Set_Parent_FK      FOREIGN KEY( Parent_ID ) REFERENCES Data_Set( ID )
        ,CONSTRAINT Data_Set_Status_FK      FOREIGN KEY( Status_ID ) REFERENCES Status( ID )
        ,CONSTRAINT Data_Set_Vendor_FK      FOREIGN KEY( Data_Vendor_ID ) REFERENCES Data_Vendor( ID )
        ,CONSTRAINT Data_Set_Frequency_FK   FOREIGN KEY( Run_Frequency_ID ) REFERENCES Frequency( ID )
)
"""
    context.execute( sql_text )

    sql_text = f"""
CREATE UNIQUE INDEX Data_Set_Code_UK1       ON  Data_Set( Code )
"""
    context.execute( sql_text )

    sql_text = """
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
JOIN    Data_Set    AS  pr  ON  pr.ID   =   ds.Parent_ID    --  Only 2 levels!
JOIN    Data_Vendor AS  dv  ON  dv.ID   =   ds.Data_Vendor_ID
JOIN    Frequency   AS  hz  ON  hz.ID   =   ds.Run_Frequency_ID
JOIN    Status      AS  st  ON  st.ID   =   ds.Status_ID
"""
    context.execute( sql_text )

def downgrade():
    context.execute( "DROP  VIEW   Data_Set_View" )
    context.execute( "DROP  TABLE  Data_Set" )
