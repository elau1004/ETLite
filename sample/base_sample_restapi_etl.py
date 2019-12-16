# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import ABC, abstractmethod

from etlite.common.base_restapi_etl import BaseRestApiEtl

"""
This is an optional class to add some additional methods and properties
for this Sample vendor to be shared by both Sam1 and Sam2 etl jobs.
"""
class   BaseSampleRestApiEtl( BaseRestApiEtl ):

    def __init__( self, job_code:str ):
        super().__init__( job_code )

