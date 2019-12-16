# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from abc import ABC, abstractmethod

class   BaseEtl( ABC ):

    def __init__( self, job_code:str ):
        self.job_code:str   = job_code
        self.job_run_id:int = None
        self.job_status:int = None

    @property
    def code( self ) -> str:
        return  self.job_code

    @property
    def run_id( self ) -> int:
        return  self.job_run_id

    @run_id.setter
    def run_id( self ,run_id:int ):
        self.job_run_id = run_id

    @abstractmethod
    def abs_method( self ):
        pass
