# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import abstractmethod
from datetime import datetime as datetime

from etlite.common.base_etl import BaseEtl

class   BaseSqlApiEtl( BaseEtl ):

    def __init__( self ,dataset_code:str ,run_id:int=None ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( dataset_code=dataset_code ,run_id=run_id ,from_date=from_date ,upto_date=upto_date )
        # SQL query workflow.
        if  self._workflow_seq:
            self._workflow_seq   += "S"
        else:
            self._workflow_seq    = "S"
        pass

# TODO: Flesh this out.
