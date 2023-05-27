# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Param1Opcode, Param2Opcode
from lingosrc.ast import ConstantValue, RepeatOperation, JumpOperation, \
    Statement, Node, JzOperation
from lingosrc.model import Context
from typing import List

#
# Unconditional jump backwards Opcode.
#
class JumpOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x54)
    
    def process(self, context: Context, stack: List[Node], \
                statements_list: List[Statement], index: int):
        op1 = self.param1
        start_index = index - 2 - op1
        
        op = RepeatOperation('repeat', start_index)
        op.condition = ConstantValue('TRUE', start_index)
        
        for stmnt in statements_list:
            if stmnt.position >= start_index:
                op.statements_list.append(stmnt)
        
        for stmnt in op.statements_list:
            statements_list.remove(stmnt)
        
        statements_list.append(Statement(op, index))

#
# Unconditional jump forward Opcode.
#
class FowardJumpOpcode(Param2Opcode):
    def __init__(self):
        Param2Opcode.__init__(self, 0x93)
    
    def process(self, context: Context, stack: List[Node], \
                statements_list: List[Statement], index: int):
        op1 = self.param1 * 256 + self.param2
        end_index = index + 3 + op1
        
        op = JumpOperation('jump', index)
        op.address = end_index
        
        statements_list.append(Statement(op, index))

#
# Conditional jump forward Opcode.
#
class ConditionalJumpOpcode(Param2Opcode):
    def __init__(self):
        Param2Opcode.__init__(self, 0x93)
    
    def process(self, context: Context, stack: List[Node], \
                statements_list: List[Statement], index: int):
        op1 = self.param1 * 256 + self.param2
        end_index = index + 3 + op1
        
        op = JzOperation('jz', index)
        op.address = end_index
        op.condition = stack.pop()
        
        statements_list.append(Statement(op, index))

