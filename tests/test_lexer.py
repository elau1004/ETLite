import unittest

from    etlite.common.lexer     import  DAG_Lexer   as  lexer
from    etlite.common.parser    import  DAG_Parser  as  parser
from    tests.base_test         import  BaseTest


class TestLexer( BaseTest ):
    @classmethod
    def setUpClass(cls):
        print('setupClass')
    
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
    
    def tearDown(self):
        print('tearDown')
    
    def test_next_token( self ):
        cases = [
            {"msg": "Test stripping punctuations." ,"dag": "~"                  ,"expect": []                                              }
           ,{"msg": "Test single character."       ,"dag": "a"                  ,"expect": ['a']                                           }
           ,{"msg": "Test multi characters."       ,"dag": "abc"                ,"expect": ['abc']                                         }
           ,{"msg": "Test stripping embedded punc.","dag": "a!b@c"              ,"expect": ['abc']                                         }
           ,{"msg": "Test multi entries."          ,"dag": "a,bc ,def"          ,"expect": ['a','bc','def']                                }  #expected 'bc '
           ,{"msg": "Test sequential jobs."        ,"dag": "[a ,b ,c]"          ,"expect": [ '[','a','b','c',']' ]                         }
           ,{"msg": "Test muti-threaded jobs."     ,"dag": "{a ,b ,c}"          ,"expect": [ '{','a','b','c', '}' ]                        }
           ,{"msg": "Test muti-process jobs."      ,"dag": "(a ,b ,c)"          ,"expect": [ '(', 'a', 'b', 'c', ')' ]                     }
           ,{"msg": "Test one nesting."            ,"dag": "[a ,{b},c]"         ,"expect": [ '[','a', '{', 'b' , '}' ,'c', ']' ]           }   #needed to remove space after }
           ,{"msg": "Test two nesting."            ,"dag": "[a ,{b},(c)]"       ,"expect": [ '[', 'a', '{','b','}', '(', 'c', ')' ,']' ]   } #needed to remove space after }
           ,{"msg": "Test two level nesting."      ,"dag": "[a ,{b,  (c)}]"     ,"expect": [ '[', 'a', '{', 'b', '(', 'c' ,')' ,'}' ,']']  }
           ,{"msg": "Test three level nesting."    ,"dag": "{ a ,b  ,[d,(e),f]}","expect": [ '{','a','b','[','d','(','e',')','f',']','}' ] }
        ]
    
        for case in cases:
            strPos= 0
            strLen= len(case['dag'])
            token = 'dag'
            result= []
            while token:
                token ,strPos = lexer.next_token( case['dag'] ,strPos=strPos ,strLen=strLen )
                if  token:
                    result.append( token ) 
            self.assertEqual( result ,case['expect'] ,case['msg'] )

if __name__ == '__main__':
    unittest.main()
