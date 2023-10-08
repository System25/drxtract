# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import Opcode
from ..ast import WindowTellOperation, \
    FunctionDef, Node, Statement
from ..model import Context
from typing import List, cast

#
# Tell window operation start Opcode.
#
class WindowTellStartOpcode(Opcode):
    def __init__(self):
        super().__init__(0x1C)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op = WindowTellOperation('tell', index)
        op.operand = stack.pop()
        fn.statements.append(Statement(op, index))
        context.tell_object = op.operand

#
# Tell window operation end Opcode.
#
class WindowTellEndOpcode(Opcode):
    def __init__(self):
        super().__init__(0x1D)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        statements: List[Statement] = []
        fn_statements: List[Statement] = []
        fn_statements.extend(fn.statements)
        fn_statements.reverse()
        
        for st in fn_statements:
            if not isinstance(st.code, WindowTellOperation):
                statements.append(st)
            else:
                op: WindowTellOperation = cast(WindowTellOperation, st.code)
                statements.reverse()
                op.statements.extend(statements)
                statements = op.statements
                break
                
        for st in statements:
            fn.statements.remove(st)
        
        context.tell_object = None
