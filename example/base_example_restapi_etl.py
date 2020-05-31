# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import ABC, abstractmethod
from datetime import datetime as datetime

from etlite.context  import RestApiContext
from etlite.common.base_restapi_etl import BaseRestApiEtl
from etlite.common.base_sqlapi_etl  import BaseSqlApiEtl

"""
This is an optional class to add some additional methods and properties
for this Example vendor to be shared by both Example1 and Example2 etl jobs.
"""
#lass   BaseExampleRestApiEtl( BaseSqlApiEtl ,BaseRestApiEtl ): # NOTE: This order of multiple inheritance produces "RS" order.
class   BaseExampleRestApiEtl( BaseRestApiEtl ):
    """ The base Example REST ETL Job object.
        It implements most of the common abstract REST methods that define the generic REST workflow.
        All common sharable Example stuff should be placed in here.
    """
    API_KEY = "OSxE5kQ2OgqGdUTlofGR1Aa07rrPjffca1hZPPGuxQyjVgel3FCrPKdhL0NY"    # Fake secret.
    STOCK_URL = f"https://api.worldtradingdata.com/api/v1/stock?api_token={API_KEY}"

    def __init__( self ,dataset_code:str=None ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( dataset_code=dataset_code  ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )


    # Concrete properties section.
    #

    @property
    def init_date( self ) -> datetime:
        """ Return the very first initial date/time.
        This property implements the abstract property defined in the parent class.
        """
        return  None

    @property
    def request_http_header( self ) -> dict:
        """ Common HTTP header to be shared by all the Example datasets.
        This property overwrote the parent default property.
        """
        return  None

    #
    # End Interface implementation section

    # Extended example properties section.
    #

if  __name__ == "__main__":
    pass    