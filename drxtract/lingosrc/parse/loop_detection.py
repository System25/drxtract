# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, cast, Optional
from ..ast import Statement, FunctionDef, JzOperation, RepeatOperation, \
    JumpOperation, IfThenOperation, ExitRepeat, UnaryOperation, \
    UnaryOperationNames, BinaryOperation, BinaryOperationNames, Node, \
    ConstantValue, CallFunction, LoadListOperation

#
# Condition detection.
# 
# =============================================================================
def condition_detect(fn: FunctionDef):
    """
    Checks the AST of the functions statements and search for conditions.
    
    Parameters
    ----------
    fn : FunctionDef
        The function definition to check.
        
    """
    condition_detect_in_statements(fn.statements, None)

#
# Condition detection.
# 
# =============================================================================
def condition_detect_in_statements(statements: List[Statement],
                                   repeat_op: Optional[RepeatOperation]):
    """
    Checks the AST of the statements and search for conditions.
    
    Parameters
    ----------
    statements : List[Statement]
        The statements to check.
    repeat_op : Optional[RepeatOperation]
        The possible loop that contains the statements.
        
    """
    
    jzOperations: List[JzOperation] = []
    address: Optional[int] = None
    previous_st: Optional[Statement] = None
    in_else: bool = False

    # Search for jump operations
    for st in statements:                    
        if isinstance(st.code, RepeatOperation):
            ro = cast(RepeatOperation, st.code)
            condition_detect_in_statements(ro.statements_list, ro)

        if address is not None and st.position < address:
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
            # exit repeat in if part?
            if repeat_op is not None:
                ro = cast(RepeatOperation, repeat_op)
                if ro.end_position < cast(int, address):
                    address = None
        

    # Create if-else-endif statements
    for op in jzOperations:
        # if part
        ifop = IfThenOperation('if-then', op.position)
        ifop.condition = op.condition
        start = op.position
        end = cast(int, op.address)

        # exit repeat in if part
        if repeat_op is not None:
            ro = cast(RepeatOperation, repeat_op)
            if ro.end_position < end:
                st = Statement(ExitRepeat(start), start)
                nop = UnaryOperation(UnaryOperationNames.NOT, start)
                nop.operand = op.condition
                ifop.condition = nop
                ifop.if_statements_list.append(st)
                for index in range(0, len(statements)):
                    st = statements[index]
                    if st.code == op:
                        statements[index].code = ifop
                        break
                continue
        
        # Normal if part
        for index in range(0, len(statements)):
            st = statements[index]
            if st.code == op:
                statements[index].code = ifop
                continue
            
            if st.position >= start and st.position < end:
                ifop.if_statements_list.append(st)
                
            if st.position >= end:
                break
        
        for st in ifop.if_statements_list:
            statements.remove(st)

        break_detect_in_statements(ifop.if_statements_list, repeat_op)
        condition_detect_in_statements(ifop.if_statements_list, repeat_op)
            
        # else part
        last_idx = len(ifop.if_statements_list) - 1
        if isinstance(ifop.if_statements_list[last_idx].code, JumpOperation):
            jop = cast(JumpOperation, ifop.if_statements_list[last_idx].code)
            start = jop.position
            end = cast(int, jop.address)
            # exit repeat in else part
            if repeat_op is not None:
                ro = cast(RepeatOperation, repeat_op)
                if ro.end_position < end:
                    st = Statement(ExitRepeat(start), start)
                    ifop.if_statements_list.pop()
                    ifop.if_statements_list.append(st)
                    continue
            
            # Normal else part
            for index in range(0, len(statements)):
                st = statements[index]
                if st.position > start and st.position < end:
                    ifop.else_statements_list.append(st)
                    
                if st.position >= end:
                    break
        
            for st in ifop.else_statements_list:
                statements.remove(st)
                 
            ifop.if_statements_list.pop()
            
            break_detect_in_statements(ifop.else_statements_list, repeat_op)
            condition_detect_in_statements(ifop.else_statements_list, repeat_op)


