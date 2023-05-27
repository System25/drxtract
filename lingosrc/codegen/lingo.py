# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Lingo code generation functions.
#

from lingosrc.ast import Script
from lingosrc.util import code_indentation

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
        code = code + "property %s\n"%(', '.join(script.properties))
    
    for f in script.functions:
        code = code + "on %s"%(f.name)
        if len(f.parameters) > 0:
            code = " %s"%(', '.join(n.name for n in f.parameters))
        code += "\n"
        
        for gv in f.global_vars:
            code = code + code_indentation(1) + "global %s\n"%(gv.name)
            
        if len(f.global_vars) > 0:
            code = code + "\n"
        
        if f.statements[-1].code.name == 'exit':
            del f.statements[-1]
        
        for st in f.statements:
            code = code + st.generate_lingo(1)
        
        code += "\nend %s"%(f.name)
    
    return code
         
