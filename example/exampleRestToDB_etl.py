# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  datetime
import  os
import  sys
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/example.
import  ujson   as  json

from    aiohttp import  ClientResponse

from    etlite.context  import  RestApiContext
from    etlite.common   import  cfg ,get_logger
from    etlite.common.base_etl  import  BaseEtl
from    etlite.common.constants import  HTTP_GET

from    example.base_example_restapi_etl  import  BaseExampleRestApiEtl

class   ExampleRestToDB( BaseExampleRestApiEtl ):
    """ An example implementation of an ETL job.
    Our example here is to download data from weather site and pump them into the database
    """
    CODE = "ExampleRestToDB"

    DB_NAME = "postgres"

    ASIA= ['Beijing,cn','Tokyo, jp']
    EUROPE= ['London,uk','Paris, fr','Rome, it' ]
    NAMERICA= ['San Francisco, us','New York, us', 'Chicago, us', 'Dallas, us']
    SAMERICA= ['Lima, pe','Bogota, co']

    # may be used in the future
    JSON_TO_DB_MAPPING = {
            "name":         "city",
            "country":      "country",
            "discription":  "discription",
            "temp":         "temp"
    }

    def __init__( self ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        # NOTE: Framework doesn't pass in instantiation parameters.
        super().__init__( dataset_code=ExampleRestToDB.CODE ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )
        
        self._cities = [ 
            ( 'weather1' ,ExampleRestToDB.ASIA ),           # Asian cities
            ( 'weather2' ,ExampleRestToDB.EUROPE ),       # Europian cities
            ( 'weather3' ,ExampleRestToDB.NAMERICA ),   # North America cities
            ( 'weather4' ,ExampleRestToDB.SAMERICA )    # South America cities
        ]

    # extract value based on key from a nested dictionary
    @staticmethod
    def extract(d, token):
        def find(d, token, result):
            for key, value in d.items():
                if key == token:
                    result.append(value)
                if isinstance(value, dict):
                    find(value, token, result)
                elif isinstance(value, list):
                    for element in value:
                        if isinstance(element, dict):
                            find(element, token, result)

        answer = []
        find(d, token, answer)  
        if not answer:
            return "Not Found !"
        else:
            return str(answer[0])


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
                loopback['table'] = self._cities[0][0] # NOTE: This
                rest_reqs.append( (HTTP_GET ,'https://api.openweathermap.org/data/2.5/weather' ,params ,None ,loopback ))
            del self._cities[0]    # NOTE: Pop the continent from the list.

        return  rest_reqs

    # Required step 8.
    async def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        # SEE: https://docs.python.org/3/library/io.html#io.TextIOBase
        ordinl = ctx.loopback['ordinal']
        city = ctx.loopback['city']
        print("\n", city)
        table = ctx.loopback['table']
        cooked = None
        if  isinstance( content ,str ):
            d = json.loads( content ) 
        
            if 'error' in d:
                print( f"{ordinl:2} {table:8} {city:16} encountered error {d['cod']['message']}" )
            else:
                print( f"{ordinl:2} {table:8} {city:16} length of returned request: {len(content)}" )
                tokens  = []
                tokens.append( ExampleRestToDB.extract(d, 'name'))
                tokens.append( ExampleRestToDB.extract(d, 'country'))
                tokens.append( ExampleRestToDB.extract(d, 'description'))
                tokens.append( ExampleRestToDB.extract(d, 'temp'))
            
                cooked  = [ ( BaseEtl.DELIMITER.join( tokens ) ,f"sql://{ExampleRestToDB.DB_NAME}/{table}",0 )]
                print(cooked)
        return  cooked

    # Concrete properties section.
    #

    @property
    def output_data_header( self ) -> str:
        """ SEE: BaseEtl.output_data_header()
        """
        return  BaseEtl.DELIMITER.join( [v for v in ExampleRestToDB.JSON_TO_DB_MAPPING.values() ] )

    #
    # End Interface implementation section
if  __name__ == "__main__":
    pass