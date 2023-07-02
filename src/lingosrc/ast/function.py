# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .variable import LocalVariable, GlobalVariable, ParameterName
from .conversion import LoadListOperation
from typing import List, Optional, cast
from ..util import code_indentation

#
# Statement class.
# 
class Statement(Node):
    """This class represents a statement in the AST"""
    
    def __init__(self, code: Node, position: int):
        Node.__init__(self, 'statement', position)
        self.code = code

    def generate_lingo(self, indentation: int) -> str: 
        if isinstance(self.code, CallFunction):
            cast(CallFunction, self.code).use_parenthesis = False
        return (code_indentation(indentation) + 
            self.code.generate_lingo(indentation) + '\n')

    def generate_js(self, indentation: int) -> str:
        js_code:str = self.code.generate_js(indentation);
        if 'getPropRef' in js_code:
            li = js_code.rsplit('getPropRef', 1)
            js_code = 'getProp'.join(li)
        if js_code.endswith('}'):
            return code_indentation(indentation) + js_code + '\n'
        else:       
            return code_indentation(indentation) + js_code + ';\n'

        
#
# Function class.
# 
class Function(Node):
    """This class represents a function in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.parameters: List[ParameterName] = []
        self.local_vars: List[LocalVariable] = []
        self.global_vars: List[GlobalVariable] = []
        self.statements: List[Statement] = []

#
# Call function operation class.
# 
class CallFunction(Node):
    """This class represents a function call in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.parameters: Optional[Node] = None
        self.use_parenthesis: bool = True

    def generate_lingo(self, indentation: int) -> str: 
        if (self.parameters is not None
            and len(cast(LoadListOperation, self.parameters).operands) > 0):
            
            params: Node = cast(Node, self.parameters)
            if self.use_parenthesis:
                return self.name + '('+params.generate_lingo(indentation)+')'
            else:    
                return self.name + ' ' + params.generate_lingo(indentation)
        else:
            return self.name

    def generate_js(self, indentation: int) -> str:
        nm = self.name
        if nm == 'birth':
            nm = '_movie.newScript'
        
        params_str: str = ''
        if self.parameters is not None:
            params: Node = cast(Node, self.parameters)
            params_str = params.generate_js(indentation)
            
        if nm == 'new':
            if params_str.startswith('symbol('):
                nm = '_movie.newMember'
            else:
                nm = '_movie.newScript'
            
        if nm == 'go':
            if params_str.startswith('symbol(\''):
                p = params_str[len('symbol(\''):-2]
                nm = '_movie.go' + p.capitalize()
                params_str = ''
            else:
                nm = '_movie.go'
            
        return self.generate_js_code(nm, params_str)

    
    def generate_js_code(self, nm: str, params: str) -> str:
        if nm in ['return']:
            if params != '':      
                return nm + ' ' + params;
            else:
                return nm;
        else:
            return nm + '(' + params + ')'
#
# Call method operation class.
# 
class CallMethod(Node):
    """This class represents a method call in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
        self.object: Optional[Node] = None
        self.parameters: Optional[Node] = None
