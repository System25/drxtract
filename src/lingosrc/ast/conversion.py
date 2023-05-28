# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from typing import List

#
# Load a list Operation class.
# 
class LoadListOperation(Node):
    """This class represents an operation to load a list as a node in the AST"""
     
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.operands: List[Node] = []

    def generate_lingo(self, indentation: int) -> str:       
        oplist = list(str(s.generate_lingo(indentation))
                      for s in self.operands)

        oplist.reverse()
        return ', '.join(oplist)

#
# Convert to list Operation class.
# 
class ToListOperation(Node):
    """This class represents an operation to convert the operand into a list
     as a node in the AST"""
     
    def __init__(self, name: str, position: int, operand: LoadListOperation):
        Node.__init__(self, name, position)
        self.operand: LoadListOperation = operand

    def generate_lingo(self, indentation: int) -> str:       
        oplist = list(str(s.generate_lingo(indentation))
                      for s in self.operand.operands)

        oplist.reverse()
        return '[' + ', '.join(oplist) +  ']'
#
# Convert to dictionary Operation class.
# 
class ToDictionaryOperation(Node):
    """This class represents an operation to convert the operand into a dict
     as a node in the AST"""
     
    def __init__(self, name: str, position: int, operand: LoadListOperation):
        Node.__init__(self, name, position)
        self.operand: LoadListOperation = operand

