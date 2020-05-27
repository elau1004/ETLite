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
from    etlite.context  import  RestApiContext
from    etlite.common   import  cfg ,get_logger
from    etlite.common.base_etl  import  BaseEtl
from    etlite.common.constants import  HTTP_GET

from    example.base_example_restapi_etl  import  BaseExampleRestApiEtl

class   Example1Etl( BaseExampleRestApiEtl ):
    """ An example implementation of an ETL job.
    Our example here is to download stocks data for Dow Jones indices.
    """
    CODE = "Example1"
    DJI30= ['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DOW','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','RTX','TRV','UNH','V','VZ','WBA','WMT','XOM' ]
    DJT20= ['ALK','AAL','CAR','CHRW','CSX','DAL','EXPD','FDX','JBHT','JBLU','KSU','KEX','LSTR','MATX','NSC','R','LUV','UNP','UAL','UPD']
    DJU15= ['AES','AEP','AWK','CNP','ED','D','DUK','EIX','EXC','FE','NEE','NI','PEG','SRE','SO']

    JSON_TO_DB_MAPPING =         {
            "symbol":               "symbol",
            "currency":             "currency",
            "last_trade_time":      "traded_at", # timestamp
            "price":                "price",
            "price_open":           "day_open",
            "day_high":             "day_high",
            "day_low":              "day_low",
            "52_week_high":         "52weeks_high",
            "52_week_low":          "52weeks_low",
            "day_change":           "day_price_change",
            "change_pct":           "day_percent_change",
            "close_yesterday":      "yesterday_close",
            "volume":               "day_volume",
            "volume_avg":           "avg_volume",
            #
            "name":                 "name",
            "pe":                   "pe",
            "eps":                  "eps",
            "shares":               "shares",
            "market_cap":           "market_cap",
#           "stock_exchange_long":  "stock_exchange_long",
            "stock_exchange_short": "exchange",
            "timezone":             "timezone",
#           "timezone_name":        "timezone_name"
            "gmt_offset":           "gmt_offset"
        }

    def __init__( self ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        # NOTE: Framework doesn't pass in instantiation parameters.
        super().__init__( dataset_code=Example1Etl.CODE ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )
        self._indices = [ 
            ( 'dji30' ,Example1Etl.DJI30 ), # Dow Jones Industrial
            ( 'djt20' ,Example1Etl.DJT20 ), # Dow Jones Transportation
            ( 'dju15' ,Example1Etl.DJU15 )  # Dow Jones Utilities
        ]

    # Private method section
    #

    # Begin Interface implementation section
    #

    # Required step 7.
    def get_datapage_urls( self ) -> list((str,str,dict,str,dict)):
        """ SEE: BaseRestApiEtl.get_datapage_urls()
        
        This method is primarily manages your data page request and pagination.
        This method will be called many times until you return empty list or 
        None value to terminate the framework internal loop.
        This example uses the self._indices stack to implement an interuptable loop.
        """
        rest_reqs = None
        if  self._indices:  # Is the stack empty?
            rest_reqs = []
            for symbol  in self._indices[0][1]:
                params  =  {'symbol': symbol}
                loopback=  self.get_loopback()          # NOTE: In BaseEtl.py
                loopback['task']  = symbol              # NOTE: Fill in something unique that make sense to you.
                loopback['index'] = self._indices[0]    # NOTE: This is the stock exchange index. i.e. DOW30 ,NIFTY50 ,NASDAQ100, S&P500
                rest_reqs.append( (HTTP_GET ,BaseExampleRestApiEtl.STOCK_URL ,params ,None ,loopback) )

            del self._indices[0]    # NOTE: Pop the stock exchange index stack.
        return  rest_reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        print( f"{ctx.loopback['ordinal']:2} {ctx.loopback['task']:2} length of returned request: {len(content)}" )
        return  None    # TODO: Finish this up.

    # Concrete properties section.
    #

    @property
    def output_data_header( self ) -> str:
        """ SEE: BaseEtl.output_data_header()
        """
        return  BaseEtl.DELIMITER.join( [v for v in Example1Etl.JSON_TO_DB_MAPPING.values() ] )

    #
    # End Interface implementation section


if  __name__ == "__main__":
    e = Example1Etl()
