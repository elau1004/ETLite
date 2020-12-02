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

class   Example3Etl( BaseExampleRestApiEtl ):
    """ An example implementation of an ETL job.
    Our example here is to download stocks data for Dow Jones indices.
    """
    CODE = "Example3"
    ASIA= ['Beijing,cn','Tokyo, jp']
    EUROPE= ['London,uk','Paris, fr','Rome, it' ]
    NAMERICA= ['San Francisco, us','New York, us', 'Chicago, us', 'Dallas, us']
    SAMERICA= ['Lima, pe','Bogota, co']

    def __init__( self ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        # NOTE: Framework doesn't pass in instantiation parameters.
        super().__init__( dataset_code=Example3Etl.CODE ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )
        self._cities = [ 
            ( 'ASIA' ,Example3Etl.ASIA ),           # Asian cities
            ( 'EUROPE' ,Example3Etl.EUROPE ),       # Europian cities
            ( 'NAMERICA' ,Example3Etl.NAMERICA ),   # North America cities
            ( 'SAMERICA' ,Example3Etl.SAMERICA )    # South America cities
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
        if  self._cities:
            rest_reqs = []
            for city in self._cities[0][1]:
                params = {'q':city ,'appid': 'c67e4ca4fa5ce556a24984a982ba6ed2'}            
                loopback=  self.get_loopback()
                loopback['city'] = city
                loopback['continent'] = self._cities[0][0] # NOTE: This
                rest_reqs.append( (HTTP_GET ,'https://api.openweathermap.org/data/2.5/weather' ,params ,None ,loopback ))
            del self._cities[0]    # NOTE: Pop the continent from the list.

        return  rest_reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        # SEE: https://docs.python.org/3/library/io.html#io.TextIOBase
        ordinl = ctx.loopback['ordinal']
        city = ctx.loopback['city']
        continent = ctx.loopback['continent']
        cooked = None
        if  isinstance( content ,str ):
            d = json.loads( content )
            if 'cod'  in d:
                print( f"{ordinl:2} {continent:8} {city:16} encountered error {d['cod']['message']}" )
            else:
                print( f"{ordinl:2} {continent:8} {city:16} length of returned request: {len(content)}" )
                tokens  = []
                tokens.append(str(self.find('id',d)))
                tokens.append(self.find('name',d))
                tokens.append(self.find('sys.country',d))
                tokens.append(d['weather'][0]['description'])
                tokens.append(str(self.find('main.temp',d)))
                tokens.append(str(self.find('main.humidity',d)))
                print(tokens)
                cooked  = [ ( BaseEtl.DELIMITER.join( tokens ) ,0 ,f"ram://{continent}/" ) ]

        return  cooked

    # Concrete properties section.
    #

    @property
    def output_data_header( self ) -> str:
        """ SEE: BaseEtl.output_data_header()
        """
        return  BaseEtl.DELIMITER.join( [v for v in Example3Etl.JSON_TO_DB_MAPPING.values() ] )

    #
    # End Interface implementation section


if  __name__ == "__main__":
    e = Example3Etl()
