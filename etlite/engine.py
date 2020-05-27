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
import random

import  gettext     # Ready for future internationalization.
i18n =  gettext.gettext
import  aiohttp
import  asyncio

from    requests.auth import AuthBase

from    etlite.context  import  RestApiContext
from    etlite.common.exceptions    import  ETLiteException
from    etlite.common.base_restapi_etl  import  BaseRestApiEtl

class   RestApiRequestor():
    """ Single REST API requestor.
    """
    # SEE: Consider the Flyweight pattern.
    #      https://refactoring.guru/design-patterns/flyweight/python/example
    def __init__( self ,ctx:RestApiContext ,headers:dict ,auth_obj:AuthBase ,callback ):
        """
        """
        self._ctx     = ctx
        self._headers = headers    # The HTTP authorization header.
        self._auth_obj= auth_obj   
        self._callback= callback
        self._outputs = {}

    @property
    def context( self ) -> RestApiContext:
        """ The request context.
        """
        return  self._ctx

    @property
    def headers( self ) -> dict:
        """ Return the Authorization HTTP header for the REST API.
        """
        return  self._headers

    @property
    def auth_obj( self ) -> AuthBase:
        """ The authetication object.
        """
        return  self._auth_obj

    async def run( self ) -> bool:
        """
        """
        # TODO: How do I trap exception in async routine.
        async with aiohttp.ClientSession() as client:
            async with client.request(   'GET'
                                        ,'http://www.google.com'
                                        ,params=self._ctx._params
                                        ,data=self._ctx.body        # The data to send in the body of the request.
                                        ,headers=self._ctx.headers
                                        #,auth=
                                        ,compress=True
                                        #,chunked=
                                        #,timeout=
                                    ) as resp:
                self._ctx.status  = resp.status
                self._ctx.reason  = resp.reason
                self._ctx.headers = dict( resp.headers )
                self._ctx.body    = await resp.text()   # TODO: Convert to streaming to reduce memory pressure.
                await asyncio.sleep(random.uniform(0.5, 5))

        result = self._callback( ctx=self._ctx ,content=self._ctx.body )

        if  isinstance( result ,bool ):
            return  result
        else:
            if  isinstance( result ,tuple ):
                if  result[2] not in self._outputs:
                    self._outputs[ result[2]] = []
                self._outputs[ result[2] ].append( result[0] )

        return  True    # maybe not like this

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
        headers  = self._job.request_http_header

        # 1. Authentication step.
        self._auth_url = None
        self._auth_obj = self._job.get_authentication_obj()
        self._auth_req = BaseRestApiEtl.check_url_tuple( self._job.get_authentication_url() )
        if  self._auth_req:
            self._auth_obj = BaseRestApiEtl.check_authentication_obj( self._job.get_authentication_obj() )

            ctx = RestApiContext( method=self._auth_req[0] ,url=self._auth_req[1] ,params=self._auth_req[2] ,body=self._auth_req[3] ,loopback=self._auth_req[4] )
            req = RestApiRequestor( ctx=ctx ,headers=headers ,auth_obj=self._auth_obj ,callback=self._job.put_authentication_resp )
            if  not req.run():
                raise RuntimeError()

        # 2. Offline batch data request step.
        self._queue_req = BaseRestApiEtl.check_url_tuple( self._job.get_data_request_url() )
        if  self._queue_req:
            ctx = RestApiContext( method=self._queue_req[0] ,url=self._queue_req[1] ,params=self._queue_req[2] ,body=self._queue_req[3] ,loopback=self._queue_req[4] )
            req = RestApiRequestor( ctx=ctx ,headers=headers ,auth_obj=self._auth_obj ,callback=self._job.put_data_request_resp )
            if  not req.run():
                raise RuntimeError()

        # 3. Offline batch data status check step.
        self._status_req = BaseRestApiEtl.check_url_tuple( self._job.get_request_status_url() )
        if  self._status_req:
            ctx = RestApiContext( method=self._status_req[0] ,url=self._status_req[1] ,params=self._status_req[2] ,body=self._status_req[3],loopback=self._status_req[4] )
            req = RestApiRequestor( ctx=ctx ,headers=headers ,auth_obj=self._auth_obj ,callback=self._job.put_request_status_resp )

            b = asyncio.run( req.run() )
            if  not b:
                raise RuntimeError()

        # 4. Retrieve data step.
        while True:
            self._rest_reqs:list = BaseRestApiEtl.check_url_tuples( self._job.get_datapage_urls() )
            if  self._rest_reqs:
                reqs = []
                for i, rest_req in enumerate( self._rest_reqs ,start=0 ):
                    ctx = RestApiContext( ordinal=i ,method=rest_req[0] ,url=rest_req[1] ,params=rest_req[2] ,body=rest_req[3] ,loopback=rest_req[4] )
                    ctx.loopback['ordinal'] = i
                    reqs.append( RestApiRequestor( ctx=ctx ,headers=headers ,auth_obj=self._auth_obj ,callback=self._job.put_datapage_resp ))

                # SEE:  https://xinhuang.github.io/posts/2017-07-31-common-mistakes-using-python3-asyncio.html
                loop    = asyncio.get_event_loop()
                tasks   = [ reqs[i].run() for i in range(0 ,len(reqs)) ]
                group1  = asyncio.gather( *tasks )
                results = loop.run_until_complete( group1 )
                print( results )
            else: # None value terminate this loop.
                break

if  __name__ == "__main__":
    from example.example1_etl  import  Example1Etl

    try:
        jb = Example1Etl()
        wf = RestWorkflowExecutor( jb )
        wf.run()
    except  Exception as ex:
        print( ex )
