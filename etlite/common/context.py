# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

class   Context():
    """ The base workflow response context object.
        It holds some basic contextual properties to convey back to the Job by the framework.
    """
    def __init__( self ,ordinal:int ,loopback:dict ):
        self._ordinal:int   = ordinal     # A sequential number starting from zero.
        self._loopback:dict = loopback    # A dictionary to be returned back to the caller for house keeping.

    @property
    def ordinal( self ) -> int:
        """ Return the unique ordinal number of this executor.
        """
        return  self._ordinal

    @property
    def loopback( self ) -> dict:
        """ Return the pass through loopback house keeping dictionary back to the caller.
        """
        return  self._loopback


class   RestApiContext( Context ):
    """ The REST API workflow response context object.
        It holds more REST specific contextual properties to convey back to the Job by the framework.
    """
    def __init__( self ,url:str ,params:dict={} ,body:str=None ,ordinal:int=0 ,loopback:dict={} ):
        super().__init__( self ,ordinal=ordinal ,loopback=loopback )

        self._url:str     = url     # The REST endpoint.
        self._params:dict = params  # Query strin parametes to be appended to the URL.
        self._body:str    = None    # The message to be POSTed in the request body .
        self._status:int  = None    # The returned response HTTP status.
        self._reason:str  = None    # The returned response failure reason/message.

    @property
    def url( self ) -> str:
        """ Return the url for the REST API.
        """
        return  self._url

    @property
    def params( self ) -> dict:
        """ Return the URL parameters used for the REST API.
        """
        return  self._params

    @property
    def body( self ) -> str:
        """ Return the HTTP body message used for the REST API.
        """
        return  self._body


    @property
    def status( self ) -> int:
        """ Return the status returned from the REST API response.
        """
        return  self._status

    @status.setter
    def status( self ,value:int ):
        """ Set the status of the REST API response.
        """
        self._status = value

    @property
    def reason( self ) -> str:
        """ Return the reason message corresponding to the status code.
        """
        return  self._reason

    @reason.setter
    def reason( self ,value:str ):
        """ Set the reason message corresponding to the status code.
        """
        self._reason = value
