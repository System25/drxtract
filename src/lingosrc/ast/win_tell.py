# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from typing import List, Optional

#
# Window Tell Start Operation class.
# 
class WindowTellStartOperation(Node):
    """This class represents the start of a Window tell operation in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.operand: Optional[Node] = None

#
# Window Tell End Operation class.
# 
class WindowTellEndOperation(Node):
    """This class represents the end of a Window tell operation in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.operands: List[Node] = []
