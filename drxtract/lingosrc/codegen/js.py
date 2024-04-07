# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Javascript code generation functions.
#

from ..ast import Script
from ..util import code_indentation, vsprintf
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
    if len(script.factory_name) > 0:
        return generate_factory_js_code(script)
    else:
        return generate_common_js_code(script)
    

# =============================================================================
def generate_factory_js_code(script: Script) -> str:
    """
    Generates javascript code from an AST for a Lingo Factory.
    
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
    
    code = 'class Factory__' + script.factory_name + ' extends FactoryBase {'
    
    for f in script.functions:
        code += "\n"
        
        code += code_indentation(1) + vsprintf("%s(", f.name)
        if len(f.parameters) > 0:
            params: List[str] = []
            for n in f.parameters:
                if n.name == 'me':
                    # Ignore 'me' parameter
                    continue
                params.append(n.name)
            
            code += vsprintf("%s", ', '.join(params))
        code += ") {\n"
        
        for lv in f.local_vars:
            code += code_indentation(2) + vsprintf("var %s;\n", lv.name)
            
        if len(f.local_vars) > 0:
            code = code + "\n"
        
        last = len(f.statements)-1
        if f.statements[last].code.name == 'exit':
            f.statements.pop()
        
        for st in f.statements:
            code = code + st.generate_js(2, True)
        
        code += code_indentation(1) + "}\n"
    
    code += "}\n\n"
    code += "function " + script.factory_name + "(methodName, ...args) {\n"
    code += code_indentation(1) + "return factoryCall('" \
        + script.factory_name + "', methodName, args);\n" 
    code += "}\n"
    
    return code
         


# =============================================================================
def generate_common_js_code(script: Script) -> str:
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
        
        code = code + vsprintf("function %s(", f.name)
        if len(f.parameters) > 0:
            params: List[str] = []
            for n in f.parameters:
                params.append(n.name)
            
            code = code + vsprintf("%s", ', '.join(params))
        code += ") {\n"
        
        for lv in f.local_vars:
            code = code + code_indentation(1) + vsprintf("var %s;\n", lv.name)
            
        if len(f.local_vars) > 0:
            code = code + "\n"
        
        last = len(f.statements)-1
        if f.statements[last].code.name == 'exit':
            f.statements.pop()
        
        for st in f.statements:
            code = code + st.generate_js(1, False)
        
        code += "}\n"
        first_function = False
    
    return code
         
