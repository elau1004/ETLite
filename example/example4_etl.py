# -*- coding: utf-8 -*-
# FX exchange rate API : www.exchangerate-api.com
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

class   Example4Etl( BaseExampleRestApiEtl ):
    """ An example implementation of an ETL job.
    Our example here is to download stocks data for Dow Jones indices.
    """
    CODE = "Example4"
    FX_BASE = ['USD','EUR','JPY','GBP']
    
    def __init__( self ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        # NOTE: Framework doesn't pass in instantiation parameters.
        super().__init__( dataset_code=Example4Etl.CODE ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )
        self._FX = [ 
            ( 'FX_Base' ,Example4Etl.FX_BASE)       # FX base code
        ]

    # Private method section
    #
    def find( self, element, json):
        keys = element.split('.')
        rv = json
        for key in keys:
            rv = rv[key]
        return rv

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
        if  self._FX:
            rest_reqs = []
            for fx in self._FX[0][1]:
    #           params = {'base_code':fx}            
                loopback=  self.get_loopback()
                loopback['fx'] = fx
    #           rest_reqs.append((HTTP_GET ,'https://v6.exchangerate-api.com/v6' ,params ,None ,loopback ))
    #           rest_reqs.append((HTTP_GET ,'https://v6.exchangerate-api.com/v6/9e50d469929454161aef2f74/latest/USD' ,params ,None ,loopback ))
                req_url = f'https://v6.exchangerate-api.com/v6/9e50d469929454161aef2f74/latest/{fx}'
                rest_reqs.append((HTTP_GET , req_url ,None ,None ,loopback ))
    #       del self._cities[0]    # NOTE: Pop the continent from the list.
            self._FX = []          # clear the list

        return  rest_reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        # SEE: https://docs.python.org/3/library/io.html#io.TextIOBase
        ordinl = ctx.loopback['ordinal']
        fx = ctx.loopback['fx']
        cooked = None
        if  isinstance( content ,str ):
            d = json.loads( content )
            if 'error'  in d:
                print( f"{ordinl:2} {fx:3} encountered error : {str(d['result'])} {d['error-type']}" )
            else:
                print( f"{ordinl:2} {fx:3}  length of returned request: {len(content)}" )
                tokens  = []
                tokens.append(self.find('base_code',d))
                tokens.append(self.find('time_last_update_utc',d))
                tokens.append(str(self.find('conversion_rates.USD',d)))
                tokens.append(str(self.find('conversion_rates.EUR',d)))
                tokens.append(str(self.find('conversion_rates.JPY',d)))
                tokens.append(str(self.find('conversion_rates.GBP',d)))
                print(tokens)
                cooked  = [ ( BaseEtl.DELIMITER.join( tokens ) ,0 ,f"ram://{fx}/" ) ]

        return  cooked

    # Concrete properties section.
    #

    @property
    def output_data_header( self ) -> str:
        """ SEE: BaseEtl.output_data_header()
        """
        return  BaseEtl.DELIMITER.join( [v for v in Example4Etl.JSON_TO_DB_MAPPING.values() ] )

    #
    # End Interface implementation section


if  __name__ == "__main__":
    e = Example4Etl()
