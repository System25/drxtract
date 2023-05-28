# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .variable import LocalVariable, GlobalVariable, ParameterName
from typing import List, Optional, cast
from ..util import code_indentation

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

    def generate_js(self, indentation: int) -> str: 
        return (code_indentation(indentation) + 
            self.code.generate_js(indentation) + ';\n')
        
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

    def generate_lingo(self, indentation: int) -> str: 
        if self.parameters is not None:
            params: Node = cast(Node, self.parameters)
            return self.name + ' ' + params.generate_lingo(indentation)
        else:
            return self.name

    def generate_js(self, indentation: int) -> str: 
        if self.parameters is not None:
            params: Node = cast(Node, self.parameters)
            return self.name + '(' + params.generate_js(indentation) + ')'
        else:
            return self.name + '()'

#
# Call method operation class.
# 
class CallMethod(Node):
    """This class represents a method call in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.object: Optional[Node] = None
        self.parameters: Optional[Node] = None
