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

The REST api I/O shall be handled by the ETLite framework.  The stream data shall be read and
each raw record shall be passed to the concrete object to be transformed.  A cooked/formmated
record shall be return back to the framework.  The returned cooked data shall be written out to
a cloud bucket like S3.

The 3 big I/O; Web, S3, and DB are abstracted out from your concrete class
to be handled by the ETLite framework.  What is left for the concrete class
to do is to transform and prepare the data to be loaded into your data warehouse.
"""

from abc import abstractmethod
from aiohttp import ClientResponse
from datetime import datetime as datetime

from etlite.common.base_etl import BaseEtl

class   BaseRestApiEtl( BaseEtl ):

    def __init__( self ,job_code:str ,job_codes:list=None ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( job_code ,run_id ,from_date ,upto_date )

        self._request_token = None

    # Abstract interface section.
    #
    
    # Optional step 1.
    @abstractmethod
    def get_authentication_url( self ) -> str:
        """
        If there is a different URL to authenthicate then return the URL,
        else return None to skip.
        """
        pass

    @abstractmethod
    def get_authentication_msg( self ) -> str:
        """
        If a HTTP message body data is needed then return the appropriate text
        else return None to skip.
        """
        pass

    # Optional step 2.
    @abstractmethod
    def put_authentication_resp( self ,resp:ClientResponse ):
        """
        Query the resp to determine if you are authenticated.
        Usually you need to save your auth token.
        """
        pass

    # Optional step 3.
    @abstractmethod
    def get_data_request_url( self ) -> str:
        """
        If there is a different URL to request a set of data then return the URL,
        else return None to skip.
        """
        pass

    @abstractmethod
    def get_data_request_msg( self ) -> str:
        """
        If a HTTP message body data is needed then return the appropriate text
        else return None to skip.
        """
        pass

    # Optional step 4.
    @abstractmethod
    def put_data_request_resp( self ,resp:ClientResponse ):
        """
        Query the resp to determine if a request token/id is returned 
        to back to you for future use.
        """
        pass

    # Optional step 5.
    @abstractmethod
    def get_request_status_url( self ):
        """
        If there is a different URL to check on a request for set of data then return the URL,
        else return None to skip to the next step.
        """
        pass

    @abstractmethod
    def get_request_status_msg( self ) -> str:
        """
        If a HTTP message body data is needed then return the appropriate text
        else return None to skip.
        """
        pass

    # Optional step 6.
    @abstractmethod
    def put_request_status_resp( self ,resp:ClientResponse ):
        """
        Query the resp to determine if a request data set is ready to download.
        """
        pass

    # Required step 7.
    @abstractmethod
    def get_next_datapage_url( self ) -> str:
        """
        If you determine that more data pages are needed then return the URL,
        else return None to skip/terminate.
        """
        pass

    @abstractmethod
    def get_next_datapage_msg( self ) -> str:
        """
        If a HTTP message body data is needed then return the appropriate text
        else return None to skip.
        """
        pass

    # Required step 8.
    @abstractmethod
    def put_next_datapage_resp( self ,resp:ClientResponse ):
        """
        Query the resp to determine if there are more pages to download.
        """
        pass

    # TODO: Are the following common enough to be moved into the BaseEtl class?

    @property
    @abstractmethod
    def raw_filepath( self ) -> str:
        """
        The raw data file to write out the downloaded data into.
        """
        pass

    @property
    @abstractmethod
    def latest_filepath( self ) -> str:
        """
        The latest data file to write out the trnsform data into.
        """
        pass

    @property
    @abstractmethod
    def archive_filepath( self ) -> str:
        """
        The archive data file to write out the transform data into.
        """
        pass

    # Concrete properties section.
    #

    @property
    def request_header( self ) -> dict:
        """
        If your request require a different header, you MUST over write this method
        to provide your implmentation.
        """
        return { "content-type": "application/json; charset=utf-8" }

    @property
    def request_mesage( self ) -> str:
        """
        If your request require a message body data, you MUST over write this method
        to provide your implmentation.
        """
        return None

    @property
    def request_token( self ) -> str:
        """
        An original token that was provided by the vendor for your requested data set.
        This is to be used to check on the status of your requested data.
        """
        return  self._request_token

    @request_token.setter
    def request_token( self ,request_token:str ):
        self._request_token = request_token
