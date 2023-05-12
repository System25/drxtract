# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node

#
# Function class.
# 
class Function:
  def __init__(self, name, position)):
    Node.__init__(self, name, position))
    self.parameters = []
		self.local_vars = []
    self.global_vars = []
    self.statements = []
