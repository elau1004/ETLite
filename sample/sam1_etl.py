# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  os
import  sys
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/sample.

from    sample.base_sample_restapi_etl  import  BaseSampleRestApiEtl

class   Sam1Etl( BaseSampleRestApiEtl ):
    CODE = "SAM1"

    def __init__( self ):
        super().__init__( Sam1Etl.CODE )

    # Example to implement the abstract method.
    def abs_method( self ):
        pass

if '__main__' == __name__:
    import os
    print( os.getcwd() )

    s = Sam1Etl()

    from etlite.common.base_etl import BaseEtl
    if isinstance( s ,BaseEtl ):
        print( "It is Base ETL")
    else:
        print( "Bummer" )

    list_of_files = {}
    for( dirpath, dirnames, filenames ) in os.walk( os.getcwd() ):
        for filename in filenames:
            if filename.endswith('_etl.py') and not filename.startswith('test'):
                list_of_files[filename] = os.sep.join([dirpath, filename])
                #if issubclass(fish_class, AnimalBaseClass):
    print( list_of_files )
