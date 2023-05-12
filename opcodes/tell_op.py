# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ../ast import WindowTellStartOperation, WindowTellEndOperation

#
# Tell window operation start Opcode.
#
class WindowTellStartOpcode:
  def __init__(self)):
    Opcode.__init__(self, 0x1C))

  def process(self, code, index, stack, statements_list):
    op = WindowTellStartOperation('win_tell_start', index)
    op.operand = stack.pop()
    stack.append(op)

#
# Tell window operation end Opcode.
#
class WindowTellEndOpcode:
  def __init__(self)):
    Opcode.__init__(self, 0x1D))

  def process(self, code, index, stack, statements_list):
    op = WindowTellEndOperation('win_tell_end', index)
    p = stack.pop()
    while p is not None:
      op.operands.append(p)
      p = stack.pop()
    
    stack.append(op)

