# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from  sqlalchemy import Binary, Column, JSON, Integer, BigInteger, SmallInteger ,String, Text, DateTime, Float, Boolean, PickleType
from  sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Frequency( Base ):
    """Frequency model.
    """
    __tablename__  = "Frequency"
    __table_args__ = {"schema": "etlite"}

    id      = Column( SmallInteger  ,nullable=False ,primary_key=True )
    name    = Column( String(8)     ,nullable=False )
    minutes = Column( Integer       ,nullable=False )

    def __repr__(self):
        return f'<Frequence {self.id}>'

class Severity( Base ):
    """Severity model.
    """
    __tablename__  = "Severity"
    __table_args__ = {"schema": "etlite"}

    id          = Column( SmallInteger  ,nullable=False ,primary_key=True )
    name        = Column( String(16)    ,nullable=False )
    description = Column( String(64)    ,nullable=False )
    updated_on  = Column( DateTime      ,nullable=False )

    def __repr__(self):
        return f'<Severity {self.id}>'

class Status( Base ):
    """Status model.
    """
    __tablename__  = "Status"
    __table_args__ = {"schema": "etlite"}

    id          = Column( SmallInteger  ,nullable=False ,primary_key=True )
    name        = Column( String(16)    ,nullable=False )
    description = Column( String(64)    ,nullable=False )
    is_active   = Column( Boolean                       )
    is_terminal = Column( Boolean                       )
    display_order=Column( SmallInteger                  )
    updated_on  = Column( DateTime      ,nullable=False )

class Data_Vendor( Base ):
    """Data Vendor model.
    """
    __tablename__  = "Data_Vendor"
    __table_args__ = {"schema": "etlite"}

    id          = Column( SmallInteger  ,nullable=False ,primary_key=True )
    code        = Column( String(8)     ,nullable=False )
    status_id   = Column( SmallInteger  ,nullable=False )
    name        = Column( String(64)    ,nullable=False )
    updated_on  = Column( DateTime      ,nullable=False )

class Data_Set( Base ):
    """Data Set model.
    """
    __tablename__  = "Data_Set"
    __table_args__ = {"schema": "etlite"}

    id                  = Column( SmallInteger  ,nullable=False ,primary_key=True )
    code                = Column( String(8)     ,nullable=False )
    parent_id           = Column( SmallInteger  )
    status_id           = Column( SmallInteger  ,nullable=False )
    data_vendor_id      = Column( SmallInteger  ,nullable=False )
    description         = Column( String(128)   ,nullable=False )
    exec_sequence       = Column( SmallInteger  ,nullable=False )
    run_frequency_id    = Column( SmallInteger  ,nullable=False )
    data_from           = Column( DateTime )
    data_upto           = Column( DateTime )
    last_data_from      = Column( DateTime )
    last_data_upto      = Column( DateTime )
    work_in_progress    = Column( Boolean  )
    lock_expires_after  = Column( SmallInteger)
    source_uri          = Column( String(128) )
    stage_uri           = Column( String(128) )
    stage_view          = Column( String( 64) )
    target_uri          = Column( String(128) )
    next_run_no         = Column( Integer       ,nullable=False )
    profiled_to_run_no  = Column( Integer  )
    verified_to_run_no  = Column( Integer  )
    next_run_no         = Column( Integer  )
    next_run_no         = Column( Integer  )
    average_duration    = Column( Integer  )
    onerror_contact     = Column( String(64))
    onsuccess_contact   = Column( String(64))
    remark              = Column( String(128))
    updated_on          = Column( DateTime      ,nullable=False )

class Job_Run( Base ):
    """Job Run model.
    """
    __tablename__   = "Job_Run"
    __table_args__  = {"schema": "etlite"}

    id              = Column( Integer       ,nullable=False ,primary_key=True )
    next_run_no     = Column( Integer       ,nullable=False )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    status_id       = Column( SmallInteger  ,nullable=False )
    data_from       = Column( DateTime )
    data_upto       = Column( DateTime )
    ran_from        = Column( DateTime )
    ran_upto        = Column( DateTime )
    total_count     = Column( Integer  )
    unique_count    = Column( Integer  )
    ingest_count    = Column( Integer  )
    error_count     = Column( Integer  )
    files_count     = Column( Integer  )
    deleted_count   = Column( Integer  )
    remark          = Column( String(128))
    updated_on      = Column( DateTime      ,nullable=False )

class Job_Run_File( Base ):
    """Job Run File model.
    """
    __tablename__   = "Job_Run_File"
    __table_args__  = {"schema": "etlite"}

    id              = Column( Integer       ,nullable=False ,primary_key=True )
    job_run_id      = Column( Integer       ,nullable=False )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    job_run_id      = Column( Integer       ,nullable=False )
    job_run_id      = Column( Integer       ,nullable=False )
    file_uri        = Column( String(128)   ,nullable=False )
    line_count      = Column( Integer )
    md5             = Column( Binary  )
    updated_on      = Column( DateTime      ,nullable=False )

