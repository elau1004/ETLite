# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
The engine to orchestrate job executions.
The orchestration is define as DAG of collections notated using the following brackets:
    [] - A list of jobs to be executed in sequence.
    {} - A set  of jobs to be executed in parallel threads on a single CPU core.
    () - A set  of jobs to be executed in parallel across all CPU cores.

Job entries in a collection are case in-sensitive and unique in the entire DAG.
Python modules shall be dynamicall discover and be matched to these job codes/entires.
Sequential processing is dependend all of previous jobs execution to be successful to proceed.

Example:
    [ a ,b ,{c ,d ,[e ,f ,(g,h,i)]} ,j ,({k,l} ,{m,n,[o,p,q]}) ,r ]
"""
# pylint: disable=line-too-long
# pylint: disable=C0103,C0326,C0330

class   DAG_Lexer():
    """The DAG lexer.
    """
    # pylint: disable=W0621
    DELIMITER   = ","
    LF_BRACKETS = "[{(<"
    RT_BRACKETS = "]})>"
    PUNCTUATION =r" '`~!@#$%^&*+=:;|\/\""

    @staticmethod
    def next_token( dag:str ,strPos:int ,strLen:int ) -> (str ,int):
        """
        Utility lexer to return next parsed token from the input string.
        You do not need to pass in sub-string but instead the starting position to continue parsing from.

        Args:
            dag    - A string representation of a DAG.
            strPos - Starting position to begin scanning for token.
            strLen - Lenght of the input string.
        Return:
            token  - A parsed token.  In out DAG language it shall be:
                       - Left  brackets.
                       - Right brackets.
                       - Literal.
            strPos - Scanned up this position in the input string.
        Exception:
            None
        """
        token = ''
        for ch  in  dag[ strPos: ]:
            strPos  +=  1
            if  ch  == DAG_Lexer.DELIMITER:
                break

            if  ch  not in  DAG_Lexer.PUNCTUATION:
                token   +=  ch

                if  ch  in  DAG_Lexer.LF_BRACKETS + DAG_Lexer.RT_BRACKETS:
                    if  strPos  +1  < strLen and dag[ strPos ] == DAG_Lexer.DELIMITER:
                        strPos  +=  1
                    break
                if  strPos < strLen and dag[ strPos ] in DAG_Lexer.LF_BRACKETS + DAG_Lexer.RT_BRACKETS:
                    break

        return  token ,strPos
