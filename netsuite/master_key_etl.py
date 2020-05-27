# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
import  dateutil.rrule  as  rrule

from    abc      import ABC, abstractmethod
from    datetime import timedelta ,datetime as  datetime
from    logging  import Logger

from    etlite.context  import  RestApiContext
from    etlite.common   import  get_logger
from    etlite.common.base_etl  import  BaseEtl

from    netsuite.base_netsuite_etl  import  BaseNetsuiteEtl

class   MasterKeyJob( BaseNetsuiteEtl ):
    """ The specific Netsuite REST ETL Job (MASTERKEY).
        The master key job to transfer the unique keys from the following Netsuite tables:
            - Sales Order Detail
            - Purchase Order Detail
            - Purchase Order Approval Routes

    """
    CODE = 'netsuite_deletion_detection_to_dwh'
    JSON_TO_DB_MAPPING = {
        "Line_No": "Line_No",                               # 1 NOT to be loaded.
        "Internal ID": "Internal_ID",                       # 2
        "PO Internal ID": "PO_Internal_ID",                 # 3
        "Date Created": "Date_Created",                     # 4
        "Date Deleted": "Date_Deleted",                     # 5
        "Last Modified": "Last_Modified_Date",              # 6
        "Line Last Modified": "Line_Last_Modified_Date",    # 7
        "Line ID": "Line_ID",                               # 8
        "Sequence": "Sequence",                             # 9
        "Header Amount": "Header_Amount",                   # 10
        "Detail Amount": "Detail_Amount",                   # 11    Pre-Discount/PO_Line_Amount
        "Amount Foreign Currency": "Detail_Amount_FX"       # 12
    }

    def __init__( self,
                  run_id:int,
                  filter_on:str='datecreated',
                  from_date:datetime=datetime.utcnow() + timedelta(days=-1),
                  upto_date:datetime=datetime.utcnow(),
                  join_to:str=None,
                  logger:Logger=None ):

        super().__init__( MasterKeyJob.CODE ,run_id=run_id ,filter_on=filter_on ,from_date=from_date ,upto_date=upto_date )

        self._header_caption= None
        self._total_pages   = None
        self._tasks_stack = [
            {   "object"      : "Sale Order Detail",
                "search_id"   : 4659,
                "table_code"  : "dd_so_lns",
                "filter_on"   : "datecreated"
            },
            {   "object"      : "Purchase Order Detail",
                "search_id"   : 4658,
                "table_code"  : "dd_po_lns",
                "filter_on"   : "datecreated"
            },
            {   "object"      : "Purchase Order Approval Routes",
                "search_id"   : 4660,
                "table_code"  : "dd_po_apr",
                "filter_on"   : "created"
            }
        ]
        if  logger:
            self.logger = logger
        else:
            self.logger = get_logger

        # Initialize the date ranges.
        self._date_ranges = list(rrule.rrule( dtstart=from_date ,until=upto_date ,freq=rrule.MONTHLY ,interval=4 ))
        if  upto_date > self._date_ranges[-1]:
            self._date_ranges.append( upto_date )

        self._dates_stack  = self._date_ranges.copy()

    # Begin Interface implementation section
    #

    # Required step 7.
    def get_datapage_urls( self ) -> list((str,dict,str,dict)):
        """ SEE: BaseRestApiEtl.get_datapage_urls()
        """
        # We cannot use a loop in this method.  Each iteration need to return a list of request.
        # Iteration shall be implemented as stack.  When the stack is empty we are done.
        rest_reqs = None
        if  self._tasks_stack:
            if  self._dates_stack:
                if  not self._total_pages: # NOTE: Set in put_datapage_resp().
                    # New object request.
                    from_page = 1
                    upto_page = BaseNetsuiteEtl.PAGE_SIZE
                    from_date = self._dates_stack[0]
                    upto_date = self._dates_stack[1]
                    del self._dates_stack[0] # Pop the dates stack.
                else:
                    # TODO: Need to check if we are done.
                    from_page = BaseNetsuiteEtl.PAGE_SIZE +1
                    upto_page = self._total_pages
                    self._total_pages = None

                search_id       = self._tasks_stack[0]['search_id']
                filter_on       = self._tasks_stack[0]['filter_on']
                loopback        = self. get_loopback()
                loopback['task']= self._tasks_stack[0]['search_id']
                loopback.update({"filter_on":filter_on ,"from_date":from_date ,"upto_date":upto_date ,"from_page":from_page ,"upto_page":upto_page})

                if  len(self._dates_stack) == 1: # Reset the stack.
                    del self._tasks_stack[0]     # Pop the tasks stack.
                    if  self._tasks_stack:
                        self._dates_stack  = self._date_ranges.copy()

                rest_reqs = self.get_requests(search_id=search_id
                                        ,filter_on=filter_on
                                        ,from_date=from_date
                                        ,upto_date=upto_date
                                        ,from_page=from_page
                                        ,upto_page=upto_page
                                        ,step=BaseNetsuiteEtl.PAGE_SIZE
                                        ,loopback=loopback )
                                
        return  rest_reqs

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content:dict ) -> list((str ,int ,str)):
        """ SEE: BaseRestApiEtl.put_datapage_resp()
        """
        output_line = None
        if 'Internal ID'  in content:
            # Happy path.
            # TODO: Flatten the data into a string.
            pass
        elif 'No of Pages Requested' in content:
            # First entry of the returned JSON is:
            # {'StatusCompleted': 'NO' ,'No of Pages Requested': '1-10 of 212' ,'No of Results Obtained': 10000 ,'Total No of Results': 211358}
            # {"StatusCompleted":"YES" ,"No of Pages Requested": "1-1 of 0"    ,"No of Results Obtained": 0     ,"Total No of Results": 0}
            self._total_pages = content['No of Pages Requested'].split(' ')[2]
        elif 'error' in content and 'code' in content['error'] and 'message' in content['error']:
            # First entry of the returned JSON if the endpoint time-out is:
            # {"error" : {"code" : "SSS_REQUEST_LIMIT_EXCEEDED" ,"message" : "Request Limit Exceeded!"}}
            # {"error" : {"code" : "UNEXPECTED_ERROR"           ,"message" : "The account you are trying to access is experiencing some system issues. ... "}}

            # TODO: Figure out what I want to do in this situation.
            pass
        else:
            raise TypeError( f"Unrecognize type '{content}' passed in by the framework!")

        return  [ (output_line ,0 ,None) ]

    # Concrete properties section.
    #

    @property
    def output_data_header( self ) -> str:
        """ Return the header caption for the output text file.
        """
        # Prepare the first header line.
        if  not self._header_caption:
            tokens = [ MasterKeyJob.JSON_TO_DB_MAPPING[ key ] for key in MasterKeyJob.JSON_TO_DB_MAPPING ]
            self._header_caption = BaseEtl.DELIMITER.join( tokens )

        return  self._header_caption

######################

jb = MasterKeyJob( 123 )
print( jb.get_datapage_urls() )

######################
