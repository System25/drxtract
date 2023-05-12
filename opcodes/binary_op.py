# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ../ast import BinaryOperation, BinaryOperationNames


#
# Binary operation Opcode.
#
class BinaryOperationOpcode:
  def __init__(self, opname, opcode)):
    Opcode.__init__(self, opcode))
    self.opname = opname

  def process(self, code, index, stack, statements_list):
    op = BinaryOperation(self.opname, index)
    op.left = stack.pop()
    op.right = stack.pop()
    stack.append(op)

#
# Mulitiply Opcode.
#
class MultiplyOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.MUL, 0x04)

#
# Addition Opcode.
#
class AddOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.ADD, 0x05)

#
# Substraction Opcode.
#
class SubOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.SUB, 0x06)

#
# Division Opcode.
#
class DivOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.DIV, 0x07)
    
#
# Modulus Opcode.
#
class ModOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.MOD, 0x08)

#
# String concatenation Opcode.
#
class ConcatOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.CONCAT, 0x0A)

#
# String concatenation with spaces Opcode.
#
class ConcatSpcOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.CONCAT_SPACES,
                                   0x0B)

#
# String contains Opcode.
#
class ContainsOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.CONTAINS,
                                   0x15) 

#
# String starts-with Opcode.
#
class StartsWithOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.START,
                                   0x16) 
    
#
# Less-than Opcode.
#
class LessThanOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.LT, 0x0C)

#
# Less-than-or-equal Opcode.
#
class LessThanEqOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.LTE, 0x0D)

#
# Not-equal Opcode.
#
class NotEqOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.NE, 0x0E)
 
#
# Equal Opcode.
#
class EqualOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.EQ, 0x0F)

#
# Greater-than Opcode.
#
class GreaterThanOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.GT, 0x10)

#
# Greater-than-or-equal Opcode.
#
class GreaterThanEqOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.GTE, 0x11)

#
# And Opcode.
#
class AndOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.AND, 0x12)

#
# Or Opcode.
#
class OrOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.OR, 0x13)


#
# Sprite intersects Opcode.
#
class IntersectsOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.INTERSECTS,
                                   0x19)

#
# Sprite within Opcode.
#
class WithinOpcode:
  def __init__(self)):
    BinaryOperationOpcode.__init__(self, BinaryOperationNames.WITHIN,
                                   0x1A)
    
    