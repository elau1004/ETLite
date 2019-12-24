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

    def __init__( self ,job_code:str ,run_id:int=0 ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( job_code ,run_id ,from_date ,upto_date )
        self.req_token = None

    def get_http_header( self ) -> dict:
        """
        Common HTTP header to be shared by all the Sample datasets.
        """
        return  None

    @property
    def request_token( self ) -> int:
        return  self.req_token

    @request_token.setter
    def request_token( self ,req_token:str ):
        self.req_token = req_token
