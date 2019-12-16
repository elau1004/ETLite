# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  etlite.common.exections

import  sample_base_etl

class   Sam2Etl( BaseSampleEtl ):
    CODE = "SAM2"

    def __init__( self ):
        super().__init__( CODE )
