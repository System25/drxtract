# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode
from ..ast import CallMethod, CallFunction, Statement, Node, \
    ToListOperation, FunctionDef, Symbol, LoadListOperation, GlobalVariable, \
    ConstantValue
from ..model import Context
from typing import List, cast
from ..util import vsprintf


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


def findVarName(varType: int, context: Context, stack: List[Node], \
                fn: FunctionDef):
    if (varType == 1 or varType == 2 or varType == 3):
        # Global or local variable
        obj = cast(Node, stack.pop())
        return obj.generate_lingo(0)
    
    elif varType == 4:
        # Argument
        argNum = cast(ConstantValue, stack.pop()).name
        num = int(argNum)
        if (num % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (num % context.bytes_per_constant)
        
        idx = int(num / context.bytes_per_constant)
        return fn.parameters[idx].name
        
    elif varType == 5:
        # local variable
        lvNum = cast(ConstantValue, stack.pop()).name
        num = int(lvNum)
        if (num % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (num % context.bytes_per_constant)
        
        idx = int(num / context.bytes_per_constant)
        return fn.local_vars[idx].name

    elif varType == 6:
        # field
        raise Exception("Missing example with field!")
    
    else:
        message = vsprintf("Unknown vartype: %s", varType)
        raise Exception(message)


#
# Call an object method.
#
class CallObjectMethodOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x58)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        var_type = self.param1
        fname = findVarName(var_type, context, stack, fn)
                    
        params: LoadListOperation = cast(LoadListOperation, stack.pop())
        op = CallFunction(fname, index)
        op.parameters = params
        operands = params.operands
        op.parameters.operands = []
        
        first_op = None
        for p in operands:
            op.parameters.operands.append(p)
            first_op = p
        
        if first_op is not None and isinstance(first_op, Symbol):
            # Avoid writing the hash symbol in the first operand
            sym: Symbol = first_op
            sym.use_hash = False        
        
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
