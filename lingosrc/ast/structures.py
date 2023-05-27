# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .function import Statement
from typing import List, Optional
#
# Repeat Operation class.
# 
class RepeatOperation(Node):
    """This class represents a repeat loop in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.condition: Optional[Node] = None
        self.statements_list: List[Statement] = []

#
# If-then Operation class.
# 
class IfThenOperation(Node):
    """This class represents an if-then-else structure in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.condition: Optional[Node] = None
        self.if_statements_list: List[Statement] = []
        self.else_statements_list: List[Statement] = []

#
# Jump Operation class.
# 
class JumpOperation(Node):
    """This class represents an inconditional jump operation in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.address: Optional[int] = None


#
# Jump if zero Operation class.
# 
class JzOperation(Node):
    """This class represents a conditional jump operation in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.condition: Optional[Node] = None
        self.address: Optional[int] = None
