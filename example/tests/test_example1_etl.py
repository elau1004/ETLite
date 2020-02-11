# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import  unittest

from  etlite.common.base_etl import BaseEtl
from  etlite.common.base_restapi_etl import BaseRestApiEtl
from  example.base_example_restapi_etl import BaseExampleRestApiEtl
from  example.example1_etl import Example1Etl
from  tests.base_test import BaseTest

class TestEtlite( BaseTest ):

    def test_inheritance( self ):
        s = Example1Etl()

        self.assertIsInstance( s ,BaseEtl )
        self.assertIsInstance( s ,BaseRestApiEtl )
        self.assertIsInstance( s ,BaseExampleRestApiEtl )

if "__main__" == __name__:
    unittest.main()