#
# Break loop detection inside if or else operation.
# 
# =============================================================================
def break_detect_in_statements(statements: List[Statement],
                                   repeat_op: Optional[RepeatOperation]):
    """
    Checks the AST of the statements inside an if or else and search for
    break.
    
    Parameters
    ----------
    statements : List[Statement]
        The statements to check.
    repeat_op : Optional[RepeatOperation]
        The possible loop that contains the statements.
        
    """
    
    if repeat_op is None or len(statements)<2:
        return
    
    # Check the last statement before "else" jump
    idx_2 = len(statements) - 2
    last_st: Statement = statements[idx_2]
    if isinstance(last_st.code, JumpOperation):
        jop = cast(JumpOperation, last_st.code)
        address: int = cast(int, jop.address)
        ro = cast(RepeatOperation, repeat_op)
        if ro.end_position < address:
            st = Statement(ExitRepeat(jop.position), jop.position)
            else_jump = statements.pop()
            statements.pop()
            statements.append(st)
            statements.append(else_jump)


#
# Loop detection.
# 
# =============================================================================
def loop_detect(fn: FunctionDef):
    """
    Checks the AST of the functions statements and search for loops.
    
    Parameters
    ----------
    fn : FunctionDef
        The function definition to check.
        
    """

    loop_detect_in_statements(fn.statements)

#
# Loop detection.
# 
# =============================================================================
def loop_detect_in_statements(statements: List[Statement]):
    """
    Checks the AST of the functions statements and search for loops.
    
    Parameters
    ----------
    statements : List[Statement]
        The statements to check.
        
    """

    to_remove: List[Statement] = []
    previous_st: Optional[Statement] = None

    # Search for repeat operations
    for st in statements:                    
        if isinstance(st.code, RepeatOperation):
            ro: RepeatOperation = cast(RepeatOperation, st.code)
            
            if is_repeat_while(ro):
                # Repeat while
                ifop: IfThenOperation = cast(IfThenOperation,
                                             ro.statements_list[0].code)
                nop: UnaryOperation = cast(UnaryOperation, ifop.condition) 
                ro.condition = nop.operand
                ro.statements_list.pop(0)
            
            if is_repeat_with(ro, previous_st):
                # Repeat with
                ro.type = 'for'
                p_st: Statement = cast(Statement, previous_st)    
                p_op: BinaryOperation = cast(BinaryOperation, p_st.code)
                ro.varname = cast(Node, p_op.left).name
                ro.start = cast(Node, p_op.right)
                
                cond: BinaryOperation = cast(BinaryOperation, ro.condition)
                ro.end = cast(Node, cond.right)
                
                last_idx = len(ro.statements_list) - 1
                last_st: Statement = ro.statements_list[last_idx]
                last_op: BinaryOperation = cast(BinaryOperation, last_st.code)
                inc_dec: BinaryOperation = cast(BinaryOperation, last_op.right)
                
                increment: Node = cast(Node, inc_dec.left)
                sign:str = '+'
                if (isinstance(increment, ConstantValue) and 
                    increment.name == '-1'):
                    sign = '-'
                ro.sign = sign
                
                ro.statements_list.pop()
                to_remove.append(p_st)
                
            if is_repeat_with_in_list(ro):
                # Repeat with in list
                ro.type = 'for_in'
                first_st: Statement = ro.statements_list[0]
                first_op: BinaryOperation = cast(BinaryOperation, first_st.code)
                ro.varname = cast(Node, first_op.left).name
                
                assign_fn: CallFunction = cast(CallFunction, first_op.right)
                assign_fn_par:LoadListOperation = cast(
                    LoadListOperation, assign_fn.parameters)
                ro.start = assign_fn_par.operands[1]
                
                ro.statements_list.pop(0)

            
            loop_detect_in_statements(ro.statements_list)
    
        if isinstance(st.code, IfThenOperation):
            io = cast(IfThenOperation, st.code)
            loop_detect_in_statements(io.if_statements_list)
            loop_detect_in_statements(io.else_statements_list)
    
        previous_st = st
        
    for st in to_remove:
        statements.remove(st)
    
