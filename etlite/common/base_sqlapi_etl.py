# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import abstractmethod
from datetime import datetime as datetime

from etlite.common.base_etl import BaseEtl

class   BaseSqlApiEtl( BaseEtl ):

    def __init__( self ,job_code:str ,run_id:int=0 ,from_date:datetime=None ,upto_date:datetime=None ):
        super().__init__( job_code ,run_id ,from_date ,upto_date )

# TODO: Flesh this out.
