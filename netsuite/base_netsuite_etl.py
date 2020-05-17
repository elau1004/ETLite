# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from  abc       import  ABC, abstractmethod
from  datetime  import  datetime as datetime

from  etlite.context    import  RestApiContext
from  etlite.common.base_restapi_etl    import BaseRestApiEtl
from  etlite.common.constants           import HTTP_GET

class   BaseNetsuiteEtl( BaseRestApiEtl ):
    """ The base Netsuite REST ETL Job object.
        It implements most of the common abstract REST methods that define the generic REST workflow.
        All common sharable Netsuite stuff should be placed in here.
    """
    BASE_API_URI   = "https://{acct_number}.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
    BASE_URI_PARAM = { "script": 862 ,"deploy": 1 ,"searchid": 0 ,"frompage": 1 ,"topage": 20 }     # Generic Netsuite request parameters.  You need to add more to it.
    PAGE_SIZE      = 20
    CLIENT_TIMEOUT = 330    # Netsuite has a 5 minutes server timeout.  We are going to use a 5'30" client timeout.

    def __init__( self ,dataset_code:str ,run_id:int ,filter_on:str ,from_date:datetime  ,upto_date:datetime ,*args ,**kwargs ):
        super().__init__( dataset_code=dataset_code  ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )

        # TODO: Populate from YMAL/Vault.
        self._acct_number   = None
        self._acct_signature= None
        self._auth_email    = None
        #
        self._searchid      = None
        self._internal_ids  = None          # Comma seperate values.  Should keep it to approx max of 500 values for it is passed in the URL.
        self._filter_on     = filter_on     # Netsuite object field to apply te filtering on.  Dates values are in the parent object.
        self._request_url   = BaseNetsuiteEtl.BASE_API_URI.format( acct_number=self._acct_number )

        # Bubble up to parent property.
        self.request_timeout= BaseNetsuiteEtl.CLIENT_TIMEOUT


    # Begin Interface implementation section
    #

    def get_authentication_url( self ) -> (str,dict,str,dict):
        """ SEE: BaseRestApiEtl.get_authentication_url()
        Not supported by Netsuite.
        """
        return  None

    def get_authentication_obj( self ) -> object:
        """ SEE: BaseRestApiEtl.get_authenticator()
        Not supported by Netsuite.
        """
        return  None

    # Optional step 2.
    def put_authentication_resp( self ,ctx:RestApiContext ,content ) -> bool:
        """ SEE: BaseRestApiEtl.put_authentication_resp()
        Not supported by Netsuite.
        """
        return  True

    # Optional step 3.
    def get_data_request_url( self ) -> (str,dict,str,dict):
        """ SEE: BaseRestApiEtl.get_data_request_url()
        Not supported by Netsuite.
        """
        return  None

    # Optional step 4.
    def put_data_request_resp( self ,ctx:RestApiContext ,content ) -> bool:
        """ SEE: BaseRestApiEtl.put_data_request_resp()
        Not supported by Netsuite.
        """
        return  True

    # Optional step 5.
    def get_request_status_url( self ) -> (str,dict,str,dict):
        """ SEE: BaseRestApiEtl.get_request_status_url()
        Not supported by Netsuite.
        """
        return  None

    # Optional step 6.
    def put_request_status_resp( self ,ctx:RestApiContext ,content ) -> bool:
        """ SEE: BaseRestApiEtl.put_request_status_resp()
        Not supported by Netsuite.
        """
        return  True

    # Required Step 7 and 8 is to be implemented by specific Netsuite jobs.
    #

    # Concrete properties section.
    #

    @property
    def init_date( self ) -> datetime:
        """ Return the very first initial date/time.
        This property implements the abstract property defined in the parent class.
        """
        return  datetime( 2011 ,2 ,1 )

    @property
    def request_http_header( self ) -> dict:
        """ Common HTTP header to be shared by all the Netsuite datasets.
        This property overwrote the parent default property.
        """
        return  {'content-type': 'application/json','Authorization':f'NLAuth nlauth_account={self._acct_number},nlauth_email={self._auth_email},nlauth_signature={self._acct_signature},nlauth_role=1090'}

    #
    # End Interface implementation section

    # Start of extended Netsuite specific properties.
    #

    @property
    def request_params( self ) -> dict:
        """ Return another copy of the generic request parameters to be augmented so to be isolated from other threads.
        """
        return  BaseNetsuiteEtl.BASE_URI_PARAM.copy()

    def get_requests( self ,search_id:int ,filter_on:str ,from_date:datetime ,upto_date:datetime ,from_page:int=1 ,upto_page:int=20 ,step=20 ,loopback:dict=None ) -> list((str,dict,str,dict)):
        """ Return a list of REST requests for the framework to execute.

        Return:
            A list of tuples of:
                str - HTTP Method. Either 'GET' or 'POST'.
                str - URL.  The authentication end point.
                dict- Parameters.  The URL parameters to be converted into a query string.
                str - Message body.  The text to be accompanied in the HTTP request  body.
                dict- Loopback freeform dictionary.  This dictionary will be returned back in the response context.
                        The minimum keys are:
                            task    - The name of the task.
                            ordinal - The sequence number of this request in the list.
        """
        reqs    = []
        params  = self.request_params
        params[ 'searchid' ] = search_id
        f = 0
        if  self._internal_ids:
            f += 1
            params[ f'field{f}'   ] = 'internalid'
            params[ f'operator{f}'] = 'anyof'
            params[ f'field{f}a'  ] = self._internal_ids

        if  filter_on:
            f += 1
#           params[ f'join{f}'    ] = self._join_to
            params[ f'operator{f}'] = 'onorafter'
            params[ f'field{f}a'  ] = from_date.strftime("%m/%d/%Y %I:%M %p"), # Date format is NOT negotiable!  Value is ib parent object.
            f += 1
#           params[ f'join{f}'    ] = self._join_to
            params[ f'field{f}'   ] = filter_on
            params[ f'operator{f}'] = 'before'
            params[ f'field{f}a'  ] = upto_date.strftime("%m/%d/%Y %I:%M %p"), # Date format is NOT negotiable!  Value is ib parent object.

        for page_from in range( from_page ,upto_page ,step ):
            param = params.copy()
            param[ 'from_page'] = page_from
            param[ 'upto_page'] = page_from + step

            if  loopback:
                ctxback = loopback.copy()
            else:
                ctxback = self.get_loopback()   # Does make a copy.
            ctxback['from_page'] = param['from_page']
            ctxback['upto_page'] = param['upto_page']
            ctxback['ordinal'  ] = page_from // step

            reqs.append( (HTTP_GET ,self._request_url ,param ,None ,ctxback) )

        return reqs

    def throttle_up( self ) ->(int,int):
        """ Throttle down the pagination.

        Return:
            int - the count of pages to request.
            int - the ceiling of the max pages to request.
        """
        return None, None

    def throttle_down( self ) ->(int,int):
        """ Throttle down the pagination.

        Return:
            int - the count of pages to request.
            int - the ceiling of the max pages to request.
        """
        return None, None

    #
    # End of Netsuite properties.
