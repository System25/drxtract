# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode
from ..ast import LocalVariable, GlobalVariable, DefinedPropertyName, \
    Function, ParameterName, Node, CallFunction, Statement
from ..model import Context
from typing import List


#
# Use local variable Opcode.
#
class VariableOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x46)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        gv = GlobalVariable(context.name_list[op1], index)
        if not gv in function.global_vars:
            stack.append(LocalVariable(context.name_list[op1], index))
        else:
            stack.append(gv)

#
# Use global variable Opcode.
#
class GlobalVariableOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x48)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        gv = GlobalVariable(context.name_list[op1], index)
        stack.append(gv)
        
        if not gv in function.global_vars:
            function.global_vars.append(gv)
    
#
# Use global variable Opcode.
#
class GlobalVarOpcode(GlobalVariableOpcode):
    def __init__(self):
        GlobalVariableOpcode.__init__(self)
        self.opcode = 0x49

#
# Use property name Opcode.
#
class PropertyNameOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x4A)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        stack.append(DefinedPropertyName(context.name_list[op1], index))

#
# Use parameter name Opcode.
#
class ParameterNameOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x4B)

    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
        
        value = function.parameters[int(op1 / context.bytes_per_constant)]
        
        stack.append(ParameterName(value.name, index))
    
#
# Use local variable name Opcode.
#
class LocalVariableOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x4C)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
        
        value = function.local_vars[int(op1 / context.bytes_per_constant)]
        
        stack.append(value)

#
# Property to tell commands.
#
class TellPropertyOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x63)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1

        op = CallFunction(context.name_list[op1], index)
        op.parameters = stack.pop()
        op.in_tell_operation = True
        function.statements.append(Statement(op, index)) 

