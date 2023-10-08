# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode, Param1Opcode, Param2Opcode
from ..ast import ConstantValue, FunctionDef, Symbol, PropertyName, Node
from ..model.context import Context
from typing import List


#
# Zero Opcode.
#
class ZeroOpcode(Opcode):
    def __init__(self):
        super().__init__(0x03)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        stack.append(ConstantValue('0', index))

#
# 1 byte integer Opcode.
#
class Int1bOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x41)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        v = self.param1
        if v > 127:
            v = v - 256
        stack.append(ConstantValue(str(v), index))

#
# 2 byte integer Opcode.
#
class Int2bOpcode(Param2Opcode):
    def __init__(self):
        super().__init__(0x81)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        v = self.param1 * 256 + self.param2
        if v > 32767:
            v = v - 65536
        stack.append(ConstantValue(str(v), index))
    
#
# Load literal Opcode.
#
class LiteralOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x44)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
    
        idx: int = int(op1 / context.bytes_per_constant)
        constant_value = context.constants[idx]
    
        stack.append(ConstantValue(constant_value, index))

#
# Load literal (2 byte index) Opcode.
#
class Literal2Opcode(Param2Opcode):
    def __init__(self):
        super().__init__(0x84)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1 * 256 + self.param2
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
    
        idx: int = int(op1 / context.bytes_per_constant)
        constant_value = context.constants[idx]
    
        stack.append(ConstantValue(constant_value, index))

#
# Load symbol Opcode.
#
class SymbolOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x45)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        stack.append(Symbol(context.name_list[op1], index))

#
# Load property Opcode.
#
class PropertyOpcode(Param1Opcode):
    def __init__(self):
        # TODO! Find code!!!
        super().__init__(0x99)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        stack.append(PropertyName(context.name_list[op1], index))

