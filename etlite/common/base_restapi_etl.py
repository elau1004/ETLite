# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
This is an abstract base class that defines the workflow interface for a REST API.
The outer framework shall have a dialog with your extended class.
If the getter method return a None value, that step and its corresponding put shall be skipped.
The dialog follows the following pattern:
    1. Framework ask for a value by "getting" the property from your class.
    2. Framework does the heavy lifting on behalf of your job.
    3. Framework put(set) the result back to you to process.
       Put implies that you have to do some work and not just storing it away.

Any properties are deemed common to REST API shall be added in this class.
"""

from abc import abstractmethod
from aiohttp import ClientResponse
from datetime import datetime as datetime

from etlite.common.base_etl import BaseEtl

# TODO: Evaluate properties vs seetter/getter. https://www.python-course.eu/python3_properties.php

class   BaseRestApiEtl( BaseEtl ):

    def __init__( self ,job_code:str ,run_id:int=0 ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( job_code ,run_id ,from_date ,upto_date )

    @abstractmethod
    def get_http_header( self ) -> dict:
        pass

    # Optional step 1.
    @abstractmethod
    def get_authentication_url( self ) -> str:
        # If there is a different URL to authenthicate then return the URL,
        # else return None to skip.
        pass

    # Optional step 2.
    @abstractmethod
    def put_authentication_resp( self ,resp:ClientResponse ):
        # Query the resp to determine if you are authenticated.
        # Usually you need to save your auth token.
        pass

    # Optional step 3.
    @abstractmethod
    def get_data_request_url( self ) -> str:
        # If there is a different URL to request a set of data then return the URL,
        # else return None to skip.
        pass

    # Optional step 4.
    @abstractmethod
    def put_data_request_resp( self ,resp:ClientResponse ):
        # Query the resp to determine if a request token/id is returned 
        # to back to you for future use.
        pass

    # Optional step 5.
    @abstractmethod
    def get_request_status_url( self ):
        # If there is a different URL to check on a request for set of data then return the URL,
        # else return None to skip to the next step.
        pass

    # Optional step 6.
    @abstractmethod
    def put_request_status_resp( self ,resp:ClientResponse ):
        # Query the resp to determine if a request data set is ready to download.
        pass

    # Required step 7.
    @abstractmethod
    def get_next_datapage_url( self ) -> str:
        # If you determine that more data pages are needed then return the URL,
        # else return None to skip/terminate.
        pass

    # Required step 8.
    @abstractmethod
    def put_next_datapage_url( self ,resp:ClientResponse ):
        pass

    @abstractmethod
    def get_raw_filepath( self ) -> str:
        # The raw data file to write out the downloaded data into.
        pass

    @abstractmethod
    def get_latest_filepath( self ) -> str:
        # The latest data file to write out the trnsform data into.
        pass

    @abstractmethod
    def get_archive_filepath( self ) -> str:
        # The archive data file to write out the transform data into.
        pass

    # TODO:
    # Figure out mapping.
    # Get target table name.
    # Get source table/view name.
    # Get source columns to ignore.
    # Insert into staging.
    # Insert into target.
    # Manage SCD2 table status.
    # Set counts. raw, unique, scd2 inserts.
