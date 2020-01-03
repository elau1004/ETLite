# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import ABC, abstractmethod
from datetime import datetime as datetime

from etlite.common.base_restapi_etl import BaseRestApiEtl

"""
This is an optional class to add some additional methods and properties
for this Sample vendor to be shared by both Sam1 and Sam2 etl jobs.
"""
class   BaseSampleRestApiEtl( BaseRestApiEtl ):

    API_KEY = "OSxE5kQ2OgqGdUTlofGR1Aa07rrPjffca1hZPPGuxQyjVgel3FCrPKdhL0NY"
    STOCK_URL = f"https://api.worldtradingdata.com/api/v1/stock?api_token={API_KEY}&symbol="

    def __init__( self ,job_code:str ,job_codes:list=None ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( job_code ,run_id ,from_date ,upto_date )

    # Begin Interface implementation section
    #
    
    def get_http_header( self ) -> dict:
        """
        Common HTTP header to be shared by all the Sample datasets.
        """
        return  None

    def get_authentication_msg( self ) -> str:
        """
        Common HTTP message body data to be shared by all the Sample datasets during authentoication.
        """
        return  None

    def get_data_request_msg( self ) -> str:
        """
        Common HTTP message body data to be shared by all the Sample datasets during data request.
        """
        return  None

    def get_request_status_msg( self ) -> str:
        """
        Common HTTP message body data to be shared by all the Sample datasets during status request.
        """
        return  None

    def get_next_datapage_msg( self ) -> str:
        """
        Common HTTP message body data to be shared by all the Sample datasets during datapage fetch.
        """
        return  None

    #
    # End Interface implementation section

    # Extended properties section.
    #

    def throttle_up( self ) ->(int,int):
        """
        Throttle down the pagination.
        Return:
        -   the count of pages to request.
        -   the ceiling of the max pages to request.
        """
        return None, None

    def throttle_down( self ) ->(int,int):
        """
        Throttle down the pagination.
        Return:
        -   the count of pages to request.
        -   the ceiling of the max pages to request.
        """
        return None, None
