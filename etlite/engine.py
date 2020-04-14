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

import  re
import  gettext     # Ready for future internationalization.
i18n =  gettext.gettext

class   ETL_Engine():
    """The DAG engine.
    """
    # pylint: disable=W0621
    DELIMITER   = ","
    LF_BRACKETS = "[{(<"
    RT_BRACKETS = "]})>"
    PUNCTUATION =r"'`~!@#$%^&*+=:;|\/\""

    # TODO: Maybe move this into its own module if it becomes un-managaeble.
    MSG_TOO_FEW_BRACKET   = "Mis-match brackets!  Too few closing bracket.  Unclosed '{bracket}'."
    MSG_TOO_MANY_BRACKET  = "Mis-match brackets!  Too many opening bracket.  Encountered '{bracket}'."
    MSG_MIS_MATCH_BRACKET = "Mis-match brackets!  Expecting '{expect}' but encountered '{actual}'."


    @staticmethod
    def get_token( dag:str ,strPos:int ,strLen:int ) -> (str ,int):
        """
        Utility lexer to return a parsed token from the input string.
        You do not need to pass in sub-string but instead the starting position to continue parsing from.

        Args:
            dag    - A string representation of a DAG.
            strPos - Strating position to begin scanning for token.
            strLen - Lengh of the inpiut string.
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
            if  ch  == ',':
                break

            if  ch  not in  ETL_Engine.PUNCTUATION:
                token   +=  ch

                if  ch  in  ETL_Engine.LF_BRACKETS + ETL_Engine.RT_BRACKETS:
                    if  strPos  +1  < strLen and dag[ strPos ] == ETL_Engine.DELIMITER:
                        strPos  +=  1
                    break
                if  strPos < strLen and dag[ strPos ] in ETL_Engine.LF_BRACKETS + ETL_Engine.RT_BRACKETS:
                    break

        return  token ,strPos

    @staticmethod
    def parse_dag( dag:str ,opnBkt:str=None ,strPos:int=0 ,strLen:int=None ) -> (list ,int ,str):
        """
        Utility parser to parse a DAG notated string and return a Python collection that represents it.
        The first entry of each list qualify the action to be taken by the exeution engine.  The values
        are:
            '[' - sequential execution on a single CPU core.
            '{' - parallel   execution on a single CPU core.
            '(' - parallel   execution on separate CPU core.
            '<' - sequential execution on separate CPU core.  Not a normal case and not implmented.

        See:
            https://en.wikipedia.org/wiki/LALR_parser
        Args:
            dag    - A string representation of a DAG.
            opnBkt - The opening bracket to be used to match the future closing bracket.
            strPos - Strating position to begin scanning for token.
            strLen - Lengh of the inpiut string.
        Return:
            list   - The DAG reprented in a nested list to be used by the execution engine.
            strPos - Scanned up this position in the input string.
            delimiter   - The encountered delimiter that terminated this iteration of parsing out the collection..
        Exception:
            SyntaxError - When it doesn't conform to our DAG syntax.
        """
        # pylint: disable=R0912
        if  not strLen:
            strLen = len( dag )

        stack = [ opnBkt ] if opnBkt else []
        graph = []

        while strPos < strLen:
            token ,strPos = ETL_Engine.get_token( dag=dag ,strPos=strPos ,strLen=strLen )
            latkn ,_      = ETL_Engine.get_token( dag=dag ,strPos=strPos ,strLen=strLen )   # NOTE: Look ahead one token.

            if  token  in ETL_Engine.LF_BRACKETS:
                stack.append( token )   # Shift. Push onto the stack.
                if  latkn not in ETL_Engine.RT_BRACKETS:
                    nested ,strPos ,delimiter = ETL_Engine.parse_dag( dag=dag ,opnBkt=stack[-1] ,strPos=strPos ,strLen=strLen )

                    if  len( stack ) == 0:
                        raise   SyntaxError( i18n( ETL_Engine.MSG_TOO_MANY_BRACKET ).format( bracket=delimiter ))
                    if ETL_Engine.RT_BRACKETS.index( delimiter ) != ETL_Engine.LF_BRACKETS.index( stack[-1] ):
                        raise   SyntaxError( i18n( ETL_Engine.MSG_MIS_MATCH_BRACKET ).format( expect=stack[-1] ,actual=delimiter  ))

                    if  len( graph ) == 0:
                        graph = nested
                    else:
                        graph.append( nested )
            elif token in ETL_Engine.RT_BRACKETS:
                return  graph ,strPos ,token
            else:
                if  len( graph ) == 0:
                    if  opnBkt:
                        graph.append( opnBkt )
                    else:
                        graph.append( '[' ) # Default to sequential execution.

                graph.append( token )

        # End of DAG string.
        if  len( stack ) > 1:   # NOTE: There is a leading code in the first position.
            raise   SyntaxError( i18n( ETL_Engine.MSG_TOO_FEW_BRACKET ).format( bracket=stack[-1] ))

        return  graph ,None ,None


    def __init__( self ,dag:dict ):
        self._dag = re.sub( r"\s+" ,"" ,dag ,flags=re.UNICODE )     # Remove all spaces.