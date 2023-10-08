# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ..ast import UnaryOperation, UnaryOperationNames, FunctionDef, Node
from ..model import Context
from typing import List

#
# Binary operation Opcode.
#
class UnaryOperationOpcode(Opcode):
    def __init__(self, opname, opcode):
        super().__init__(opcode)
        self.opname = opname
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = UnaryOperation(self.opname, index)
        op.operand = stack.pop()
        stack.append(op)

#
# Unary minus Opcode.
#
class MinusOpcode(UnaryOperationOpcode):
    def __init__(self):
        super().__init__(UnaryOperationNames.MINUS, 0x09)

#
# Not Opcode.
#
class NotOpcode(UnaryOperationOpcode):
    def __init__(self):
        super().__init__(UnaryOperationNames.NOT, 0x14)

#
# Field Opcode.
#
class FieldOpcode(UnaryOperationOpcode):
    def __init__(self):
        super().__init__(UnaryOperationNames.FIELD, 0x1B)
