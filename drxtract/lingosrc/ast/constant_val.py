# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from ..util import get_keys, replace
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

REPLACEMENT_CONSTANTS: Dict[str, str] =  {
    'BACKSPACE': "\\x08",
    'ENTER': "\\x03",
    'QUOTE': "\"",
    'RETURN': "\\r",
    'TAB': "\\t"
}

#
# Constant value class.
# 
class ConstantValue(Node):
    """This class represents a constant value in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def replace_chars_with_lingo_constants(self, n: str) -> str:
        for k in get_keys(REPLACEMENT_CONSTANTS):
            v: str = REPLACEMENT_CONSTANTS[k]
            idx = 1
            l: int = (len(n) - 1)
            pos: int = n.find(v, idx, l)
            while pos > 0:
                start = n[0:pos]
                e0: int = pos + len(v)
                el: int = len(n)
                end = n[e0:el]
    
                idx = len(start)
                if not start.endswith('& "'):
                    start = start + '" & '
                    idx = idx + 4
                else:
                    idx = idx - 1
                    start = start[0:idx]
    
                idx = idx + len(k)
                if end != '"':
                    end = ' & "' + end
                    idx = idx + 4
                else:
                    end = ''
    
                n = start + k + end
                    
                l = (len(n) -1)
                pos = n.find(v, idx, l)
        
        return n

    def generate_lingo(self, indentation: int) -> str:
        n: str = self.name
        if n in get_keys(PREDEFINED_CONSTANTS):
            return PREDEFINED_CONSTANTS[n]
    
        if (isinstance(n, str) and n.startswith('"')):
            n = self.replace_chars_with_lingo_constants(n)

        return n
        
    def generate_js(self, indentation: int, factory_method: bool) -> str:
        n: str = self.name
        if isinstance(n, str) and n.startswith('"'):
            l: int = len(n) - 1;
            n = n[1:l]
            return 'new LingoString("' + replace(n, '"', '\\"') + '")'
        
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
