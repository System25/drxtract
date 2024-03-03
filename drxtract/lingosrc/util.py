# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

import struct
from typing import Dict, KeysView, Any

#
# Utility functions.
# 

# =============================================================================
def vsprintf(fmt: str, *args) -> str:
    """
    Retuns a C-style vsprintf formatted string.
    
    Parameters
    ----------
    fmt : String format.
    args : parameters.
            
    Returns
    -------
    str Formatted string.
        
    """
    return fmt%(args)

# =============================================================================
def is_same_class(o1: Any, o2: Any) -> bool:
    """
    Retuns true if both objects share the same class.
    
    Parameters
    ----------
    o1 : any object.
    o2 : any object.
            
    Returns
    -------
    bool True if both objects share the same class.
        
    """
    return isinstance(o1, o2.__class__)

# =============================================================================
def get_class_name(o: Any) -> str:
    """
    Retuns the name of the class of the object.
    
    Parameters
    ----------
    o : any object.
            
    Returns
    -------
    str Objects class name.
        
    """
    return o.__class__.__name__

# =============================================================================
def get_keys(d: Dict) -> KeysView:
    """
    Retuns the keys of a dictionary.
    
    Parameters
    ----------
    d : dictionary.
            
    Returns
    -------
    KeysView The list of keys.
        
    """
    return d.keys()

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

# =============================================================================
def repeat_string(word:str, n:int) -> str:
    """
    Returns a string with the word repeated N times.
    
    Parameters
    ----------
    word : str
        The word to repeat.
    n: int
        The number of times that the word will be repeated.
        
    Returns
    -------
    str
        The word repeated N times.
        
    """

    return word * n

# =============================================================================
class Dictionary(dict):
    """This class is a wrapper for dict"""
    
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
