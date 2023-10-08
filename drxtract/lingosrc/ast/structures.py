# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .function_op import Statement
from typing import List, Optional, cast
from ..util import code_indentation

#
# Repeat Operation class.
# 
class RepeatOperation(Node):
    """This class represents a repeat loop in the AST"""
    
    def __init__(self, name: str, position: int, end_position: int):
        super().__init__(name, position)
        self.end_position: int = end_position
        self.condition: Optional[Node] = None
        self.statements_list: List[Statement] = []
        self.type: str = 'while'
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.varname: str = ''
        self.sign: str = ''

    def generate_lingo(self, indentation: int) -> str: 
        cond = cast(Node, self.condition)
        str_cond: str = cond.generate_lingo(0)
        if str_cond.startswith('('):
            str_cond = str_cond[1:-1]

        if self.type == 'while':
            code = "repeat while %s\n"%(str_cond)
        elif self.type == 'for':
            code = "repeat with %s = %s %s %s\n"%(self.varname,
                    cast(Node, self.start).generate_lingo(0),
                    'to' if self.sign == '+' else 'down to',
                    cast(Node, self.end).generate_lingo(0))
        else:
            code = "repeat with %s in %s\n"%(self.varname,
                        cast(Node, self.start).generate_lingo(0))
        
        for st in self.statements_list:
            code = code + st.generate_lingo(indentation + 1)
        
        code = code + code_indentation(indentation) + 'end repeat'
        return code

    def generate_js(self, indentation: int) -> str: 
        cond = cast(Node, self.condition)
        str_cond: str = cond.generate_js(0)
        if not str_cond.startswith('('):
            str_cond = "(%s)"%(str_cond)

        if self.type == 'while':
            code = "while %s {\n"%(str_cond)
        elif self.type == 'for':
            code = "for(%s = %s; %s; %s%s) {\n"%(self.varname,
                    cast(Node, self.start).generate_js(0),
                    str_cond[1:-1],
                    self.varname,
                    '++' if self.sign == '+' else '--')
        else:
            code = "for(%s of %s) {\n"%(self.varname,
                        cast(Node, self.start).generate_js(0))
        
        for st in self.statements_list:
            code = code + st.generate_js(indentation + 1)           
        
        code = code + code_indentation(indentation) + '}'
        return code

#
# If-then Operation class.
# 
class IfThenOperation(Node):
    """This class represents an if-then-else structure in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
        self.condition: Optional[Node] = None
        self.if_statements_list: List[Statement] = []
        self.else_statements_list: List[Statement] = []

    def generate_lingo(self, indentation: int) -> str: 
        cond = cast(Node, self.condition)

        code = "if %s then\n"%(cond.generate_lingo(0))
        for st in self.if_statements_list:
            code = code + st.generate_lingo(indentation + 1)
        
        if len(self.else_statements_list) > 0:
            code = code + code_indentation(indentation) + 'else\n'
            for st in self.else_statements_list:
                code = code + st.generate_lingo(indentation + 1)            
        
        code = code + code_indentation(indentation) + 'end if'
        return code

    def generate_js(self, indentation: int) -> str: 
        cond = cast(Node, self.condition)
        str_cond: str = cond.generate_js(0)
        if not str_cond.startswith('('):
            str_cond = "(%s)"%(str_cond)

        code = "if %s {\n"%(str_cond)
        for st in self.if_statements_list:
            code = code + st.generate_js(indentation + 1)
        
        if len(self.else_statements_list) > 0:
            code = code + code_indentation(indentation) + '} else {\n'
            for st in self.else_statements_list:
                code = code + st.generate_js(indentation + 1)            
        
        code = code + code_indentation(indentation) + '}'
        return code

#
# Jump Operation class.
# 
class JumpOperation(Node):
    """This class represents an inconditional jump operation in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
        self.address: Optional[int] = None


#
# Jump if zero Operation class.
# 
class JzOperation(Node):
    """This class represents a conditional jump operation in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
        self.condition: Optional[Node] = None
        self.address: Optional[int] = None

#
# Exit repeat class.
# 
class ExitRepeat(Node):
    """This class represents an exit repeat loop operation"""
    
    def __init__(self, position: int):
        super().__init__('exit repeat', position)

    def generate_js(self, indentation: int) -> str: 
        return 'break'
