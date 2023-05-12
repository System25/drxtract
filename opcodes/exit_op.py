# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ../ast import Statement

#
# Exit Opcode.
#
class ExitOpcode:
  def __init__(self)):
    Opcode.__init__(self, 0x01))

  @abstractmethod
  def process(self, code, index, stack, statements_list):
    statements_list.append(Statement('exit', index) 
