# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
The engine to orchestrate job executions.
The orchestration is define as DAG of collections notated using the following brackets:
    [] - A list of jobs to be executed in sequence.
    {} - A set  of jobs to be executed in parallel threads on a single CPU core.
    () - A set  of jobs to be executed in parallel across all CPU cores.

Job entries in a collection are case in-sensitive and unique in the entire DAG.
Python modules shall be dynamicall discover and be matched to these job codes/entires.
Sequential processing is dependend all of previous jobs execution to be successful to proceed.

Example:
    [ a ,b ,{c ,d ,[e ,f ,(g,h,i)]} ,j ,({k,l} ,{m,n,[o,p,q]}) ,r ]
"""
# pylint: disable=line-too-long
# pylint: disable=C0103,C0326,C0330

import  gettext     # Ready for future internationalization.
i18n =  gettext.gettext

from    requests.auth import AuthBase

from    etlite.context  import  RestApiContext
from    etlite.common.exceptions    import  ETLiteException
from    etlite.common.base_restapi_etl  import  BaseRestApiEtl

class   RestApiRequestor():
    """
    """
    def __init__( self ,ctx:RestApiContext ,header:dict ,auth_obj:AuthBase ,callback ):
        """
        """
        self._ctx     = ctx
        self._header  = header     # The HTTP authorization header.
        self._auth_obj= auth_obj   
        self._callback= callback
        self._outputs = {}

    @property
    def context( self ) -> RestApiContext:
        """ The request context.
        """
        return  self._ctx

    @property
    def header( self ) -> dict:
        """ Return the Authorization HTTP header for the REST API.
        """
        return  self._header

    @property
    def auth_obj( self ) -> AuthBase:
        """ The authetication object.
        """
        return  self._auth_obj

    def run( self ) -> bool:
        """
        """
        # TODO: Make the async request using the info in the context object.
        #       Fill in the ctx with the response info.
        #       Extract out the content for the callback method.
        result = self._callback( ctx=self._ctx ,content=None )

        if  isinstance( result ,bool ):
            return  result
        else:
            if  isinstance( result ,tuple ):
                if  result[2] not in self._outputs:
                    self._outputs[ result[2]] = []
                self._outputs[ result[2] ].append( result[0] )

        return  True

class   BaseExecutor():
    pass

class   RestWorkflowExecutor( BaseExecutor ):
    """
    """ 
    def __init__( self ,job:BaseRestApiEtl ):
        """
        """
        self._job = job

    def run( self ):
        """
        """
        header  = self._job.request_http_header
        auth_obj= self._job.get_authentication_obj

        # 1. Authentication step.
        self._auth_url = None
        self._auth_obj = None
        self._auth_req = BaseRestApiEtl.check_url_tuple( self._job.get_authentication_url() )
        if  self._auth_req.url:
            self._auth_obj = BaseRestApiEtl.check_authentication_obj( self._job.get_authentication_obj() )

            ctx = RestApiContext( ordinal=0 ,url=self._auth_req[0] ,params=self._auth_req[1] ,body=self._auth_req[2] ,loopback=self._auth_req[3] )
            req = RestApiRequestor( ctx=ctx ,header=header ,auth_obj=auth_obj ,callback=self._job.put_authentication_resp )
            if  not req.run():
                raise RuntimeError()

        # 2. Offline batch data request step.
        self._queue_req = BaseRestApiEtl.check_url_tuple( self._job.get_data_request_url() )
        if  self._queue_req.url:
            ctx = RestApiContext( ordinal=0 ,url=self._queue_req[0] ,params=self._queue_req[3] ,body=self._queue_req[2] ,loopback=self._queue_req[3] )
            req = RestApiRequestor( ctx=ctx ,header=header ,auth_obj=auth_obj ,callback=self._job.put_data_request_resp )
            if  not req.run():
                raise RuntimeError()

        # 3. Offline batch data status check step.
        self._status_req = BaseRestApiEtl.check_url_tuple( self._job.get_request_status_url() )
        if  self._status_req.url:
            ctx = RestApiContext( ordinal=0 ,url=self._status_req[0] ,params=self._status_req[1] ,body=self._status_req[2],loopback=self._status_req[3] )
            req = RestApiRequestor( ctx=ctx ,header=header ,auth_obj=auth_obj ,callback=self._job.put_request_status_resp )
            if  not req.run():
                raise RuntimeError()

        # 4. Retrieve data step.
        while True:
            self._data_reqs:list = BaseRestApiEtl.check_url_tuples( self._job.get_datapage_urls() )
            if  self._data_reqs:
                reqs = []
                for i, data_req in enumerate( self._data_reqs ,start=0 ):
                    ctx = RestApiContext( ordinal=i ,url=data_req[0] ,params=data_req[1] ,body=data_req[2] ,loopback=data_req[3] )
                    reqs.append( RestApiRequestor( ctx=ctx ,header=header ,auth_obj=auth_obj ,callback=self._job.put_datapage_resp ))

                # TODO: Parallel request the list.
            else: # None value terminate this loop.
                break


if  __name__ == "__main__":
    pass