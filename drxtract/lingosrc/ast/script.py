# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .function_op import FunctionDef
from typing import List

#
# Script class.
# 
class Script:
    """This class represents a whole Lingo script and it is the root of
    the AST"""
    
    def __init__(self):
        self.properties: List[str] = []
        self.global_vars: List[str] = []
        self.functions: List[FunctionDef] = []
