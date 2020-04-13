# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  os
import  sys
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/example.

from    aiohttp import  ClientResponse
from    etlite.common   import  cfg ,get_logger
from    etlite.common.base_etl  import  BaseEtl
from    example.base_example_restapi_etl  import  BaseExampleRestApiEtl

class   Example2Etl( BaseExampleRestApiEtl ):
    CODE = "EXAMPLE2"

    def __init__( self ):
        super().__init__( Example2Etl.CODE )

    # Private method section
    #

    
    # Begin Interface implementation section
    #

    @property
    def http_mesage( self ) -> str:
        return  None

    # Optional step 1.
    def get_authentication_url( self ) -> str:
        return  None

    # Optional step 2.
    def put_authentication_resp( self ,resp:ClientResponse ):
        pass

    # Optional step 3.
    def get_data_request_url( self ) -> str:
        return  None

    # Optional step 4.
    def put_data_request_resp( self ,resp:ClientResponse ):
        pass

    # Optional step 5.
    def get_request_status_url( self ):
        return  None

    # Optional step 6.
    def put_request_status_resp( self ,resp:ClientResponse ):
        pass

    # Required step 7.
    def get_next_datapage_url( self ) -> str:
        return  BaseExampleRestApiEtl.STOCK_URL + "IBM"

    # Required step 8.
    def put_next_datapage_resp( self ,resp:ClientResponse ):
        pass

    # Properties section
    #

    def raw_filepath( self ) -> str:
        return  None

    def latest_filepath( self ) -> str:
        return  None

    def archive_filepath( self ) -> str:
        return  None

    def output_data_header( self ) -> str:
        return None

    def transform_data( self ,record:str ,delimiter:str=BaseEtl.DELIMITER ) -> str:
        return None

    def source_table( self ) -> str:
        pass

    def source_columns( self ,columns:list ) -> list:
        pass

    def target_columns( self ,columns:list ) -> list:
        pass

    def stage_query( self ) -> str:
        pass

    def insert_query( self ) -> str:
        pass

    def update_query( self ) -> str:
        pass

    #
    # End Interface implementation section
