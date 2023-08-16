# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

import struct

#
# Utility functions.
# 

# =============================================================================
def code_indentation(indentation:int) -> str:
    """
    Retuns the string to append to indent the code.
    
    Parameters
    ----------
    indentation : int
        indentation level.
        
    Returns
    -------
    str
        The string to append to indent the code.
        
    """
    return '    ' * indentation

# =============================================================================
def unpack_float80(b: bytes) -> str:
    """
    Unpacks a 80 bytes float.
    
    Parameters
    ----------
    b : bytes
        Bytes containing the 80 bytes float number.
        
    Returns
    -------
    str
        The string that represents the float number.
        
    """
    e = struct.unpack(">H", b[0:2])[0] 
    q = struct.unpack(">Q", b[2:10])[0]
    m = (q*2.0)/(1<<64)
    
    value = '%s'%(m*pow(2, e - 16383))
    
    return value

# =============================================================================
def escape_string(strval: str) -> str:
    """
    Returns a string with escaped characters.
    
    Parameters
    ----------
    strval : str
        The string to escape.
        
    Returns
    -------
    str
        The escaped string.
        
    """

    return '"' + strval.encode("unicode_escape").decode('ascii') + '"'
