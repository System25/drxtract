# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ..ast import Statement, Node, CallFunction, FunctionDef
from ..model import Context
from typing import List

#
# Exit Opcode.
#
class ExitOpcode(Opcode):
    def __init__(self):
        super().__init__(0x01)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = CallFunction('exit', index)
        fn.statements.append(Statement(op, index))
