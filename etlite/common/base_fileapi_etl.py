# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import abstractmethod
from datetime import datetime as datetime

from etlite.common.base_etl import BaseEtl

class   BaseFileApiEtl( BaseEtl ):

    def __init__( self ,dataset_code:str ,dataset_codes:list=None ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ,status_id:int=None ):
        super().__init__( dataset_code ,dataset_codes ,run_id ,from_date ,upto_date ,status_id )
        self._workflow_seq  += "F" # File Transfer workflow.

# TODO: Flesh this out.
