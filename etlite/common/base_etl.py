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
    DELIMITER = '\t'

    def __init__( self ,dataset_code:str ,dataset_codes:list=None ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ,status_id:int=None ):
        self._dataset_code:str  = dataset_code      # Unique code for this job.
        self._dataset_codes:list= dataset_codes     # A list of codes in a Flywheel.
        self._run_id:int        = run_id            # Unique id for each run.
        self._from_date:datetime= from_date         # Inclusive (greater and equal) to filter the source data.
        self._upto_date:datetime= upto_date         # Not inclusive (less than) to filter the source data.
        self._status_id:int     = status_id         # Current status/life-cycle of processing instance of thius dataset.

        if  not self._status_id:
            self._status_id = Status.PENDING

        if  not self._upto_date:
            self._upto_date = datetime.utcnow()

        if  dataset_code and dataset_codes:
            raise ETLiteException( "Dataset_Code and Dataset_Codes MUST be mutually exclusively provided." )

    @property
    def dataset_code( self ) -> str:
        """Return the code for the current data set.
        """
        return  self._dataset_code

    @property
    def dataset_codes( self ) -> list:
        """Return the list of codes for the current data set.
        """
        return  self._dataset_codes

    @property
    def run_id( self ) -> int:
        """Return the unique run id.
        """
        return  self._run_id

    @run_id.setter
    def run_id( self ,run_id:int ):
        self._run_id = run_id

    @property
    def from_date( self ) -> datetime:
        """Return the starting from date to be used to filter your incremental data.
        """
        return  self._from_date

    @from_date.setter
    def from_date( self ,from_date:datetime ):
        self._from_date = from_date

    @property
    def upto_date( self ) -> datetime:
        """Return the ending upto date to be used to filter your incremental data.
        """
        return  self._upto_date

    @upto_date.setter
    def upto_date( self ,upto_date:datetime ):
        self._upto_date = upto_date

    @property
    def status_id( self ) -> int:
        """Return the current status id of the current run of this dataset.
        """
        return  self._status_id

    @status.setter
    def status( self ,status:int ):
        self._status = status

    @property
    @abstractmethod
    def output_data_header( self ) -> str:
        """Return the header caption for the output text file.
        """
        pass

    @abstractmethod
    def transform_data( self ,record:str ,delimiter:str=DELIMITER ) -> str:
        """
        Transform the raw record into your new formatted record to be output.
        The input is a text stream and should hold off on marshalling into
        and un-marshalling out from JSON.
        """
        pass

    @property
    @abstractmethod
    def source_table( self ) -> str:
        """
        Framework shall use this table/view to query a default list of columns.
        """
        pass

    @property
    @abstractmethod
    def source_columns( self ,columns:list ) -> list:
        """
        Framework is asking you to verify/transform the default source columns.
        Ideally source columns should be the same as target columns.
        """
        pass

    @property
    @abstractmethod
    def target_columns( self ,columns:list ) -> list:
        """
        Framework is asking you to verify/transform the default target columns.
        Ideally source columns should be the same as target columns.
        """
        pass

    @property
    @abstractmethod
    def stage_query( self ) -> str:
        """
        The query you want the ETLite framework to execute on your behalf
        to stage your data into the staging area/table.
        Return None is you want to skip this step.
        """
        pass

    @property
    @abstractmethod
    def insert_query( self ) -> str:
        """
        The query you want the ETLite framework to execute on your behalf
        to insert your data into the target table.
        Return None is you want to skip this step.
        """
        pass

    @property
    @abstractmethod
    def update_query( self ) -> str:
        """
        The query you want the ETLite framework to execute on your behalf
        to update your data in the target table.  This is usually for maintaing SCD2 rows.
        Return None is you want to skip this step.
        """
        pass
