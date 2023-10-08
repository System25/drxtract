# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode
from ..ast import FunctionDef, Node
from ..model import Context
from typing import List

#
# Copy a symbol from the stack Opcode.
#
class CopySymbolOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x64)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        idx: int = len(stack) - 1 - op1
        stack.append(stack[idx])    

#
# Discard values from the stack Opcode.
#
class DiscardSymbolsOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x65)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        for _ in range(0, op1):
            stack.pop()
