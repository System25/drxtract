# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
from .lnam import parse_lnam_file_data
from .lscr import parse_lrcr_file_data
from ..ast import Script


#
# Parse LNAM file
# 
# =============================================================================
def parse_lnam_file(lnam_file: str) -> List[str]:
    """
    Parse a LNAM file and return the list of names inside it.
    
    Parameters
    ----------
    lnam_file : str
        The path to the LNAM file to parse.
        
    Returns
    -------
    list
        a list of strings that contains variable names and method names.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """

    with open(lnam_file, mode='rb') as file:
        fdata: bytes = file.read()

        return parse_lnam_file_data(fdata)

#
# Parse LSCR file
# 
# =============================================================================
def parse_lrcr_file(lscr_file: str, name_list: List[str]) -> Script:
    """
    Parse a LSCR file and return the AST of the code inside it.
    
    Parameters
    ----------
    lscr_file: str
        The path to the LSCR file to parse.
    name_list: List[str]
        The list of variables names and function names.
        
    Returns
    -------
    script
        a script object with the Abstract-Syntax-Tree.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """

    with open(lscr_file, mode='rb') as file:
        fdata: bytes = file.read()

        return parse_lrcr_file_data(fdata, name_list)
