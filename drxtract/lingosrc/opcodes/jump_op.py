# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode, Param2Opcode
from ..ast import ConstantValue, RepeatOperation, JumpOperation, \
    Statement, Node, JzOperation, FunctionDef
from ..model import Context
from typing import List

#
# Unconditional jump backwards Opcode.
#
class JumpOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x54)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        start_index = index - op1
        
        op = RepeatOperation('repeat', start_index, index)
        op.condition = ConstantValue('TRUE', start_index)
        
        for stmnt in fn.statements:
            if stmnt.position >= start_index:
                op.statements_list.append(stmnt)
        
        for stmnt in op.statements_list:
            fn.statements.remove(stmnt)
        
        fn.statements.append(Statement(op, index))

#
# Unconditional jump forward Opcode.
#
class FowardJumpOpcode(Param2Opcode):
    def __init__(self):
        super().__init__(0x93)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1 * 256 + self.param2
        end_index = index + op1
        
        op = JumpOperation('jump', index)
        op.address = end_index
        
        fn.statements.append(Statement(op, index))

#
# Conditional jump forward Opcode.
#
class ConditionalJumpOpcode(Param2Opcode):
    def __init__(self):
        super().__init__(0x95)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1 * 256 + self.param2
        end_index = index + op1
        
        op = JzOperation('jz', index)
        op.address = end_index
        op.condition = stack.pop()
        
        fn.statements.append(Statement(op, index))

