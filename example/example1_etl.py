# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  datetime
import  os
import  sys
#sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/example.
import  ujson   as  json

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
    
#   {'pagination': {'limit': 100, 'offset': 0, 'count': 1, 'total': 0}
    JSON_TO_DB_MAPPING = {
            "symbol":     "symbol",
            "exchange":   "exchange",
            "date":       "traded_at",  # 2020-11-24T00:00:00+0000
            "open":       "open",
            "close":      "close",
            "high":       "high",
            "low":        "low",
            "volume":     "volume",
            "adj_open":   "adj_open",
            "adj_close":  "adj_close",
            "adj_high":   "adj_high",
            "adj_low":    "adj_low",
            "adj_volume": "adj_volume"
        }

    def __init__( self ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        # NOTE: Framework doesn't pass in instantiation parameters.
        super().__init__( dataset_code=Example1Etl.CODE ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )
        self._indices = [ 
            ( 'dji30' ,Example1Etl.DJI30 ), # Dow Jones Industrial
            ( 'djt20' ,Example1Etl.DJT20 ), # Dow Jones Transportation
            ( 'dju15' ,Example1Etl.DJU15 )  # Dow Jones Utilities
        ]
#        self._cities = [ 'London,uk' ,'Chicago,us' ,'Oakland,us' ,'Beijing,cn' ]

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
        This exametlite.engineple uses the self._indices stack to implement an interuptable loop.
        """
        rest_reqs = None
        if  self._indices:  # Is the stack empty?
            rest_reqs = []
            for symbol  in self._indices[0][1]:
                params  =  {'symbols': symbol}
                loopback=  self.get_loopback()          # NOTE: In BaseEtl.py
                loopback['task']  = symbol              # NOTE: Fill in something unique that make sense to you.
                loopback['index'] = self._indices[0][0] # NOTE: This is the stock exchange index. i.e. DOW30 ,NIFTY50 ,NASDAQ100, S&P500
                rest_reqs.append( (HTTP_GET ,BaseExampleRestApiEtl.STOCK_URL ,params ,None ,loopback) )
            del self._indices[0]    # NOTE: Pop the stock exchange index stack.

#        rest_reqs = None
#        if  self._cities:
#            rest_reqs = []
#            for city in self._cities:
#                params = {'q':city ,'appid': 'c67e4ca4fa5ce556a24984a982ba6ed2'}            
#                loopback=  self.get_loopback()
#                rest_reqs.append( (HTTP_GET ,'https://api.openweathermap.org/data/2.5/weather' ,params ,None ,loopback ))
#            self._cities = []

        return  rest_reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        # SEE: https://docs.python.org/3/library/io.html#io.TextIOBase
        
        ordinl = ctx.loopback['ordinal']
        stkidx = ctx.loopback['index']
        symbol = ctx.loopback['task']
        cooked = None
        if  isinstance( content ,str ):
            d = json.loads( content )
            if 'error'  in d:
                print( f"{ordinl:2} {stkidx}: {symbol:4} encountered error {d['error']['code']}" )
            else:
                print( f"{ordinl:2} {stkidx}: {symbol:4} length of returned request: {len(content)}" )
                tokens  = [str(d['data'][0][k]) if d['data'][0][k] else '' for k in Example1Etl.JSON_TO_DB_MAPPING ]
                cooked  = [ ( BaseEtl.DELIMITER.join( tokens ) ,0 ,f"ram://{stkidx}/" ) ]

        return  cooked

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
