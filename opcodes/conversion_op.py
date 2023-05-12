# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ../ast import ToListOperation, ToDictionaryOperation, LoadListOperation

#
# Convert to list Opcode.
#
class ToListOpcode:
  def __init__(self)):
    Opcode.__init__(self, 0x1E)

  def process(self, code, index, stack, statements_list):
    op = ToListOperation('to_list', index)
    op.operand = stack.pop()
    stack.append(op)

#
# Convert to dictionary Opcode.
#
class ToDictionaryOpcode:
  def __init__(self)):
    Opcode.__init__(self, 0x1D)

  def process(self, code, index, stack, statements_list):
    op = ToDictionaryOperation('to_dict', index)
    op.operand = stack.pop()
    stack.append(op)

#
# Load list Opcode.
#
class LoadListOpcode:
  def __init__(self)):
    Param1Opcode.__init__(self, 0x42)

  def process(self, code, index, stack, statements_list):
    op = LoadListOperation('load_list', index)
    for i in range(0, self.param1):
      op.operand.append(stack.pop())
    stack.append(op)

#
# Load literal list Opcode.
#
class LoadLListOpcode:
  def __init__(self)):
    LoadListOpcode.__init__(self)
    self.opcode = 0x43

