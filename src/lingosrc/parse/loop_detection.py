# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, cast, Optional
from ..ast import Statement, Function, JzOperation, RepeatOperation, \
    JumpOperation, IfThenOperation
from dns.rdataclass import NONE


#
# Condition detection.
# 
# =============================================================================
def condition_detect(function: Function):
    """
    Checks the AST of the functions statements and search for conditions.
    
    Parameters
    ----------
    function : Function
        The function to check.
        
    """
    condition_detect_in_statements(function.statements)

#
# Condition detection.
# 
# =============================================================================
def condition_detect_in_statements(statements: List[Statement]):
    """
    Checks the AST of the statements and search for conditions.
    
    Parameters
    ----------
    statements : List[Statement]
        The statements to check.
        
    """
    
    jzOperations: List[JzOperation] = []
    address: Optional[int] = None
    previous_st: Optional[Statement] = None
    in_else: bool = False

    # Search for jump operations
    for st in statements:                    
        if isinstance(st.code, RepeatOperation):
            ro = cast(RepeatOperation, st.code)
            condition_detect_in_statements(ro.statements_list)

        if address is not None and st.position < cast(int, address):
            previous_st = st
            continue

        if in_else:
            previous_st = None
            address = None
            in_else = False

        if (previous_st is not None and 
            isinstance(previous_st.code, JumpOperation)):
            jop = cast(JumpOperation, previous_st.code)
            address = jop.address
            in_else = True
            continue


        if isinstance(st.code, JzOperation):
            jzop: JzOperation = cast(JzOperation, st.code)
            address = jzop.address
            jzOperations.append(jzop)
        

    # Create if-else-endif statements
    for op in jzOperations:
        ifop = IfThenOperation('if-then', op.position)
        ifop.condition = op.condition
        start = op.position
        end = cast(int, op.address)

        # if part
        for index, st in enumerate(statements):
            if st.code == op:
                statements[index].code = ifop
                continue
            
            if st.position >= start and st.position < end:
                ifop.if_statements_list.append(st)
                
            if st.position >= end:
                break
        
        for st in ifop.if_statements_list:
            statements.remove(st)
            
        # else part
        if isinstance(ifop.if_statements_list[-1].code, JumpOperation):
            # Else part
            jop = cast(JumpOperation, ifop.if_statements_list[-1].code)
            start = jop.position
            end = cast(int, jop.address)
            
            for index, st in enumerate(statements):
                if st.position > start and st.position < end:
                    ifop.else_statements_list.append(st)
                    
                if st.position >= end:
                    break
        
            for st in ifop.else_statements_list:
                statements.remove(st)
                 
            ifop.if_statements_list.pop()
            
        condition_detect_in_statements(ifop.if_statements_list)
        condition_detect_in_statements(ifop.else_statements_list)

#
# Loop detection.
# 
# =============================================================================
def loop_detect(function: Function):
    """
    Checks the AST of the functions statements and search for loops.
    
    Parameters
    ----------
    function : Function
        The function to check.
        
    """

    pass
