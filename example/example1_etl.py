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

class   Example1Etl( BaseExampleRestApiEtl ):
    """ An example implementtion of an ETL job.
    Our example here is to download 30 stocks data.
    """
    CODE = "EXAMPLE1"
    DOW30= ['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DOW','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','RTX','TRV','UNH','V','VZ','WBA','WMT','XOM' ]

    def __init__( self ):
        super().__init__( Example1Etl.CODE )

    # Private method section
    #

    # Begin Interface implementation section
    #

    # Required step 7.
    def get_datapage_urls( self ) -> list((str,dict,str,dict)):
        """ SEE: BaseRestApiEtl.get_datapage_urls()
        """
        reqs = []
        for symbol  in ExampleEtl.DOW30:
            loopback = self.get_loopback()  # NOTE: In BaseEtl.py
            loopback['task'] = symbol
            reqs.append( (BaseExampleRestApiEtl.STOCK_URL + symbol ,{} ,None ,loopback ) )

        return  reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content:dict ) -> list((str ,int ,str))
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        return  None

    #
    # End Interface implementation section


if '__main__' == __name__:
    import os
    print( os.getcwd() )

    s = Example1Etl()

    from etlite.common.base_etl import BaseEtl
    from etlite.common.base_restapi_etl import BaseRestApiEtl
    if  isinstance( s ,BaseEtl ):
        print( "It is Base ETL")

        if  isinstance( s ,BaseRestApiEtl ):
            print( "It is Base RestApi ETL")

            if  isinstance( s ,BaseExampleRestApiEtl ):
                print( "It is Base Example RestApi ETL")
    else:
        print( "Bummer!" )

    list_of_files = {}
    for( dirpath, dirnames, filenames ) in os.walk( os.getcwd() ):
        for filename in filenames:
            if filename.endswith('_etl.py') and not filename.startswith('test'):
                list_of_files[filename] = os.sep.join([dirpath, filename])
                #if issubclass(fish_class, AnimalBaseClass):
    print( list_of_files )
