# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ../ast import UnaryOperation, UnaryOperationNames

#
# Binary operation Opcode.
#
class UnaryOperationOpcode:
  def __init__(self, opname, opcode):
    Opcode.__init__(self, opcode)
    self.opname = opname

  def process(self, code, index, stack, statements_list):
    op = UnaryOperation(self.opname, index)
    op.operand = stack.pop()
    stack.append(op)

#
# Unary minus Opcode.
#
class MinusOpcode:
  def __init__(self)):
    UnaryOperationOpcode.__init__(self, UnaryOperationNames.MINUS, 0x09)

#
# Not Opcode.
#
class NotOpcode:
  def __init__(self)):
    UnaryOperationOpcode.__init__(self, UnaryOperationNames.NOT, 0x14)

#
# Field Opcode.
#
class FieldOpcode:
  def __init__(self)):
    UnaryOperationOpcode.__init__(self, UnaryOperationNames.FIELD, 0x1B)