# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  datetime
import  os
import  sys
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/example.

from    aiohttp import  ClientResponse
from    etlite.common   import  cfg ,get_logger
from    etlite.common.base_etl  import  BaseEtl
from    etlite.common.context   import  RestApiContext
from    example.base_example_restapi_etl  import  BaseExampleRestApiEtl

class   Example1Etl( BaseExampleRestApiEtl ):
    """ An example implementation of an ETL job.
    Our example here is to download 30 stocks data.
    """
    CODE = "Example1"
    DOW30= ['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DOW','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','RTX','TRV','UNH','V','VZ','WBA','WMT','XOM' ]

    def __init__( self ,run_id:int=None ,filter_on:str=None ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( dataset_code=Example1Etl.CODE ,run_id=run_id ,filter_on='symbol' ,from_date=from_date ,upto_date=upto_date )
        self._is_Done = False

    # Private method section
    #

    # Begin Interface implementation section
    #

    # Required step 7.
    def get_datapage_urls( self ) -> list((str,dict,str,dict)):
        """ SEE: BaseRestApiEtl.get_datapage_urls()
        """
        rest_reqs = None
        if  not self._is_Done:
            rest_reqs = []
            for symbol  in Example1Etl.DOW30:
                params  =  {'symbol': symbol}
                loopback=  self.get_loopback()  # NOTE: In BaseEtl.py
                loopback['task'] = symbol       # NOTE: Fill in something unique that make sense to you.
                rest_reqs.append( (BaseExampleRestApiEtl.STOCK_URL ,params ,None ,loopback) )
            
            self._is_Done = True    # NOTE: Only do it once.

        return  rest_reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        return  None

    # Concrete properties section.
    #

    @property
    def output_data_header( self ) -> str:
        """ SEE: BaseEtl.output_data_header()
        """
        return  BaseEtl.DELIMITER.join( ['Symbol','Open','Close','High','Low','Volume'] )

    #
    # End Interface implementation section


if  __name__ == "__main__":
    e = Example1Etl()