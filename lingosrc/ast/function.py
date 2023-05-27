# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .variable import LocalVariable, GlobalVariable, ParameterName
from typing import List, Optional
from lingosrc.util import code_indentation

#
# Statement class.
# 
class Statement(Node):
    """This class represents a statement in the AST"""
    
    def __init__(self, code: Node, position: int):
        Node.__init__(self, 'statement', position)
        self.code = code

    def generate_lingo(self, indentation: int) -> str: 
        return (code_indentation(indentation) + 
            self.code.generate_lingo(indentation) + '\n')


#
# Function class.
# 
class Function(Node):
    """This class represents a function in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.parameters: List[ParameterName] = []
        self.local_vars: List[LocalVariable] = []
        self.global_vars: List[GlobalVariable] = []
        self.statements: List[Statement] = []

#
# Call function operation class.
# 
class CallFunction(Node):
    """This class represents a function call in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.parameters: Optional[Node] = None

#
# Call method operation class.
# 
class CallMethod(Node):
    """This class represents a method call in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.object: Optional[Node] = None
        self.parameters: Optional[Node] = None
