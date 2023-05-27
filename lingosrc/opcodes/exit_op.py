# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from lingosrc.ast import Statement, Node, CallFunction
from lingosrc.model import Context
from typing import List

#
# Exit Opcode.
#
class ExitOpcode(Opcode):
    def __init__(self):
        Opcode.__init__(self, 0x01)

    def process(self, context: Context, stack: List[Node], \
                statements_list: List[Statement], index: int):
        op = CallFunction('exit', index)
        statements_list.append(Statement(op, index))
