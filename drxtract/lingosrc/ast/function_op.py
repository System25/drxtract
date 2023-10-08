# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .variable import LocalVariable, GlobalVariable, ParameterName
from .conversion import LoadListOperation
from .constant_val import Symbol
from typing import List, Optional, cast
from ..util import code_indentation

LIST_FUNCTIONS: List[str] = ['findpos', 'findposnear', 'getaprop', 'getone',
                             'getpos', 'getpropat', 'getprop']

#
# Statement class.
# 
class Statement(Node):
    """This class represents a statement in the AST"""
    
    def __init__(self, code: Node, position: int):
        super().__init__('statement', position)
        self.code = code

    def generate_lingo(self, indentation: int) -> str: 
        if isinstance(self.code, CallFunction):
            cast(CallFunction, self.code).use_parenthesis = False
        return (code_indentation(indentation) + 
            self.code.generate_lingo(indentation) + '\n')

    def generate_js(self, indentation: int) -> str:
        js_code:str = self.code.generate_js(indentation);
        if ('getPropRef' in js_code and not js_code.startswith('delete(')
            and not '=' in js_code[js_code.rindex('getPropRef'):]):
            li = js_code.rsplit('getPropRef', 1)
            js_code = 'getProp'.join(li)
        if js_code.endswith('}'):
            return code_indentation(indentation) + js_code + '\n'
        else:       
            return code_indentation(indentation) + js_code + ';\n'

        
#
# Function definition class.
# 
class FunctionDef(Node):
    """This class represents a function in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
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
        super().__init__(name, position)
        self.parameters: Optional[Node] = None
        self.use_parenthesis: bool = True
        self.in_tell_operation: bool = False
        
    def gv_as_sym(self):
        # Sometimes Macromedia Director creates symbols instead of
        # global variables. So we need to ensure that any parameter that
        # is a symbol makes sense in that position
        if self.parameters is not None:
            params: LoadListOperation = cast(LoadListOperation, self.parameters)
            operands = params.operands
            l: int = len(operands)
            if  l > 0:
                # The first parameter of a list function has to be a list
                idx = l - 1
                if (self.name.lower() in LIST_FUNCTIONS
                    and isinstance(operands[idx], Symbol)):
                    sym: Symbol = cast(Symbol, operands[idx])
                    operands[idx] = GlobalVariable(sym.name, sym.position)

    def generate_lingo(self, indentation: int) -> str: 
        self.gv_as_sym()     
        
        if (self.parameters is not None
            and len(cast(LoadListOperation, self.parameters).operands) > 0):
            
            params: LoadListOperation = cast(LoadListOperation, self.parameters)
            if 'sound' == self.name:
                sym: Node = params.operands.pop()
                return "sound %s %s"%(sym.name,
                                      params.generate_lingo(indentation))
            
            if self.use_parenthesis:
                return self.name + '('+params.generate_lingo(indentation)+')'
            else:    
                return self.name + ' ' + params.generate_lingo(indentation)
        else:
            return self.name

    def generate_js(self, indentation: int) -> str:
        self.gv_as_sym()

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
            nm = ''
            if not self.in_tell_operation:
                nm = '_movie.'
            if params_str.startswith('symbol(\''):
                p = params_str[len('symbol(\''):-2]
                nm = nm + 'go' + p.capitalize()
                params_str = ''
            else:
                nm = nm + 'go'
        
        if nm == 'cast':
            nm = 'member'
        
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
        super().__init__(name, position)
        self.object: Optional[Node] = None
        self.parameters: Optional[Node] = None

    def generate_lingo(self, indentation: int) -> str:
        obj: Node = cast(Node, self.object)
        params: Node = cast(Node, self.parameters)
        return "tell %s to %s(%s)"%(obj.generate_lingo(indentation),
                            self.name,
                            params.generate_lingo(indentation))

    def generate_js(self, indentation: int) -> str:
        obj: Node = cast(Node, self.object)
        params: Node = cast(Node, self.parameters)
        return "%s.%s(%s)"%(obj.generate_js(indentation),
                            self.name,
                            params.generate_js(indentation))
