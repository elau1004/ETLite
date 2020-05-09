# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
The dynamic ETL class loader.
From the current working directory or a supplied sub-directory, it will scan for all modules that has the
literal 'etl' in the file name and a '.py' file extention.
For each of the found module, an attempt to import it will be performed.  Once imported, the classes in the
module shall be instantiated and be queried if it is inherited from the BaseETL class
and it is not an abstract class.
Those that are inherited from the base BaseETL class shall be cached and be ready to be served out by
its case insensitive unique dataset code.

SEE:    https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-packages-or-classes/
        https://www.bnmetrics.com/blog/dynamic-import-in-python3

"""
import  inspect
import  gettext     # Ready for future internationalization.
i18n =  gettext.gettext
import  os
import  pathlib
import  sys

from    etlite.common import    get_logger
from    etlite.common.base_etl  import BaseEtl
from    etlite.common.base_restapi_etl import BaseRestApiEtl

class   Loader():
    MSG_MODULES_NOT_FOUND = "No ETL Job modules are found from root directory '{dir}'."
    MSG_MODULE_IMPORT_ERR = "Unable to import module '{mod}', ImportError='{err}'."
    MSG_MODULE_SYNTAX_ERR = "Unable to compile module '{mod}', ImportError='{err}'."
    MSG_DUPLICATE_ETL_JOB = "Duplicate Job '{jobcode}' detected in module '{mod}'."
    MSG_INSTANTIATION_ERR = "Unable to intantiate job module '{mod}' due to: '{err}'."
    MSG_INITIALIZATION_ERR= "No ETL Job object discovered during loader initialization from root directory '{dir}'."

    def __init__( self ,cwd:str=None ,logger=None ):
        """
        Loader initialization by instantiating subclasses of BaseETL, and
        saving the instances in internal data structure as cache

        Args:
            cwd         - (Optional). Default is the current working directory.
                          The directory is used as base directory to find modules
                          which contains the classes that need to be instantiated.
            logger      - Reuse the caller's logger.
        Return:
            None
        Exceptions:
            Exception   - Modules not found from the base directory
            ImportError - When unable to import modules
            Exception   - Error creating instances from the discovered classes
            Exception   - Unable to initialize the internal data structure
        """
        # A dictionary to store all created instances
        # using jobcode in upper case as key, object itself as value
        self._jobs = {}
        # Unit test Loader stuff
        self._top_level_dir = None
        self._loading_packages = None

        if  not cwd:
            cwd = os.getcwd()
        if  not logger:
            logger = get_logger()

        logger.debug( f"Current Working Directory: {cwd}" )

        mod_names = []
        file_list = pathlib.Path( cwd ).glob( f'**/*etl*.py' )
        for filename in file_list:
            package = str( filename ).replace( cwd + os.sep ,'' ).replace( os.sep ,'.' )[:-3]
            if  not os.path.basename( filename ).find( 'test' ) >= 0 \
            and not package.startswith( 'etlite' ):
                logger.debug( f"Package: {package}" )
                mod_names.append( package )

        if  not mod_names:
            logger.warning( i18n( Loader.MSG_MODULES_NOT_FOUND ).format( dir=cwd ))
            raise ModuleNotFoundError( i18n( Loader.MSG_MODULES_NOT_FOUND ).format( dir=cwd ))

        # Try to import all discovered modules.
        for mod_name in mod_names:
            module = None
            try:
                __import__( mod_name )  # NOTE: Dynamically import the module.

                # Import successful, resume.
                module= sys.modules[ mod_name ]
                # Get ONLY the ETL specific attributes from the module.
                names = list( filter( lambda attr: attr.lower().find('etl') > 0 ,dir( module )))
                for name  in  names:
                    obj = getattr( module ,name )
                    if  isinstance( obj ,type ) and issubclass( obj ,BaseEtl ) and not inspect.isabstract( obj ):
                        try:
                            if  issubclass( obj ,BaseRestApiEtl ):
                                instance = obj() # dataset_code=None  ,run_id=None ,from_date=None ,upto_date=None )    # Job class found, creating an instance of it.
                            else:
                                raise   NotImplementedError("Framework have NOT implemented your new Transport Type.  Try subclassing from BaseRestApiEtl.")
                        except TypeError as ex:
                            # NOTE: May be legit work in progress, so don't raise an exception.
                            logger.warning( i18n( Loader.MSG_INSTANTIATION_ERR ).format( mod=mod_name ,err=ex ))
                            raise
                        except Exception as ex:
                            # NOTE: May be legit work in progress, so don't raise an exception.
                            logger.warning( i18n( Loader.MSG_INSTANTIATION_ERR ).format( mod=mod_name ,err=ex ))

                        if  instance:
                            code = instance.dataset_code.upper()    # Make it case insensitive.
                            if  code not in self._jobs:
                                self._jobs[ code ] = instance
                            else:
                                # NOTE: May be legit work in progress, so don't raise an exception.
                                logger.warning( i18n( Loader.MSG_DUPLICATE_ETL_JOB ).format( jobcode=code ,mod=mod_name ))

            except SyntaxError as ex:
                logger.warning( i18n( Loader.MSG_MODULE_SYNTAX_ERR ).format( mod=mod_name, err=ex ))

            except ImportError as ex:
                # NOTE: May be legit work in progress, so don't raise an exception.
                logger.warning( i18n( Loader.MSG_MODULE_IMPORT_ERR ).format( mod=mod_name, err=ex ))

        # If the dictionary is still empty, something's got to be wrong here!
        if  not self._jobs:
            logger.error( i18n( Loader.MSG_INITIALIZATION_ERR ).format( dir=cwd ))
            raise NotImplementedError( i18n( Loader.MSG_INITIALIZATION_ERR ))

    # Public methods.
    #

    def get_jobs( self ) -> dict:
        return  self._jobs

    def get_job( self ,code:str ) -> BaseEtl:
        return  self._jobs[ code.upper() ]


# TODO: Move the following into a unit test.
if  __name__ == "__main__":
    loader = Loader()
    jobs   = loader.get_jobs()

    if  jobs:
        job = loader.get_job('EXAMPLE1')
        if  isinstance( job ,BaseEtl ):
            print( f"Job '{job.dataset_code}' is BaseEtl")
            if  isinstance( job ,BaseRestApiEtl ):
                print( f"Job '{job.dataset_code}' is BaseRestApiEtl")
                # TODO: Add 'BaseExampleRestApiEtl' class test.
