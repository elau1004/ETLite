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
    #   method:str
    #   url:str
    #   params:dict
    #   data:dict    for multipart/form-data and application/x-www-form-urlencoded body
    #   headers:dict
    #   auth:aiohttp.BasicAuth
    #   compress:bool
    #   timeout:int 
    #   
    def __init__( self ,method:str ,url:str ,headers:dict={} ,params:dict={} ,body:str=None ,ordinal:int=0 ,loopback:dict={} ):
        super().__init__( ordinal=ordinal ,loopback=loopback )

        self._method:str  = method  # HTTP method to use to make the request.
        self._url:str     = url     # The REST endpoint.
        self._headers:dict= headers # HTTP Headers to send with the request.
        self._params:dict = params  # Key/Value pairs dictionary to be sent as parameters in the query string of the new request.
        self._body:str    = None    # The data to send in the body of the request.
        self._status:int  = None    # The returned response HTTP status.
        self._reason:str  = None    # The returned response failure reason/message.

    @property
    def method( self ) -> str:
        """ Return the method to make the REST request.
        """
        return  self._method

    @property
    def url( self ) -> str:
        """ Return the url for the REST API request.
        """
        return  self._url

    @property
    def headers( self ) -> dict:
        """ Return the header for the REST API request/response.
        """
        return  self._headers

    @headers.setter
    def headers( self ,value:dict ):
        """ Set the headers of the REST API response.
        """
        self._headers = value

    @property
    def params( self ) -> dict:
        """ Return the URL parameters used for the REST API request.
        """
        return  self._params

    @params.setter
    def params( self ,value:dict ):
        """ Set the params of the REST API request.
        """
        self._params = value

    @property
    def body( self ) -> str:
        """ Return the HTTP body message used for the REST API response.
        """
        return  self._body

    @body.setter
    def body( self ,value:str ):
        """ Set the body data of the REST API request/response.
        """
        self._body = value

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

