# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
This is an abstract base class that defines the workflow interface for a REST API.
The outer framework shall have a dialog with your extended class.
If the getter method return a None value, that step and its corresponding put shall be skipped.
The dialog follows the following pattern:
    1. Framework ask for a value by "getting" the property from your class.
    2. Framework does the heavy lifting on behalf of your job.
    3. Framework put(set) the result back to you to process.
       Put implies that you have to do some work and not just storing it away.

Any properties are deemed common to REST API shall be added in this class.

The REST api I/O shall be handled by the ETLite framework.  The stream data shall be read and
each raw record shall be passed to the concrete object to be transformed.  A cooked/formmated
record shall be return back to the framework.  The returned cooked data shall be written out to
a cloud bucket like S3.

The 3 big I/O; Web, S3, and DB are abstracted out from your concrete class
to be handled by the ETLite framework.  What is left for the concrete class
to do is to transform and prepare the data to be loaded into your data warehouse.
"""

import  collections

from  abc           import abstractmethod
from  aiohttp       import ClientResponse
from  aiohttp.hdrs  import METH_GET ,METH_POST
from  datetime      import datetime as datetime
from  requests.auth import AuthBase

from  etlite.context    import  RestApiContext
from  etlite.common.base_etl    import BaseEtl

class   BaseRestApiEtl( BaseEtl ):
    """ The base abstract REST ETL Job object.
        It holds more REST specific contextual properties and define the generic REST workflow.
    """
    CLIENT_TIMEOUT = 300    # Default to 5 minutes before timing out.

    def __init__( self ,dataset_code:str ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( dataset_code=dataset_code ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )

        self._auth_token:str      = None
        self._request_token:str   = None
        self._request_timeout:int = BaseRestApiEtl.CLIENT_TIMEOUT
        # REST API workflow.
        if  self._workflow_seq:
            self._workflow_seq   += "R" 
        else:
            self._workflow_seq    = "R"

    # Static utility section.
    #
    @staticmethod
    def check_url_tuple( url_tuple:tuple ) -> (str,str,dict,str,dict):
        """ Validate that the URL request tuple conform to the expected types and values.
        """
        if  url_tuple:
            if  url_tuple[0]:
                if  not isinstance( url_tuple[0] ,str ):
                    raise TypeError()
                else:
                    if  not url_tuple[0] in { METH_GET ,METH_POST }:
                        raise ValueError()
            else:
                raise ValueError()

            if  url_tuple[1]:
                if  not isinstance( url_tuple[1] ,str ):
                    raise TypeError()
                else:
                    if  not str(url_tuple[1]).startswith('http') >= 0:
                        raise ValueError()
            if  url_tuple[3]:
                if  not isinstance( url_tuple[3] ,str ):
                    raise TypeError()

            if  url_tuple[4]:
                if  not isinstance( url_tuple[4] ,dict ):
                    raise TypeError()
                else:
                    if  not('task' in url_tuple[4] or 'ordinal' in url_tuple[4]):
                        raise ValueError()
            else:
                raise ValueError()
            
        return  url_tuple

    @staticmethod
    def check_url_tuples( url_tuples:list ) -> list((str,dict,str,dict)):
        """ Validate that the list of URL tuples conform to the expected types.
        """
        url_reqs = []
        if  url_tuples:
            for url_tuple in url_tuples:
                url_reqs.append( BaseRestApiEtl.check_url_tuple( url_tuple ))
        return  url_reqs

    @staticmethod
    def check_authentication_obj( auth_obj:object ) -> AuthBase:
        """ Validate that the authentication object conform to the expected subclass of AuthBase.
        """
        if  auth_obj:
            if  not isinstance( auth_obj ,AuthBase ):
                raise   TypeError()

        return  auth_obj


    # Abstract interface section.
    #

    # Optional step 1a.
    @abstractmethod
    def get_authentication_url( self ) -> (str,dict,str,dict):
        """ If there is a different URL to authenthicate at then return a tuple of URL pertinent data,
        else return None to skip.

        Return:
            A tuple of:
                str - URL.  The authentication end point.
                dict- Parameters.  The URL parameters to be converted into a query string.
                str - Message body.  The text to be accompanied in the HTTP request  body.
                dict- Loopback freeform dictionary.  This dictionary will be returned back in the response context.
        """
        pass

    # Optional step 1b.
    @abstractmethod
    def get_authentication_obj( self ) -> AuthBase:
        """ If the authentication requires an Auth object then return the AuthBase,
        else return None to skip.

        SEE: https://www.geeksforgeeks.org/authentication-using-python-requests/

        Return:
            AuthBase - The base Auth class where other authentication subclass from.
        """
        pass

    # Optional step 2.
    @abstractmethod
    def put_authentication_resp( self ,ctx:RestApiContext ,content ) -> bool:
        """ The response for the previous get_authentication_url() call is put to you.
        Query the content to determine if you are authenticated.
        Usually you need to save your auth token.
        You should do the mininum to figure out if the request is good.

        Args:
            RestApiContext - The REST API context.
            str - The response content.
        Return:
            bool- True if successfully processed else False.
        """
        pass

    # Optional step 3.
    @abstractmethod
    def get_data_request_url( self ) -> (str,dict,str,dict):
        """ If there is a different URL to request a set of data then return the URL,
        else return None to skip.

        Return:
            A tuple of:
                str - URL.  The authentication end point.
                dict- Parameters.  The URL parameters to be converted into a query string.
                str - Message body.  The text to be accompanied in the HTTP request  body.
                dict- Loopback freeform dictionary.  This dictionary will be returned back in the response context.
        """
        pass

    # Optional step 4.
    @abstractmethod
    def put_data_request_resp( self ,ctx:RestApiContext ,content ) -> bool:
        """ The response for the previous get_data_request_url() call is put to you.
        Query the content to determine if a request token/id is returned
        to back to you for future use.
        You should do the mininum to figure out if the request is good.

        Args:
            RestApiContext - The REST API context.
            str            - The response content.
        Return:
            bool- True if successfully processed else False.
        """
        pass

    # Optional step 5.
    @abstractmethod
    def get_request_status_url( self ) -> (str,dict,str,dict):
        """ If there is a different URL to check on a request for set of data then return the URL,
        else return None to skip to the next step.

        Return:
            A tuple of:
                str - URL.  The authentication end point.
                dict- Parameters.  The URL parameters to be converted into a query string.
                str - Message body.  The text to be accompanied in the HTTP request  body.
                dict- Loopback freeform dictionary.  This dictionary will be returned back in the response context.
        """
        pass

    # Optional step 6.
    @abstractmethod
    def put_request_status_resp( self ,ctx:RestApiContext ,content ) -> bool:
        """ The response for the previous get_request_status_url() call is put to you.
        Query the content to determine if a request data set is ready to download.
        You should do the mininum to figure out if the request is good.

        Args:
            RestApiContext - The REST API context.
            str - The response content.
        Return:
            bool- True if successfully processed else False.
        """
        pass

    # Required step 7.
    @abstractmethod
    def get_datapage_urls( self ) -> list((str,str,dict,str,dict)):
        """ If you determine that more data pages are needed then return the list of tuples.
        else return None to skip/terminate.

        This method shall be called multiple times for a list of URLs until you return None to terminate.

        Return:
            A list of tuple of:
                str - HTTP Method. Either 'GET' or 'POST'.
                str - URL.  The authentication end point.
                dict- Parameters.  The URL parameters to be converted into a query string.
                str - Message body.  The text to be accompanied in the HTTP request  body.
                dict- Loopback freeform dictionary.  This dictionary will be returned back in the response context.
        """
        pass

    # Required step 8.
    @abstractmethod
    def put_datapage_resp( self ,ctx:RestApiContext ,content ) -> list((str ,int ,str)):
        """ The response for the previous get_datapage_urls() call is put to you.
        Query the content to determine if there are more pages to download.
        You should do the mininum to figure out if the request is good.
        This is may be the main method where you process the requested data.

        This method shall be called multiple times depending on the number of the entries
        in the list returned from get_datapage_urls().

        Args:
            RestApiContext - The REST API context.
            str/dict       - The content either as JSON dictionary or a CSV string.
        Return:
            A list of tuple of:
                str - The cleansed and processed output record.
                int - The return code to communicate the status of the processing.
                        0 - successful
                        1 - encountered issue with the data. Retry again.
                str - The name of a output stream to direct this record into.
                      This is usually the name of a file URI.
        """
        pass

    # TODO: Flesh out the remaining abstract methods.

    # Concrete properties section.
    #

    @property
    def request_http_header( self ) -> dict:
        """ If your request require a different headers, you MUST over write this property
        to provide your implmentation.
        """
        return { "content-type": "application/json; charset=utf-8" }

#   @property
#   def request_body_mesage( self ) -> str:
#       """ If your request require a message body data, you MUST over write this method
#       to provide your implmentation.
#       """
#       return  None

    @property
    def auth_token( self ) -> str:
        """ An original authentication token that was provided by the vendor.
        This is to be used to prove taht you have been authenticate.
        """
        return  self._auth_token

    @auth_token.setter
    def auth_token( self ,value:str ):
        self._auth_token =value

    @property
    def request_token( self ) -> str:
        """ An original token that was provided by the vendor for your requested data set.
        This is to be used to check on the status of your requested data.
        """
        return  self._request_token

    @request_token.setter
    def request_token( self ,value:str ):
        self._request_token =value

    @property
    def request_timeout( self ) -> int:
        """ A default timeout for a client request.
        """
        return  self._request_timeout

    @request_timeout.setter
    def request_timeout( self ,value:int ):
        self._request_timeout =value
