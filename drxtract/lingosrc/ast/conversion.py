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
        super().__init__(name, position)
        self.operands: List[Node] = []

    def generate_lingo(self, indentation: int) -> str:
        oplist: List[str] = []
        for s in self.operands:
            oplist.append(str(s.generate_lingo(indentation)))

        oplist.reverse()
        return ', '.join(oplist)

    def generate_js(self, indentation: int) -> str:
        oplist: List[str] = []
        for s in self.operands:
            oplist.append(str(s.generate_js(indentation)))

        oplist.reverse()
        return ', '.join(oplist)

#
# Convert to list Operation class.
# 
class ToListOperation(Node):
    """This class represents an operation to convert the operand into a list
     as a node in the AST"""
     
    def __init__(self, name: str, position: int, operand: LoadListOperation):
        super().__init__(name, position)
        self.operand: LoadListOperation = operand

    def generate_lingo(self, indentation: int) -> str:       
        oplist: List[str] = []
        for s in self.operand.operands:
            oplist.append(str(s.generate_lingo(indentation)))

        oplist.reverse()
        return '[' + ', '.join(oplist) +  ']'
    
    def generate_js(self, indentation: int) -> str:
        oplist: List[str] = []
        for s in self.operand.operands:
            oplist.append(str(s.generate_js(indentation)))

        oplist.reverse()
        return 'list(' + ', '.join(oplist) +  ')'
#
# Convert to dictionary Operation class.
# 
class ToDictionaryOperation(Node):
    """This class represents an operation to convert the operand into a dict
     as a node in the AST"""
     
    def __init__(self, name: str, position: int, operand: LoadListOperation):
        super().__init__(name, position)
        self.operand: LoadListOperation = operand

    def generate_lingo(self, indentation: int) -> str:
        oplist: List[str] = []
        for i in range(0, len(self.operand.operands), 2):
            j = i + 1
            val = self.operand.operands[i].generate_lingo(indentation)
            sym = self.operand.operands[j].generate_lingo(indentation)
                   
            oplist.append("%s: %s"%(sym, val))

        oplist.reverse()
        
        if len(oplist) == 0:
            return '[:]'
        
        return '[' + ', '.join(oplist) +  ']'
    
    def generate_js(self, indentation: int) -> str:
        oplist: List[str] = []
        for s in self.operand.operands:
            oplist.append(str(s.generate_js(indentation)))

        oplist.reverse()
        return 'propList(' + ', '.join(oplist) +  ')'
