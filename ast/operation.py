# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from enum import Enum

#
# Unary Operation class.
# 
class UnaryOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
		self.operand = None

#
# Binary Operation class.
# 
class BinaryOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
    self.left = None
		self.right = None

#
# String Operation class.
# 
class StringOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
		self.start = None
    self.end = None
    self.of = None
    

#
# Binary Operation names enumeration.
# 
class BinaryOperationNames(Enum):
  ADD = 'add'
  SUB = 'sub'
  MUL = 'mul'
  DIV = 'div'
  MOD = 'mod'
  
  CONCAT = 'concat'
  CONCAT_SPACES = 'concats'
  CONTAINS = 'contains'
  START = 'start'
  
  AND = 'and'
  OR = 'or'
  
  LT = 'lt'
  LTE = 'lte'
  GT = 'gt'
  GTE = 'gte'
  EQ = 'eq'
  NE = 'ne'
  
  INTERSECTS = 'intersects'
  WITHIN = 'within'
  
  
  
#
# Unary Operation names enumeration.
# 
class UnaryOperationNames(Enum):
  MINUS = 'minus'
  NOT = 'not'
  FIELD = 'field'

#
# String Operation names enumeration.
# 
class StringOperationNames(Enum):
  WORD = 'word'
  CHAR = 'char'
  ITEM = 'item'
  LINE = 'line'
  