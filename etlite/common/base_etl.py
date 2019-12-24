# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from datetime import datetime as datetime

from abc import ABC, abstractmethod

class   BaseEtl( ABC ):

    def __init__( self ,job_code:str ,run_id:int ,from_date:datetime=None ,upto_date:datetime=None ,status=None ):
        self.job_code:str = job_code        # Unique code for this job.
        self.run_id:int = run_id            # Unique id for each run.
        self.from_date:datetime = from_date # Inclusive greater and equal.
        self.upto_date:datetime = upto_date # Not inclusive less than.
        self.status:int = status

        if  not  self.upto_date:
            self.upto_date = datetime.now()

    @property
    def code( self ) -> str:
        return  self.job_code

    @property
    def run_id( self ) -> int:
        return  self.run_id

    @run_id.setter
    def run_id( self ,run_id:int ):
        self.run_id = run_id

    @property
    def from_date( self ) -> datetime:
        return  self.from_date

    @from_date.setter
    def from_date( self ,from_date:datetime ):
        self.from_date = from_date

    @property
    def upto_date( self ) -> datetime:
        return  self.upto_date

    @upto_date.setter
    def upto_date( self ,upto_date:datetime ):
        self.upto_date = upto_date

    @property
    def run_status( self ) -> int:
        return  self.status

    @run_status.setter
    def run_status( self ,status:int ):
        self.status = status
