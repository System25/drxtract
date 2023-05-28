# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ..ast import WindowTellStartOperation, WindowTellEndOperation, \
    Function, Node
from ..model import Context
from typing import List

#
# Tell window operation start Opcode.
#
class WindowTellStartOpcode(Opcode):
    def __init__(self):
        Opcode.__init__(self, 0x1C)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op = WindowTellStartOperation('win_tell_start', index)
        op.operand = stack.pop()
        stack.append(op)

#
# Tell window operation end Opcode.
#
class WindowTellEndOpcode(Opcode):
    def __init__(self):
        Opcode.__init__(self, 0x1D)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op = WindowTellEndOperation('win_tell_end', index)
        p = stack.pop()
        while p is not None:
            op.operands.append(p)
            p = stack.pop()
        
        function.statements.append(op)

