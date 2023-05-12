# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ../ast import StringOperation, StringOperationNames, ConstantValue

#
# String slice operation Opcode.
#
class StringOperationOpcode:
  def __init__(self):
    Opcode.__init__(self, 0x17)

  def add_str_operation(op, start_pos, end_pos, name):
    operation = op
    
    if !isinstance(start_pos, ConstantValue) or  start_pos.name != '0':
      operation = StringOperation(name, index)
      operation.of = op
      operation.start = start_pos
      
      if !isinstance(end_pos, ConstantValue) or  end_pos.name != '0':
        operation.end = end_pos

    return operation

  def process(self, code, index, stack, statements_list):

    op = stack.pop()           # The string to slice
    op_ll_pos = stack.pop()    # Last line position
    op_fl_pos = stack.pop()    # First line position
    op_li_pos = stack.pop()    # Last item position
    op_fi_pos = stack.pop()    # First item position
    # (items separated by the itemDelimiter, which is a comma by default)
    op_lw_pos = stack.pop()    # Last word position
    op_fw_pos = stack.pop()    # First word position
    op_lc_pos = stack.pop()    # Last char position
    op_fc_pos = stack.pop()    # First char position

    op = add_str_operation(op, op_fc_pos, op_lc_pos, StringOperation.CHAR)
    op = add_str_operation(op, op_fw_pos, op_lw_pos, StringOperation.WORD)
    op = add_str_operation(op, op_fi_pos, op_li_pos, StringOperation.ITEM)
    op = add_str_operation(op, op_fl_pos, op_ll_pos, StringOperation.LINE)

    stack.append(op)

#
# Hilite Opcode.
#
class HiliteOpcode:
  def __init__(self)):
    StringOperationOpcode.__init__(self)
    self.opcode = 0x18
    


