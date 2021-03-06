# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
# Author        Changes On  Comment
# ------        ----------  -------
# E Lau         2020-03-28  Initial creation.
"""
The common initialization for all ETLite modules.
The following objects are made available:
    cfg           - The global configuraiton for all to use.
    ETLITE_ENV    - The global variable to indicate the runtime environment.  Should be 'prod' ,'cicd' ,'dev'.
    get_logger()  - The global method to return a logger for all to  use.
"""

import  datetime
import  inspect
import  logging
import  os
import  sys
from    pathlib import Path
from    logging import Logger

# Common initialization section.
#
if 'cfg' not in globals():  # Experimenting with single initialization.
    import  yaml
    from    dotenv  import load_dotenv ,find_dotenv

    load_dotenv( find_dotenv() )
    if 'ETLITE_ENV' in os.environ:
        ETLITE_ENV  =  os.environ['ETLITE_ENV']
    else:
        raise KeyError( "The environment variable ETLITE_ENV is not set.  Set it to either 'dev' ,'cicd' ,'prod' ,'qa'." )

    # Dynamically load config module and assign ETLite Cross DB mapping to a local variable.
    _path2yml = str( sorted( Path( os.getcwd()).glob( '**/ETLite.yaml' )).pop())

    with open( _path2yml ) as fn:    
        ycfg = yaml.load( fn ,Loader=yaml.FullLoader )
        if  ETLITE_ENV  not in  ycfg:
            raise KeyError(f"Value '{ETLITE_ENV}' in variable ETLITE_ENV is not set in ETLite.yaml file." )

    cfg = {}
    # NOTE: Remove the obvious root 'global' node.
    for key in ycfg['global']:
        cfg[ key ] = ycfg['global'][ key ]
    # NOTE: Remove the obvious root environment node.
    for key in ycfg[ ETLITE_ENV ]:
        cfg[ key ] = ycfg[ ETLITE_ENV ][ key ]

    # NOTE: Just trying things out.  May not be needed.
    # Clear out the temporary variables and class objects.
    del(_path2yml )
    del( fn )
    del( key )
    del( ycfg )
    del( yaml )
    del( load_dotenv )
    del( find_dotenv )

# Common routines section.
#
if 'get_logger' not in globals():   # Experimenting with single initialization.
    def get_logger( name:str=None ,log_pathname:str=None ,err_pathname:str=None ,log_dir:str=None ,log_group:str=None ,msg_format:str=None ,dtm_format:str=None ) -> Logger:
        """Return a ETLite standardized logger for you to log your messages.
        Arguments:
            name        - Name for this logger.  Default to the name of the calling module.
            log_pathname- Full path name to the log file.  Will default timestamp into the name.
            err_pathname- Full path name to the err file.  Will default timestamp into the name.
            log_dir     - The root directory for collecting the logs.  Default to 'logs' in your home direcory.
            log_group   - The grouping sub-directory to further organize logs under.
            msg_format  - The logger message format.
            dtm_format  - The timestamp format to be used during logging.

        Return:
            Logger
        """
        if  not log_dir:
            if 'logdir' in cfg['logger']:
                log_dir =  cfg['logger']['logdir']
            else:
                if  sys.platform.find('win') == 0:
                    home = os.environ['HOMEPATH']
                else:
                    home = os.environ['HOME']
                log_dir  = os.path.join( home ,'logs' ) 

        if  not log_group:
            log_group = '.'

        if  not msg_format:
            msg_format = cfg['logger']['msgformat']

        if  not dtm_format:
            dtm_format = cfg['logger']['dtmformat']

        if  not name:
            # Get the name of the caller and NOT this module.
            name = inspect.getmodulename( inspect.stack()[1][1] )
            if  name == '__init__':
                name =  'etlite'

        dtm_fragment = datetime.datetime.utcnow().strftime( cfg['logger']['fragment'] )

        if  not log_pathname:
            log_pathname = os.path.join( log_dir ,log_group ,name +'_' +dtm_fragment +'.log' ) 
        Path( os.path.dirname( log_pathname )).mkdir( parents=True ,exist_ok=True )

        if  not err_pathname:
            err_pathname = os.path.join( log_dir ,log_group ,name +'_' +dtm_fragment +'.err' ) 
        Path( os.path.dirname( err_pathname )).mkdir( parents=True ,exist_ok=True )

        log_formatter = logging.Formatter( msg_format )
        log = logging.getLogger( name )

        if 'ETLITE_LOG_LEVEL' in os.environ:
            log.setLevel( os.environ['ETLITE_LOG_LEVEL'] )
        else:
            if  cfg['logger']['level']:
                try:
                    log.setLevel( {  'DEBUG'    : logging.DEBUG
                                    ,'INFO'     : logging.INFO
                                    ,'WARN'     : logging.WARN
                                    ,'WARNING'  : logging.WARNING
                                    ,'ERROR'    : logging.ERROR
                                    ,'CRITICAL' : logging.CRITICAL
                                }[ cfg['logger']['level'] ])
                except  KeyError:
                    raise KeyError(f"Log level {cfg['logger']['level']} from YMAL configuration is NOT valid!  Use the Python logging level constants." )
            else:
                log.setLevel( logging.INFO )

        log_formatter = logging.Formatter( msg_format )

        # Set up the log handler.
        file_info_handler=logging.FileHandler( log_pathname ,mode='a' )
        file_info_handler.setFormatter( log_formatter )
        file_info_handler.setLevel( logging.INFO )
        log.addHandler( file_info_handler )

        # Set up the err handler.
        file_err_handler=logging.FileHandler( err_pathname ,mode='a' )
        file_err_handler.setFormatter( log_formatter )
        file_err_handler.setLevel( logging.ERROR )
        log.addHandler( file_err_handler )

        if 'TERM' in os.environ or 'TERM_PROGRAM' in os.environ:
            # We are in development mode and not running in the background.
            log.setLevel( logging.DEBUG )

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter( log_formatter )
            log.addHandler( stream_handler )

        return log
