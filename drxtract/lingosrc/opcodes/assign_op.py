# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode, BiOpcode
from ..ast import GlobalVariable, PropertyName, \
   BinaryOperation, BinaryOperationNames, SpAssignOperation, \
   UnaryOperation, UnaryOperationNames, Statement, Node, \
   ConstantValue, FunctionDef, PropertyAccessorOperation, LocalVariable
from ..model import Context
from typing import List


KNOWN_PROPERTIES = {
    'updateMovieEnabled': '_movie'
}

#
# Assign to global variable Opcode.
#
class AssignGlobalVariableOpcode(Param1Opcode):  
    def __init__(self):
        super().__init__(0x4E)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = GlobalVariable(context.name_list[op1], index)
        op.right = stack.pop()
        fn.statements.append(Statement(op, index))
        
        if not op.left in fn.global_vars:
            fn.global_vars.append(op.left)

    
#
# Assign to global variable Opcode.
#
class AssignGlobalVarOpcode(AssignGlobalVariableOpcode):
    def __init__(self):
        super().__init__()
        self.opcode = 0x4F

#
# Load property Opcode.
#
class LoadPropertyOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x5F)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        property_name = context.name_list[op1]
        op: Node = PropertyName(property_name, index)
        if property_name in KNOWN_PROPERTIES.keys():
            obj: Node = LocalVariable(KNOWN_PROPERTIES[property_name], index)
            op = PropertyAccessorOperation(obj, property_name, index)
        
        stack.append(op)

#
# Assign to property Opcode.
#
class AssignPropertyOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x50)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        if context.name_list[op1] in context.properties:
            op.left = PropertyAccessorOperation(Node('me', index),
                                                context.name_list[op1],
                                                index)
        else:    
            op.left = PropertyName(context.name_list[op1], index)
        op.right = stack.pop()
        fn.statements.append(Statement(op, index))

#
# Assign to property Opcode.
#
class AssignValToPropertyOpcode(AssignPropertyOpcode):
    def __init__(self):
        super().__init__()
        self.opcode = 0x60


#
# Assign to parameter Opcode.
#
class AssignParameterOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x51)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        idx: int = int(op1 / context.bytes_per_constant)
        op.left = fn.parameters[idx]
        op.right = stack.pop()
        
        fn.statements.append(Statement(op, index))

#
# Assign to local variable Opcode.
#
class AssignLocalVariableOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x52)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        idx: int = int(op1 / context.bytes_per_constant)
        op.left = fn.local_vars[idx]
        op.right = stack.pop()
        
        fn.statements.append(Statement(op, index))


#
# Assign <mode> local var Opcode.
#
class AssignModeLocalVarOpcode(BiOpcode):
    def __init__(self, opcode1: int, opcode2: int, mode: str):
        super().__init__(opcode1, opcode2)
        self.mode = mode

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        operand = stack.pop()
        if not isinstance(operand, ConstantValue):
            raise TypeError(
                'Operand needs to be a contant value but it is: %s'%(
                    ConstantValue))
        op1 = int(operand.name)
        if (op1 % context.bytes_per_constant) > 0:
            context.bytes_per_constant = (op1 % context.bytes_per_constant)
        
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        idx: int = int(op1 / context.bytes_per_constant)
        op.left = fn.local_vars[idx]
        op.right = stack.pop()
        op.mode = self.mode
        
        fn.statements.append(Statement(op, index))

#
# Assing <mode> field Opcode.
#
class AssignModeFieldOpcode(BiOpcode):
    def __init__(self, opcode1: int, opcode2: int, mode: str):
        super().__init__(opcode1, opcode2)
        self.mode = mode
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int): 
        op = SpAssignOperation(BinaryOperationNames.ASSIGN, index)
        op.left = UnaryOperation(UnaryOperationNames.FIELD, index)
        op.left.operand = stack.pop()
        op.right = stack.pop()
        op.mode = self.mode
        
        fn.statements.append(Statement(op, index))

#
# Assign into local var Opcode.
#
class AssignIntoLocalVarOpcode(AssignModeLocalVarOpcode):
    def __init__(self):
        super().__init__(0x59, 0x15, 'into')


#
# Assing into field Opcode.
#
class AssignIntoFieldOpcode(AssignModeFieldOpcode):
    def __init__(self):
        super().__init__(0x59, 0x16, 'into')



#
# Assign after local var Opcode.
#
class AssignAfterLocalVarOpcode(AssignModeLocalVarOpcode):
    def __init__(self):
        super().__init__(0x59, 0x25, 'after')

#
# Assing after field Opcode.
#
class AssignAfterFieldOpcode(AssignModeFieldOpcode):
    def __init__(self):
        super().__init__(0x59, 0x26, 'after')


#
# Assign before local var Opcode.
#
class AssignBeforeLocalVarOpcode(AssignModeLocalVarOpcode):
    def __init__(self):
        super().__init__(0x59, 0x35, 'before')

#
# Assing before field Opcode.
#
class AssignBeforeFieldOpcode(AssignModeFieldOpcode):
    def __init__(self):
        super().__init__(0x59, 0x36, 'before')

