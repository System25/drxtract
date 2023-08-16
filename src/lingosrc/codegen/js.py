# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Javascript code generation functions.
#

from ..ast import Script
from ..util import code_indentation

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
            code = code + "%s"%(', '.join(n.name for n in f.parameters))
        code += ") {\n"
        
        for lv in f.local_vars:
            code = code + code_indentation(1) + "var %s;\n"%(lv.name)
            
        if len(f.local_vars) > 0:
            code = code + "\n"
        
        if f.statements[-1].code.name == 'exit':
            del f.statements[-1]
        
        for st in f.statements:
            code = code + st.generate_js(1)
        
        code += "}\n"
        first_function = False
    
    return code
         
