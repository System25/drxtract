# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node

#
# Window Tell Start Operation class.
# 
class WindowTellStartOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
		self.operand = None

#
# Window Tell End Operation class.
# 
class WindowTellEndOperation:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
    self.operands = []
