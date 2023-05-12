# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode, Param1Opcode
from ../ast import ConstantValue

#
# Zero Opcode.
#
class ZeroOpcode:
  def __init__(self):
    Opcode.__init__(self, 0x03)

  def process(self, code, index, stack, statements_list):
    stack.append(ConstantValue('0', index))

#
# 1 byte integer Opcode.
#
class Int1bOpcode:
  def __init__(self):
    Param1Opcode.__init__(self, 0x41)

  def process(self, code, index, stack, statements_list):
    v = int(self.param1)
    if v > 127:
        v = v - 256
    stack.append(ConstantValue(v, index))

#
# Load literal Opcode.
#
class Int1bOpcode:
  def __init__(self):
    Param1Opcode.__init__(self, 0x44)

  def process(self, code, index, stack, statements_list):
    v = int(self.param1)
    TODO!!
    stack.append(ConstantValue(v, index))