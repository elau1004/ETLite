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
    SUCCESSFUL= 0
    DELIMITER = '\t'
    CONTEXT   = { 'task': 'Not filled in!' ,'ordinal': 0 }  # Zero based ordinal.

    def __init__( self ,dataset_code:str ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        self._workflow_seq:str  = None          # The sequence of workflow engine to invoke from the inheritance order.
        self._dataset_code:str  = dataset_code  # Required unique code for this job in your code base.
        self._run_id:int        = run_id        # Optional unique id for each run.
        self._from_date:datetime= from_date     # Optional inclusive (greater and equal) to filter the source data.
        self._upto_date:datetime= upto_date     # Optional not inclusive (less than) to filter the source data.
        self._status_id:int     = None          # The current status/lifecycle this job is in.
        self._run_env:str       = ''            # The environment this object is running in. 'dev_' ,'test_' ,'' <- Production.

        if  not self._upto_date:
            self._upto_date = datetime.utcnow()

        # TOOD: Figure out what environment I am in.

    @property
    def dataset_code( self ) -> str:
        """ Return the code for the current data set.
        """
        return  self._dataset_code

    @property
    def workflow_seq( self ) -> str:
        """ Return the workflow sequence to invoke.
        """
        return  self._workflow_seq

    @workflow_seq.setter
    def workflow_seq( self ,value:str ):
        """ Set the workflow sequence to invoke.
        """
        self._workflow_seq = value

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
        """ Return the very first initial date/time to start your incremental extraction from.
        Generally, to be implemented in the specific Job concrete class.
        """
        pass

    @property
    @abstractmethod
    def output_data_header( self ) -> str:
        """ Return the header caption for the output text file.
        Generally, to be implemented in the specific Job concrete class.
        """
        pass

    # Concrete properties section.
    #

    def new_context( self ) -> dict:
        """ Return a default loopback context dictionary for sub-objects to fill.
        """
        return  BaseEtl.CONTEXT.copy()
