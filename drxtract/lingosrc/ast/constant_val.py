# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from ..util import get_keys
from typing import List, Dict

KNOWN_SYMBOLS: List[str] = [
    "loop", "next", "previous", "playFile", "fadeIn", "fadeOut", "stop", "close"
]

PREDEFINED_CONSTANTS: Dict[str, str] =  {
    '""': 'EMPTY',
    '"\\x08"': 'BACKSPACE',
    '"\\x03"': 'ENTER',
    '"\""': 'QUOTE',
    '"\\r"': 'RETURN',
    '"\\t"': 'TAB'
    
}

#
# Constant value class.
# 
class ConstantValue(Node):
    """This class represents a constant value in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def generate_lingo(self, indentation: int) -> str:
        n: str = self.name
        if n in get_keys(PREDEFINED_CONSTANTS):
            return PREDEFINED_CONSTANTS[n]
        
        return n
    
    def generate_js(self, indentation: int, factory_method: bool) -> str:
        n: str = self.name
        if isinstance(n, str) and n.startswith('"'):
            return "new LingoString(" + n + ")"
        
        return n

#
# Symbol class.
# 
class Symbol(Node):
    """This class represents a symbol in the AST"""
    def __init__(self, name:str, position: int):
        super().__init__(name, position)
        self.use_hash = True

    def generate_lingo(self, indentation: int) -> str:
        if self.name in KNOWN_SYMBOLS:
            self.use_hash = False
        
        if self.use_hash:
            return '#' + self.name
        return self.name

    def generate_js(self, indentation: int, factory_method: bool) -> str:
        return 'symbol(\'' + self.name + '\')'
