# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
The concrete class that is to be extended from this base class with be ultimately be instantiated
by the ETLite framework and thus begins a dialog between them.
The framewoark get properties from the object.  If the value is None, the pre-determine workflow step
shall be skipped.
"""

from abc import ABC, abstractmethod
from datetime import datetime as datetime

from etlite.common.constants    import Status
from etlite.common.exceptions   import ETLiteException

class   BaseEtl( ABC ):
    """ The base abstract ETL Job object.
        It holds some basic metadata properties to track the life-cycle of a job.
    """
    DELIMITER = '\t'
    LOOPBACK  = { 'task': 'Not filled in!' ,'ordinal': 0 }

    def __init__( self ,dataset_code:str ,run_id:int ,from_date:datetime ,upto_date:datetime ):
        self._dataset_code:str  = dataset_code  # Unique code for this job.
        self._run_id:int        = run_id        # Unique id for each run.
        self._from_date:datetime= from_date     # Inclusive (greater and equal) to filter the source data.
        self._upto_date:datetime= upto_date     # Not inclusive (less than) to filter the source data.
        self._status_id:int     = None          # The current status/lifecycle this job is in.

        if  not self._upto_date:
            self._upto_date = datetime.utcnow()

    @property
    def dataset_code( self ) -> str:
        """ Return the code for the current data set.
        """
        return  self._dataset_code

    @property
    def run_id( self ) -> int:
        """ Return the unique run id.
        """
        return  self._run_id

    @run_id.setter
    def run_id( self ,value:int ):
        self._run_id =value

    @property
    def from_date( self ) -> datetime:
        """ Return the starting from date to be used to filter your incremental data.
            By convention you should filter it with the greater-and-equal operator.
        """
        return  self._from_date

    @from_date.setter
    def from_date( self ,value:datetime ):
        self._from_date =value

    @property
    def upto_date( self ) -> datetime:
        """ Return the ending upto date to be used to filter your incremental data.
            By convention you should filter it with the less-than operator.
        """
        return  self._upto_date

    @upto_date.setter
    def upto_date( self ,value:datetime ):
        self._upto_date =value

    @property
    def status_id( self ) -> int:
        """ Return the current status id of the current run of this dataset.
        """
        return  self._status_id

    @status_id.setter
    def status_id( self ,value:int ):
        self._status_id =value

    @property
    @abstractmethod
    def init_date( self ) -> datetime:
        """ Return the very first initial date/time to start your incremental extraction.
        """
        pass

    @property
    @abstractmethod
    def output_data_header( self ) -> str:
        """ Return the header caption for the output text file.
        """
        pass

    # Concrete properties section.
    #

    def get_loopback( self ) -> dict:
        """ Return a default loop back dictionary for sub-objects to fill.
        """
        return  LOOPBACK.copy()
