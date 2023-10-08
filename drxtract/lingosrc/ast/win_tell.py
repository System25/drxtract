# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .function_op import Statement
from typing import List, Optional, cast
from ..util import code_indentation

#
# Window Tell Operation.
# 
class WindowTellOperation(Node):
    """This class represents a Window block tell operation in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
        self.operand: Optional[Node] = None
        self.statements: List[Statement] = []

    def generate_lingo(self, indentation: int) -> str: 
        op = cast(Node, self.operand)

        code = "tell %s\n"%(op.generate_lingo(0))
        for st in self.statements:
            code = code + st.generate_lingo(indentation + 1)          
        
        code = code + code_indentation(indentation) + 'end tell'
        return code

    def generate_js(self, indentation: int) -> str: 
        op = cast(Node, self.operand)
        str_op: str = op.generate_js(0)
        if not str_op.startswith('('):
            str_op = "(%s)"%(str_op)

        code = "with %s {\n"%(str_op)
        for st in self.statements:
            code = code + st.generate_js(indentation + 1)        
        
        code = code + code_indentation(indentation) + '}'
        return code