def is_repeat_with_in_list(ro: RepeatOperation):
    """
    Checks the repeat operation and the previous statement in order
    to see if this is a repeat-with-in-list operation.
    
    Parameters
    ----------
    ro : RepeatOperation
        The repeat operation to check.
        
    Returns
    -------
    boolean
        True if this is repeat-while loop.
    """
    
    if not isinstance(ro.condition, BinaryOperation):
        return False
    
    cond: BinaryOperation = cast(BinaryOperation, ro.condition)
    if (not isinstance(cond.left, ConstantValue) or 
        not isinstance(cond.right, CallFunction)):
        return False
    
    index: str = cast(ConstantValue, cond.left).name
    cond_func: CallFunction = cast(CallFunction, cond.right)
    if index != '1' or cond_func.name != 'count':
        return False
    cond_func_par:LoadListOperation = cast(
        LoadListOperation, cond_func.parameters)

    if len(ro.statements_list) > 0:
        st: Statement = ro.statements_list[0]
        if (isinstance(st.code, BinaryOperation)
            and st.code.name == BinaryOperationNames.ASSIGN.value):
            first_op: BinaryOperation = cast(BinaryOperation, st.code)
            
            if not isinstance(first_op.right, CallFunction):
                return False
            
            assign_fn: CallFunction = cast(CallFunction, first_op.right)
            if not assign_fn.name == 'getAt':
                return False
            
            assign_fn_par:LoadListOperation = cast(
                LoadListOperation, assign_fn.parameters)

            if (cond_func_par.operands[0] != assign_fn_par.operands[1]
                or assign_fn_par.operands[0].name != '1'):
                return False
    
            return True
    
    

    return False 
        
def is_repeat_with(ro: RepeatOperation, previous_st: Optional[Statement]):
    """
    Checks the repeat operation and the previous statement in order
    to see if this is a repeat-with operation.
    
    Parameters
    ----------
    ro : RepeatOperation
        The repeat operation to check.
        
    previous_st: Optional[Statement]
        The previous statement.
        
    Returns
    -------
    boolean
        True if this is repeat-while loop.
    """

    if previous_st is None:
        return False
    
    p_st: Statement = cast(Statement, previous_st)
    if (not isinstance(p_st.code, BinaryOperation)
        or p_st.code.name != BinaryOperationNames.ASSIGN.value):
        return False
    
    p_op: BinaryOperation = cast(BinaryOperation, p_st.code)
    varname1: str = cast(Node, p_op.left).name
    
    if not isinstance(ro.condition, BinaryOperation):
        return False
    
    cond: BinaryOperation = cast(BinaryOperation, ro.condition)
    varname2: str = cast(Node, cond.left).name
    
    if varname1 != varname2:
        return False

    if len(ro.statements_list) > 0:
        last_idx = len(ro.statements_list) - 1
        st: Statement = ro.statements_list[last_idx]
        if (isinstance(st.code, BinaryOperation)
            and st.code.name == BinaryOperationNames.ASSIGN.value):
            last_op: BinaryOperation = cast(BinaryOperation, st.code)
            varname3: str = cast(Node, last_op.left).name
            
            if ((varname1 != varname3) or (last_op.right is None)
                or not isinstance(last_op.right, BinaryOperation)):
                return False
            
            inc_dec: BinaryOperation = cast(BinaryOperation, last_op.right)
            if (cast(Node, inc_dec.right).name != varname3 or
                inc_dec.name != BinaryOperationNames.ADD.value):
                return False
    
            return True
    
    

    return False        
        
def is_repeat_while(ro: RepeatOperation):
    """
    Checks the repeat operation and the previous statement in order
    to see if this is a repeat-while operation.
    
    Parameters
    ----------
    ro : RepeatOperation
        The repeat operation to check.
        
    Returns
    -------
    boolean
        True if this is repeat-while loop.
    """

    if len(ro.statements_list) > 0:
        st: Statement = ro.statements_list[0]
        if isinstance(st.code, IfThenOperation):
            ifop: IfThenOperation = cast(IfThenOperation, st.code)
            if (len(ifop.else_statements_list) == 0
                and len(ifop.if_statements_list) == 1
                and isinstance(ifop.if_statements_list[0].code, ExitRepeat)
                and isinstance(ifop.condition, UnaryOperation)
                and ifop.condition.name is UnaryOperationNames.NOT.value):                
                return True
                
    return False
