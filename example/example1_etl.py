# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  os
import  sys
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/example.

from    aiohttp import ClientResponse
from    etlite.common.base_etl  import  BaseEtl
from    example.base_example_restapi_etl  import  BaseExampleRestApiEtl

class   Example1Etl( BaseExampleRestApiEtl ):
    CODE = "EXAMPLE1"

    def __init__( self ):
        super().__init__( Example1Etl.CODE )

    # Private method section
    #

    
    # Begin Interface implementation section
    #

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
        return  BaseExampleRestApiEtl.STOCK_URL + "IBM"

    # Required step 8.
    def put_next_datapage_resp( self ,resp:ClientResponse ):
        pass

    # Properties section
    #

    def raw_filepath( self ) -> str:
        return  None

    def latest_filepath( self ) -> str:
        return  None

    def archive_filepath( self ) -> str:
        return  None

    def output_data_header( self ) -> str:
        return None

    def transform_data( self ,record:str ,delimiter:str=BaseEtl.DELIMITER ) -> str:
        return None

    def source_table( self ) -> str:
        pass

    def source_columns( self ,columns:list ) -> list:
        pass

    def target_columns( self ,columns:list ) -> list:
        pass

    def stage_query( self ) -> str:
        pass

    def insert_query( self ) -> str:
        pass

    def update_query( self ) -> str:
        pass

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