class Job_Run_Metric( Base ):
    """Job Run Metric model.
    """
    __tablename__   = "Job_Run_Metric"
    __table_args__  = {"schema": "etlite"}

    id              = Column( Integer       ,nullable=False ,primary_key=True )
    job_run_id      = Column( Integer       ,nullable=False )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    stats           = Column( JSON )
    updated_on      = Column( DateTime      ,nullable=False )

class Data_Set_Profile( Base ):
    """Data Set Profile model.
    """
    __tablename__   = "Data_Set_Profile"
    __table_args__  = {"schema": "etlite"}

    id              = Column( Integer       ,nullable=False ,primary_key=True )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    status_id       = Column( SmallInteger  ,nullable=False )
    field_seq       = Column( SmallInteger  ,nullable=False )
    field_name      = Column( String(64)    ,nullable=False )
    data_type       = Column( String( 8)    ,nullable=False )
    skip_it         = Column( Boolean )
    do_Count        = Column( Boolean )
    do_Blank        = Column( Boolean )
    do_Distinct     = Column( Boolean )
    do_Average      = Column( Boolean )
    do_Median       = Column( Boolean )
    do_Minimum      = Column( Boolean )
    do_Maximum      = Column( Boolean )
    updated_on      = Column( DateTime      ,nullable=False )

class Job_Run_Profile_Result( Base ):
    """Job Run Profile Result model.
    """
    __tablename__   = "Job_Run_Profile_Result"
    __table_args__  = {"schema": "etlite"}

    id              = Column( Integer       ,nullable=False ,primary_key=True )
    job_run_id      = Column( Integer       ,nullable=False )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    profile_id      = Column( Integer       ,nullable=False )
    field_seq       = Column( SmallInteger  ,nullable=False )
    record_count    = Column( BigInteger )
    blank_count     = Column( BigInteger )
    distinct_count  = Column( BigInteger )
    average_numvalue= Column( Float )
    median_numvalue = Column( Float )
    minimum_numvalue= Column( Float )
    maximum_numvalue= Column( Float )
    average_dtmvalue= Column( DateTime )
    median_dtmvalue = Column( DateTime )
    minimum_dtmvalue= Column( DateTime )
    maximum_dtmvalue= Column( DateTime )
    updated_on      = Column( DateTime      ,nullable=False )

class Validation_Rule( Base ):
    """Validation Rule model.
    """
    __tablename__   = "Validation_Rule"
    __table_args__  = {"schema": "etlite"}

    id              = Column( SmallInteger  ,nullable=False ,primary_key=True )
    code            = Column( String(64)    ,nullable=False )
    parent_id       = Column( SmallInteger  )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    status_id       = Column( SmallInteger  ,nullable=False )
    description     = Column( String(128)   ,nullable=False )
    assert_order    = Column( SmallInteger  ,nullable=False )
    run_frequency_id= Column( SmallInteger  ,nullable=False )
    frequency_interval=Column(Integer       ,nullable=False )
    threshold_type  = Column( String( 1)    ,nullable=False )
    warn_top_limit  = Column( Float         ,nullable=False )   
    warn_bot_limit  = Column( Float         ,nullable=False )   
    error_top_limit = Column( Float         ,nullable=False )   
    error_bot_limit = Column( Float         ,nullable=False )   
    fatal_top_limit = Column( Float         ,nullable=False )   
    fatal_bot_limit = Column( Float         ,nullable=False )   
    expect_metric_sql=Column( Text          ,nullable=False )   
    actual_metric_sql=Column( Text          ,nullable=False )   
    last_validated_on=Column( DateTime )
    last_failed_on  = Column( DateTime )
    updated_on      = Column( DateTime      ,nullable=False )

class Validation_Result( Base ):
    """Validation Result model.
    """
    __tablename__   = "Validation_Result"
    __table_args__  = {"schema": "etlite"}

    id              = Column( Integer       ,nullable=False ,primary_key=True )
    validation_rule_id=Column(SmallInteger  ,nullable=False )
    job_run_id      = Column( Integer       ,nullable=False )
    data_set_id     = Column( SmallInteger  ,nullable=False )
    severity_id     = Column( SmallInteger  ,nullable=False )
    expect_int      = Column( BigInteger    )
    actual_int      = Column( BigInteger    )
    expect_flt      = Column( Float         )
    actual_flt      = Column( Float         )
    expect_dtm      = Column( DateTime      )
    actual_dtm      = Column( DateTime      )
    updated_on      = Column( DateTime      ,nullable=False )
