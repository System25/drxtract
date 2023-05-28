# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode
from ..ast import CallMethod, CallFunction, Statement, Node, \
    ToListOperation, Function
from ..model import Context
from typing import List, cast


#
# Call a local function Opcode.
#
class CallLocalOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x56)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        fname = context.local_func_names[op1]
        
        op = CallFunction(fname, index)
        op.parameters = stack.pop()
        
        if op.parameters is not None and op.parameters.name.startswith('<'):
            stack.append(op)
        else:
            function.statements.append(Statement(op, index))

#
# Call an external function Opcode.
#
class CallExternalOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x57)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        fname = context.name_list[op1]
        
        op = CallFunction(fname, index)
        op.parameters = stack.pop()
        
        if op.parameters is not None and op.parameters.name.startswith('<'):
            stack.append(op)
        else:
            function.statements.append(Statement(op, index))


#
# Call an object method Opcode.
#
class CallMethodOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x58)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        raise Exception("CallMethodOpcode not implemented!")

#
# Call an object method Opcode.
#
class CallExternalMethodOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x67)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        fname = context.name_list[op1]
        
        params: ToListOperation = cast(ToListOperation, stack.pop())
        obj = params.operand.operands[0]
        params.operand.operands = params.operand.operands[1:]
        
        op = CallMethod(fname, index)
        op.object = obj
        op.parameters = params.operand
        
        if op.parameters is not None and op.parameters.name.startswith('<'):
            stack.append(op)
        else:
            function.statements.append(Statement(op, index))
