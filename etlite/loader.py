# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
The dynamic ETL class loader.
From the current working directory or a supplied sub-directory, it will scan for all modules that has the
literal 'etl' in the file name and a '.py' file extention.
For each of the found module, an attempt to import it will be attempted.  Once imported, the classes in the
module shall be instantiated and be queried if it is inherited from the BaseETL class.
Those that base inherited from the BaseETL class shall be cached and be ready to be served out by
its case insensitive unique code.

SEE:    https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-packages-or-classes/
        https://www.bnmetrics.com/blog/dynamic-import-in-python3

"""
import  inspect
import  os
import  pathlib
import  sys

from    etlite.common.base_etl          import BaseEtl
from    etlite.common.base_restapi_etl  import BaseRestApiEtl
from    etlite.common.base_sqlapi_etl   import BaseSqlApiEtl

from    importlib.machinery import SourceFileLoader


class   Loader():
    def __init__( self ,cwd:str=None ):
        self._jobs = {}

        if  not cwd:
            cwd = os.getcwd()
        print( f"Current Working Directory: {cwd}" )
        
        file_list = pathlib.Path( cwd ).glob( f'**/*etl*.py' )
        for filename in file_list:
            package = str( filename ).replace( cwd + os.sep ,'' ).replace( os.sep ,'.' )[:-3]
            if  os.path.basename( filename ) != '__init__.py' and not package.startswith( 'etlite' ):
                print( package )

        # pylint: disable=no-value-for-parameter
        #xdb = SourceFileLoader( 'xdb_config' ,_path2cfg ).load_package().xdb_map[db]

    def get_jobs( self ) -> dict:
        return  self._jobs

    def get_job( self ,code:str ) -> BaseEtl:
        return  self._jobs[ code.upper() ]

l = Loader()

