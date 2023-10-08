# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ..ast import BinaryOperation, BinaryOperationNames, FunctionDef, \
    Node
from ..model import Context
from typing import List

#
# Binary operation Opcode.
#
class BinaryOperationOpcode(Opcode):
    """This class process a binary operation opcode"""
    
    def __init__(self, opname: BinaryOperationNames, opcode: int):
        super().__init__(opcode)
        self.opname: BinaryOperationNames = opname
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = BinaryOperation(self.opname, index)
        op.right = stack.pop()
        op.left = stack.pop()
        stack.append(op)

#
# Mulitiply Opcode.
#
class MultiplyOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.MUL, 0x04)

#
# Addition Opcode.
#
class AddOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.ADD, 0x05)

#
# Substraction Opcode.
#
class SubOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.SUB, 0x06)

#
# Division Opcode.
#
class DivOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.DIV, 0x07)
    
#
# Modulus Opcode.
#
class ModOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.MOD, 0x08)

#
# String concatenation Opcode.
#
class ConcatOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.CONCAT, 0x0A)

#
# String concatenation with spaces Opcode.
#
class ConcatSpcOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.CONCAT_SPACES,
                                   0x0B)

#
# String contains Opcode.
#
class ContainsOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.CONTAINS,
                                       0x15) 

#
# String starts-with Opcode.
#
class StartsWithOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.START,
                                       0x16) 
    
#
# Less-than Opcode.
#
class LessThanOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.LT, 0x0C)

#
# Less-than-or-equal Opcode.
#
class LessThanEqOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.LTE, 0x0D)

#
# Not-equal Opcode.
#
class NotEqOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.NE, 0x0E)
 
#
# Equal Opcode.
#
class EqualOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.EQ, 0x0F)

#
# Greater-than Opcode.
#
class GreaterThanOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.GT, 0x10)

#
# Greater-than-or-equal Opcode.
#
class GreaterThanEqOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.GTE, 0x11)

#
# And Opcode.
#
class AndOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.AND, 0x12)

#
# Or Opcode.
#
class OrOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.OR, 0x13)


#
# Sprite intersects Opcode.
#
class IntersectsOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.INTERSECTS,
                                       0x19)

#
# Sprite within Opcode.
#
class WithinOpcode(BinaryOperationOpcode):
    def __init__(self):
        super().__init__(BinaryOperationNames.WITHIN,
                                       0x1A)
    
    