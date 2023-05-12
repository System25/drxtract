# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node

#
# Convert to list Operation class.
# 
class ToListOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
		self.operand = None

#
# Convert to dictionary Operation class.
# 
class ToDictionaryOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
    self.operand = None

#
# Load a list Operation class.
# 
class LoadListOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
		self.operands = []
