# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
DAG Parser test suite.

SEE:    https://docs.python.org/3/library/unittest.html
        https://realpython.com/python-testing/
"""
import  unittest

from    etlite.common.lexer     import  DAG_Lexer   as  lexer
from    etlite.common.parser    import  DAG_Parser  as  parser
from    tests.base_test         import  BaseTest

class Test_DAG_Parser( BaseTest ):
    @classmethod
    def setUpClass( cls ):
        pass

    @classmethod
    def tearDownClass( cls ):
        pass

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    ####

    def test_parser( self ):
        # Positive cases.
        cases = [
             {"msg": "Test stripping punctuations." ,"dag": lexer.PUNCTUATION       ,"expect": []}
            ,{"msg": "Test single character."       ,"dag": "a"                     ,"expect": ['[' ,'a']   }
            ,{"msg": "Test multi characters."       ,"dag": "abc"                   ,"expect": ['[' ,'abc'] }
            ,{"msg": "Test stripping embedded punc.","dag": "a!b@c"                 ,"expect": ['[' ,'abc'] }
            ,{"msg": "Test multi entries."          ,"dag": "a,bc ,def"             ,"expect": ['[' ,'a' ,'bc','def']}
            ,{"msg": "Test sequential jobs."        ,"dag": "[a ,b ,c]"             ,"expect": ['[' ,'a' ,'b' ,'c'] }
            ,{"msg": "Test muti-threaded jobs."     ,"dag": "{a ,b ,c}"             ,"expect": ['{' ,'a' ,'b' ,'c'] }
            ,{"msg": "Test muti-process jobs."      ,"dag": "(a ,b ,c)"             ,"expect": ['(' ,'a' ,'b' ,'c'] }
            ,{"msg": "Test one nesting."            ,"dag": "[a ,{b} ,c]"           ,"expect": ['[' ,'a' ,['{','b'] ,'c']   }
            ,{"msg": "Test two nesting."            ,"dag": "[a ,{b} ,(c)]"         ,"expect": ['[' ,'a' ,['{','b'] ,['(' ,'c']]    }
            ,{"msg": "Test two level nesting."      ,"dag": "[a ,{b  ,(c)}]"        ,"expect": ['[' ,'a' ,['{','b'  ,['(' ,'c']]]   }
            ,{"msg": "Test three level nesting."    ,"dag": "{ a ,b  ,[d,(e),f]}"   ,"expect": ['{' ,'a' ,'b' ,['[' ,'d' ,['(' ,'e'] ,'f' ]] }
        ]

        for case in cases:
            dag ,_ ,_ = parser.parse_dag( case['dag'] )
            self.assertEquals( dag ,case['expect'] ,case['msg'] )

if "__main__" == __name__:
    unittest.main()
