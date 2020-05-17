# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

HTTP_GET = 'get'
HTTP_POST= 'post'

from enum import Enum, unique

@unique
class Frequency( Enum ):
    MANUAL      = 0
    MINUTE      = 1
    HOUR        = 2
    DAY         = 3
    WEEK        = 4
    MONTH       = 5
    QUARTER     = 6
    SEMESTER    = 7
    ANNUAL      = 8

@unique
class Severity( Enum ):
    CRITICAL    = 1 #   Functionality is affected.
    ERROR       = 2 #   An error condition exists and functionality could be affected.
    WARNING     = 3 #   Functionality could be affected.
    INFO        = 4 #   General information about system operations.
    DEBUG       = 5 #   Debugging trace.

# This following are the lifecycle status for a job.  The maximum value shall be 255.
@unique
class Status( Enum ):
    ERRORED         = 0   
    DISABLED        = 1   
    ENABLED         = 2   
    PENDING         = 3
    SUSPENDED       = 4   
    CANCELLING      = 5   
    CANCELLED       = 6   
    COMPLETING      = 7   
    COMPLETED       = 8   
#   Extraction/Transport phase
    AUTHENTICATING  = 11  
    AUTHENTICATED   = 12  
    REQUESTING      = 13  # From REST API.
    REQUESTED       = 14  
    CHECKING        = 15  
    CHECKED         = 16
    DOWNLOADING     = 17
    DOWNLOADED      = 18
    PAGINATING      = 19  
    PAGINATED       = 20  
    QUERYING        = 21  # From Database.
    QUERIED         = 22  
    COPYING         = 25  # From Filesystem.
    COPIED          = 26
#   Processing phase  
    FORMATTING      = 31  
    FORMATTED       = 32  
    STAGING         = 33
    STAGED          = 34  
#   Ingestion phase     
    IMPORTING       = 41  
    IMPORTED        = 42  
    PROFILING       = 43  
    PROFILED        = 44  
#   Certification phase
    VALIDATING      = 51  
    VALIDATED       = 52  
    FAILING         = 53  
    FAILED          = 54  
#   Above value of 200 is for you to extend into.
