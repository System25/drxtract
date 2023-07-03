# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from typing import List, Dict

KNOWN_SYMBOLS: List[str] = [
    "loop", "next", "previous"
]

PREDEFINED_CONSTANTS: Dict[str, str] =  {
    '""': 'empty',
    '"\\x08"': 'backspace',
    '"\\x03"': 'enter',
    '"\""': 'quote',
    '"\\r"': 'return',
    '"\\t"': 'tab'
    
}

#
# Constant value class.
# 
class ConstantValue(Node):
    """This class represents a constant value in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

    def generate_lingo(self, indentation: int) -> str:
        if self.name in PREDEFINED_CONSTANTS.keys():
            return PREDEFINED_CONSTANTS[self.name]
        
        return self.name

#
# Symbol class.
# 
class Symbol(Node):
    """This class represents a symbol in the AST"""
    def __init__(self, name:str, position: int):
        Node.__init__(self, name, position)

    def generate_lingo(self, indentation: int) -> str:
        if self.name in KNOWN_SYMBOLS:
            return self.name
        
        return '#' + self.name

    def generate_js(self, indentation: int) -> str:      
        return 'symbol(\'' + self.name + '\')'