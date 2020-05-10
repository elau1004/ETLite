# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc      import ABC, abstractmethod
from datetime import datetime as datetime

from etlite.common.base_restapi_etl import BaseRestApiEtl

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

        super().__init__( NetsuiteObjectKeyJob.CODE ,run_id=run_id ,filter_on=filter_on ,from_date=from_date ,upto_date=upto_date )

        self._header_caption = None
        self.tasks = {
            "Sale Order Detail": {
                "search_id"   : 4659,
                "table_code"  : "dd_so_lns",
                "filter_on"   : "datecreated",
                "ttl_pages"   : None,
                "ttl_records" : None
            },
            "Purchase Order Detail": {
                "search_id"   : 4658,
                "table_code"  : "dd_po_lns",
                "filter_on"   : "datecreated",
                "ttl_pages"   : None,
                "ttl_records" : None
            },
            "Purchase Order Approval Routes": {
                "search_id"   : 4660,
                "table_code"  : "dd_po_apr",
                "filter_on"   : "created",
                "ttl_pages"   : None,
                "ttl_records" : None
            }
        }
        if  logger:
            self.logger = logger
        else:
            self.logger = get_logger


    # Begin Interface implementation section
    #

    # Required step 7.
    def get_datapage_urls( self ) -> list((str,dict,str,dict)):
        """ SEE: BaseRestApiEtl.get_datapage_urls()
        """
        from_page = 1
        upto_page = 20
        # TODO: Need to iterate through the tasks.
        if  self.tasks['Sale Order Detail']['ttl_pages']:
            from_page = 21
            upto_page = self.tasks['Sale Order Detail']['ttl_pages']

        loopback = self.get_loopback()
        loopback['task'] = 'Sales Order Detail'
        return  self.get_requests( from_page=from_page ,upto_page=upto_page ,step=20 ,loopback=loopback )

    # Required step 8.
    def put_datapage_resp( self ,ctx:RestApiContext ,content:dict ) -> list((str ,int ,str))
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
            self.tasks['Sale Order Detail']['ttl_pages'] = content['No of Pages Requested'].split(' ')[2]    # TODO: Flesh this out!
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
            tokens = [ NetsuiteObjectKeyJob.JSON_TO_DB_MAPPING[ key ] for key in JSON_TO_DB_MAPPING ]
            self._header_caption = BaseEtl.DELIMITER.join( tokens )

        return  self._header_caption

######################

jb = NetsuiteObjectKeyJob( 123 )
print( jb.get_next_datapage_url() )

######################
