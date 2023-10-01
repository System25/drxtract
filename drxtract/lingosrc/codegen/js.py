# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Javascript code generation functions.
#

from ..ast import Script
from ..util import code_indentation
from typing import List

# =============================================================================
def generate_js_code(script: Script) -> str:
    """
    Generates javascript code from an AST.
    
    Parameters
    ----------
    script : Script
        Lingo script AST.
        
    Returns
    -------
    str
        The string that contains the code generated.
        
    """
    code: str = ''
    
    first_function: bool = True
    for f in script.functions:
        if not first_function:
            code += "\n"
        
        if f.name == 'new':
            f.name = 'birth'
        
        code = code + "function %s("%(f.name)
        if len(f.parameters) > 0:
            params: List[str] = []
            for n in f.parameters:
                params.append(n.name)
            
            code = code + "%s"%(', '.join(params))
        code += ") {\n"
        
        for lv in f.local_vars:
            code = code + code_indentation(1) + "var %s;\n"%(lv.name)
            
        if len(f.local_vars) > 0:
            code = code + "\n"
        
        last = len(f.statements)-1
        if f.statements[last].code.name == 'exit':
            del f.statements[last]
        
        for st in f.statements:
            code = code + st.generate_js(1)
        
        code += "}\n"
        first_function = False
    
    return code
         
