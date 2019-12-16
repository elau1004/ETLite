# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import abstractmethod

from etlite.common.base_etl import BaseEtl

class   BaseRestApiEtl( BaseEtl ):

    def __init__( self, job_code:str ):
        super().__init__( job_code )

