# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from    aiohttp import ClientResponse
from    sample.base_sample_restapi_etl  import  BaseSampleRestApiEtl

class   Sam2Etl( BaseSampleRestApiEtl ):
    CODE = "SAM2"

    def __init__( self ):
        super().__init__( Sam2Etl.CODE )

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
        return  None

    # Required step 8.
    def put_next_datapage_url( self ,resp:ClientResponse ):
        pass

    def get_raw_filepath( self ) -> str:
        return  None

    def get_latest_filepath( self ) -> str:
        return  None

    def get_archive_filepath( self ) -> str:
        return  None
