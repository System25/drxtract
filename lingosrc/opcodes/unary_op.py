# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from lingosrc.ast import UnaryOperation, UnaryOperationNames, Function, Node
from lingosrc.model import Context
from typing import List

#
# Binary operation Opcode.
#
class UnaryOperationOpcode(Opcode):
    def __init__(self, opname, opcode):
        Opcode.__init__(self, opcode)
        self.opname = opname
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op = UnaryOperation(self.opname, index)
        op.operand = stack.pop()
        stack.append(op)

#
# Unary minus Opcode.
#
class MinusOpcode(UnaryOperationOpcode):
    def __init__(self):
        UnaryOperationOpcode.__init__(self, UnaryOperationNames.MINUS, 0x09)

#
# Not Opcode.
#
class NotOpcode(UnaryOperationOpcode):
    def __init__(self):
        UnaryOperationOpcode.__init__(self, UnaryOperationNames.NOT, 0x14)

#
# Field Opcode.
#
class FieldOpcode(UnaryOperationOpcode):
    def __init__(self):
        UnaryOperationOpcode.__init__(self, UnaryOperationNames.FIELD, 0x1B)
