# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
"""
The parser to convert an input notated string into a Python collection thgat represent a DAG of j0ob execution..
The orchestration is define as DAG of collections notated using the following brackets:
    [] - A list of jobs to be executed in sequence.
    {} - A set  of jobs to be executed in parallel threads on a single CPU core.
    () - A set  of jobs to be executed in parallel across all CPU cores.

Job entries in a collection are case in-sensitive and unique in the entire DAG.
Python modules shall be dynamically discover, instantiated and be matched to these job codes/entires.
Sequential processing is dependend all of previous jobs execution to be successful to proceed.

Example:
    [ a ,b ,{c ,d ,[e ,f ,(g,h,i)]} ,j ,({k,l} ,{m,n,[o,p,q]}) ,r ]
"""
# pylint: disable=line-too-long
# pylint: disable=C0103,C0326,C0330

import  re
import  gettext     # Ready for future internationalization.
i18n =  gettext.gettext

from    etlite.lexer import  DAG_Lexer as    lexer

class   DAG_Parser():
    """The DAG Parser.
    """
    # pylint: disable=W0621
#   DELIMITER   = ","
#   LF_BRACKETS = "[{(<"
#   RT_BRACKETS = "]})>"
#   PUNCTUATION =r"'`~!@#$%^&*+=:;|\/\""

    # TODO: Maybe move this into its own module if it becomes un-managaeble.
    MSG_TOO_FEW_BRACKET   = "Mis-match brackets!  Too few closing bracket.  Unclosed '{bracket}'."
    MSG_TOO_MANY_BRACKET  = "Mis-match brackets!  Too many opening bracket.  Encountered '{bracket}'."
    MSG_MIS_MATCH_BRACKET = "Mis-match brackets!  Expecting '{expect}' but encountered '{actual}'."
    MSG_NON_UNIQUE_COUNT  = "Job '{job}' occured {count} times in the input DAG."
    MSG_NON_DAG_INSTANCE  = "Object not instantiated with a DAG.  Nothing to parse."

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
            opnBkt - The opening bracket to be used to match the future closing bracket.  Must not be provided for the intial invocation.
            strPos - Starting position to begin scanning for token.  Must not be provided for the intial invocation.
            strLen - Lengh of the input string.  Must not be oorvided for the intial invocation.
        Return:
            list   - The DAG reprented in a nested list to be used by the execution engine.
            strPos - Scanned up this position in the input string.
            delimiter   - The encountered delimiter that terminated this iteration of parsing out the collection..
        Exception:
            SyntaxError - When it doesn't conform to our DAG syntax.
        """
        # pylint: disable=R0912
        if  not strLen: # NOTE: Not set on the initial call to parse the string.
            dag    = re.sub( r"\s+" ,"" ,dag ,flags=re.UNICODE )     # Remove all spaces.
            strLen = len( dag )

        stack = [ opnBkt ] if opnBkt else []
        graph = []

        while strPos < strLen:
            token ,strPos = lexer.next_token( dag=dag ,strPos=strPos ,strLen=strLen )
            latkn ,_      = lexer.next_token( dag=dag ,strPos=strPos ,strLen=strLen )   # NOTE: Look ahead one token.

            if  token  in lexer.LF_BRACKETS:
                stack.append( token )   # Shift. Push onto the stack.
                if  latkn not in lexer.RT_BRACKETS:
                    nested ,strPos ,delimiter = DAG_Parser.parse_dag( dag=dag ,opnBkt=stack[-1] ,strPos=strPos ,strLen=strLen )

                    if  len( stack ) == 0:
                        raise SyntaxError( i18n( DAG_Parser.MSG_TOO_MANY_BRACKET ).format( bracket=delimiter ))

                    if  lexer.RT_BRACKETS.index( delimiter ) != lexer.LF_BRACKETS.index( stack[-1] ):
                        raise SyntaxError( i18n( DAG_Parser.MSG_MIS_MATCH_BRACKET ).format( expect=stack[-1] ,actual=delimiter  ))

                    if  len( graph ) == 0:
                        graph = nested
                    else:
                        graph.append( nested )
            elif token  in lexer.RT_BRACKETS:
                return  graph ,strPos ,token
            else:
                if  len( graph ) == 0:
                    # NOTE: First entry is to be used to decode the type of collection
                    #       because a set of list is NOT Python compliant.
                    if  opnBkt:
                        graph.append( opnBkt )
                    else:
                        graph.append( '[' ) # Default to sequential execution.

                graph.append( token )

        # End of DAG string.
        if  len( stack ) > 1:   # NOTE: There is a leading code in the first position.
            raise   SyntaxError( i18n( DAG_Parser.MSG_TOO_FEW_BRACKET ).format( bracket=stack[-1] ))

        return  graph ,None ,None

    @staticmethod
    def validate_dag( dag:list ):
        """
        Utility to validate the parsed DAG.

        Args:
            dag    - A parsed DAG represented as a nested list.
        Return:
            None
        Exception:
            ValueError
        """
        nodes = {}
        # TODO: Make sure it recurse down into each sub-collection.
        for job in dag:
            job =  job.upper()
            if  job not in nodes:
                nodes[ job ] = 0
            nodes[ job ] += 1

        err_msg = ''
        for job in nodes:
            if  nodes[ job ] > 1:
                err_msg += i18n( DAG_Parser.MSG_NON_UNIQUE_COUNT ).format( job=job ,count=nodes[ job ] )
                err_msg += "\n"

        if  err_msg:
            raise ValueError( err_msg )


    def __init__( self ,dag:str=None ):
        self._dag_str:str = None
        self._dag:list    = None

        if  dag:
            self._dag_str = dag

    def parse( self ):
        """
        Parse the DAG string that was instantiated in this object.

        Args:
            None
        Return:
            None
        Exception:
            ReferenceError
            SyntaxError
            ValueError
        """
        if  self._dag_str:
            self._dag   = DAG_Parser.parse_dag( self._dag_str )

            DAG_Parser.validate_dag( self._dag )
        else:
            raise ReferenceError( i18n( DAG_Parser.MSG_NON_DAG_INSTANCE ))

    def get_parsed_dag( self ):
        """
        Return the aprsed DAG that was instantiated in this object.
        You sound first executed the parse() method.

        Args:
            None
        Return:
            List - An intermediate representation of the parsed DAG string.
        Exception:
            None
        """
        return  self._dag

