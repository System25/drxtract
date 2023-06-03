# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, cast
from ..ast import Statement, Function, JzOperation, RepeatOperation, \
    JumpOperation, IfThenOperation


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
    jumpOperations: List[JumpOperation] = []

    # Search for jump operations
    for st in statements:
        if isinstance(st.code, JzOperation):
            jzOperations.append(cast(JzOperation, st.code))
            
        if isinstance(st.code, JumpOperation):
            jumpOperations.append(cast(JumpOperation, st.code))
            
        if isinstance(st.code, RepeatOperation):
            ro = cast(RepeatOperation, st.code)
            condition_detect_in_statements(ro.statements_list)
        

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
