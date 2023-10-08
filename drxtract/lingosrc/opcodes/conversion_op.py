# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode, Param1Opcode, Param2Opcode
from ..ast import ToListOperation, ToDictionaryOperation, \
    LoadListOperation, FunctionDef, Node
from ..model import Context
from typing import List, cast

#
# Convert to list Opcode.
#
class ToListOpcode(Opcode):
    def __init__(self):
        super().__init__(0x1E)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = ToListOperation('to_list', index, \
                             cast(LoadListOperation, stack.pop()))
        stack.append(op)

#
# Convert to dictionary Opcode.
#
class ToDictionaryOpcode(Opcode):
    def __init__(self):
        super().__init__(0x1F)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = ToDictionaryOperation('to_dict', index, \
                                   cast(LoadListOperation, stack.pop()))
        stack.append(op)

#
# Load list Opcode.
#
class LoadListOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x42)
        self.name = 'load_list'
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = LoadListOperation(self.name, index)
        for _ in range(0, self.param1):
            op.operands.append(stack.pop())
        stack.append(op)

#
# Load literal list Opcode.
#
class LoadLListOpcode(LoadListOpcode):
    def __init__(self):
        super().__init__()
        self.opcode = 0x43
        self.name = '<load_list>'

#
# Load long list Opcode.
#
class LoadLongListOpcode(Param2Opcode):
    def __init__(self):
        super().__init__(0x82)
        self.name = 'load_list'
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        n = self.param1 * 256 + self.param2
        op = LoadListOperation(self.name, index)
        for _ in range(0, n):
            op.operands.append(stack.pop())
        stack.append(op)

#
# Load long literal list Opcode.
#
class LoadLongLListOpcode(LoadLongListOpcode):
    def __init__(self):
        super().__init__()
        self.opcode = 0x83
        self.name = '<load_list>'

