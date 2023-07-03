# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode, BiOpcode
from ..ast import Node, StringOperation, UnaryOperation,\
    Statement, UnaryOperationNames, StringOperationNames, Function
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
        Opcode.__init__(self, 0x17)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op = stack.pop()           # The string to slice
        op = add_modifiers(self, op, stack, index)
        stack.append(op)

#
# Hilite Opcode.
#
class HiliteOpcode(Opcode):
    def __init__(self):
        Opcode.__init__(self, 0x18)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to hilite     
        field = add_modifiers(self, field, stack, index)
        
        op = UnaryOperation(UnaryOperationNames.HILITE, index)
        op.operand = field
        stack.append(op)

#
# Delete slice Opcode.
#
class DeleteSliceOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5B, 0x06)

    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()  # The field to delete     
        field = add_modifiers(self, field, stack, index)
        
        op = UnaryOperation(UnaryOperationNames.DELETE, index)
        op.operand = field
        stack.append(op)
        
        function.statements.append(Statement(op, index))
