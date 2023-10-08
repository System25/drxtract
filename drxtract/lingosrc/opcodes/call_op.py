# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode
from ..ast import CallMethod, CallFunction, Statement, Node, \
    ToListOperation, FunctionDef, Symbol, LoadListOperation, GlobalVariable
from ..model import Context
from typing import List, cast


#
# Call a local function Opcode.
#
class CallLocalOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x56)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        fname = context.local_func_names[op1]
        
        op = CallFunction(fname, index)
        op.parameters = stack.pop()
        
        if op.parameters is not None and op.parameters.name.startswith('<'):
            stack.append(op)
        else:
            fn.statements.append(Statement(op, index))

#
# Call an external function Opcode.
#
class CallExternalOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x57)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        fname = context.name_list[op1]
        
        op = CallFunction(fname, index)
        op.parameters = stack.pop()
        
        if op.parameters is not None and op.parameters.name.startswith('<'):
            stack.append(op)
        else:
            fn.statements.append(Statement(op, index))


#
# Call a function with an external global var parameter.
#
# For example:
#   -- First cast element
#   on startMovie
#     global myList <-- DEFINE myList AS GLOBAL AS MOVIE LEVEL
#     set myList = [#the_70s: 1970, #the_80s: 1980, #the_90: 1990]
#   end
#
#   -- Second cast element
#   on exitFrame
#     put "90s: ", findPos(myList, 1990) <-- USE myList WITHOUT DEFINING IT
#   end
#
class CallFuncWithExtGlobalOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x58)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        ext_global_name = context.name_list[op1]
        
        fname = cast(Node, stack.pop()).generate_lingo(0)
        
        params: LoadListOperation = cast(LoadListOperation, stack.pop())
        op = CallFunction(fname, index)
        op.parameters = params
        operands = params.operands
        op.parameters.operands = []
        
        for p in operands:
            if isinstance(p, Symbol) and p.name == ext_global_name:
                p = GlobalVariable(p.name, p.position)
            op.parameters.operands.append(p)
        
        if op.parameters.name.startswith('<'):
            stack.append(op)
        else:
            fn.statements.append(Statement(op, index))

#
# Call an object method Opcode.
#
class CallExternalMethodOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x67)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
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
            fn.statements.append(Statement(op, index))
