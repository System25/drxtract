# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Lingo code generation functions.
#

from ..ast import Script
from ..util import code_indentation, vsprintf
from typing import List
from builtins import sorted

# =============================================================================
def generate_lingo_code(script: Script) -> str:
    """
    Generates lingo code from an AST.
    
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
    if len(script.properties) > 0:
        code = code + vsprintf("property %s\n", ', '.join(script.properties))
        
    if len(script.global_vars) > 0:
        for gvh in script.global_vars:
            code = code + vsprintf("global %s\n", gvh)
        code = code + "\n"
    
    first_function: bool = True
    for f in script.functions:
        if not first_function:
            code += "\n"
        
        code = code + vsprintf("on %s", f.name)
        if len(f.parameters) > 0:
            params: List[str] = []
            for n in f.parameters:
                params.append(n.name)
            
            code = code + vsprintf(" %s", ', '.join(params))
        code += "\n"
        
        f.global_vars = sorted(f.global_vars, key = lambda x: x.name)
        gv_count: int = 0
        for gv in f.global_vars:
            if gv.name not in script.global_vars:
                code = code + code_indentation(1) + vsprintf("global %s\n",
                                                             gv.name)
                gv_count = gv_count + 1
            
        if gv_count > 0:
            code = code + "\n"
        
        last = len(f.statements)-1
        if f.statements[last].code.name == 'exit':
            f.statements.pop()
        
        for st in f.statements:
            code = code + st.generate_lingo(1)
        
        code += "end\n"
        first_function = False
    
    return code
         
