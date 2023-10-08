# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode, BiOpcode
from ..ast import Node, StringOperation, UnaryOperation,\
    Statement, UnaryOperationNames, StringOperationNames, FunctionDef, \
    SpAssignOperation, BinaryOperationNames
from ..model import Context
from typing import List

def add_str_operation(op: Node, start_pos: Node, end_pos: Node, \
                      name: StringOperationNames, index: int):
    operation = op
    
    if start_pos.name != '0':
        operation = StringOperation(name, index)
        operation.of = op
        operation.start = start_pos
    
        if end_pos.name != '0':
            operation.end = end_pos
    
    return operation

def add_modifiers(self, op: Node, stack: List[Node], index: int):
    
    op_ll_pos = stack.pop()    # Last line position
    op_fl_pos = stack.pop()    # First line position
    op_li_pos = stack.pop()    # Last item position
    op_fi_pos = stack.pop()    # First item position
    # (items separated by the itemDelimiter, which is a comma by default)
    op_lw_pos = stack.pop()    # Last word position
    op_fw_pos = stack.pop()    # First word position
    op_lc_pos = stack.pop()    # Last char position
    op_fc_pos = stack.pop()    # First char position

    op = add_str_operation(op, op_fl_pos, op_ll_pos, \
                           StringOperationNames.LINE, index)    
    op = add_str_operation(op, op_fi_pos, op_li_pos, \
                           StringOperationNames.ITEM, index)
    op = add_str_operation(op, op_fw_pos, op_lw_pos, \
                           StringOperationNames.WORD, index)
    op = add_str_operation(op, op_fc_pos, op_lc_pos, \
                           StringOperationNames.CHAR, index)


    return op

#
# String slice operation Opcode.
#
class StringOperationOpcode(Opcode):
    def __init__(self):
        super().__init__(0x17)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = stack.pop()           # The string to slice
        op = add_modifiers(self, op, stack, index)
        stack.append(op)

#
# Hilite Opcode.
#
class HiliteOpcode(Opcode):
    def __init__(self):
        super().__init__(0x18)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to hilite     
        field = add_modifiers(self, field, stack, index)
        
        op = UnaryOperation(UnaryOperationNames.HILITE, index)
        op.operand = field

        fn.statements.append(Statement(op, index))

#
# Put into field Opcode.
#
class PutIntoFieldOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x06)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to put     
        field = add_modifiers(self, field, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = field
        op.right = stack.pop()
        op.mode = 'into'
        
        fn.statements.append(Statement(op, index))


#
# Put into field Opcode.
#
class PutIntoFieldSpOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x16)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to put     
        field = add_modifiers(self, field, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = field
        op.right = stack.pop()
        op.mode = 'into'
        
        fn.statements.append(Statement(op, index))

#
# Put into list Opcode.
#
class PutIntoListOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x12)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        lval = stack.pop()
        lval = add_modifiers(self, lval, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = lval
        op.right = stack.pop()
        op.mode = 'into'
        
        fn.statements.append(Statement(op, index))

#
# Put into string Opcode.
#
class PutIntoStringOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x15)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        op1 = int(stack.pop().name)
        lval = fn.local_vars[op1]
        lval = add_modifiers(self, lval, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = lval
        op.right = stack.pop()
        op.mode = 'into'
        
        fn.statements.append(Statement(op, index))

#
# Put after list Opcode.
#
class PutAfterListOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x22)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        lval = stack.pop()
        lval = add_modifiers(self, lval, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = lval
        op.right = stack.pop()
        op.mode = 'after'
        
        fn.statements.append(Statement(op, index))

#
# Put after string Opcode.
#
class PutAfterStringOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x25)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        op1 = int(stack.pop().name)
        lval = fn.local_vars[op1]
        lval = add_modifiers(self, lval, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = lval
        op.right = stack.pop()
        op.mode = 'after'
        
        fn.statements.append(Statement(op, index))

#
# Put after field Opcode.
#
class PutAfterFieldOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x26)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to put     
        field = add_modifiers(self, field, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = field
        op.right = stack.pop()
        op.mode = 'after'
        
        fn.statements.append(Statement(op, index))

#
# Put before list Opcode.
#
class PutBeforeListOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x32)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        lval = stack.pop()
        lval = add_modifiers(self, lval, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = lval
        op.right = stack.pop()
        op.mode = 'before'
        
        fn.statements.append(Statement(op, index))
        
#
# Put before String Opcode.
#
class PutBeforeStringOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x35)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        op1 = int(stack.pop().name)
        lval = fn.local_vars[op1]
        lval = add_modifiers(self, lval, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = lval
        op.right = stack.pop()
        op.mode = 'before'
        
        fn.statements.append(Statement(op, index))

#
# Put before field Opcode.
#
class PutBeforeFieldOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5A, 0x36)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to put     
        field = add_modifiers(self, field, stack, index)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = field
        op.right = stack.pop()
        op.mode = 'before'
        
        fn.statements.append(Statement(op, index))

#
# Delete from list Opcode.
#
class DeleteFromListOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5B, 0x02)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        lval = stack.pop()  # The list to delete from     
        lval = add_modifiers(self, lval, stack, index)
        
        op = UnaryOperation(UnaryOperationNames.DELETE, index)
        op.operand = lval
        
        fn.statements.append(Statement(op, index))
        
#
# Delete from string Opcode.
#
class DeleteFromStringOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5B, 0x05)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        op1 = int(stack.pop().name)
        lval = fn.local_vars[op1]
        lval = add_modifiers(self, lval, stack, index)
        
        op = UnaryOperation(UnaryOperationNames.DELETE, index)
        op.operand = lval
        
        fn.statements.append(Statement(op, index))

#
# Delete from field Opcode.
#
class DeleteFromFieldOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5B, 0x06)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to delete     
        field = add_modifiers(self, field, stack, index)
        
        op = UnaryOperation(UnaryOperationNames.DELETE, index)
        op.operand = field
        
        fn.statements.append(Statement(op, index))
