# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .variable import PropertyName, Menu, MenuItem
from enum import Enum
from typing import Optional, cast, Dict

#
# Unary Operation names in Javascript.
# 
JS_UNA_OP: Dict[str,str] = {
    'minus': '-',
    'not': '!',
    'field': 'field',
    'hilite': 'hilite',
    'delete': 'delete',
    'last': 'last',
    'number': 'number',
}

#
# Binary Operation names in Lingo.
# 
LINGO_BIN_OP: Dict[str,str] = {
    'add': '+',
    'sub': '-',
    'mul': '*',
    'div': '/',
    'mod': 'mod',
    
    'concat': '&',
    'concats': '&&',
    'contains': 'contains',
    'start': 'start',
    
    'and': 'and',
    'or': 'or',
    
    'lt': '<',
    'lte': '<=',
    'gt': '>',
    'gte': '>=',
    'eq': '=',
    'ne': '<>',
    
    'intersects': 'intersects', 
    'within': 'within'
}

#
# Binary Operation names in Javascript.
# 
JS_BIN_OP: Dict[str,str] = {
    'add': '+',
    'sub': '-',
    'mul': '*',
    'div': '/',
    'mod': '%',
    
    'concat': '+',
    'concats': '+ " " +',
    'contains': '.includes',
    'start': '.startsWith',
    
    'and': '&&',
    'or': '||',
    
    'lt': '<',
    'lte': '<=',
    'gt': '>',
    'gte': '>=',
    'eq': '==',
    'ne': '!=',
    
    'intersects': '.intersects', 
    'within': '.within'
}



#
# Binary Operation names enumeration.
# 
class BinaryOperationNames(Enum):
    ASSIGN = 'assign'
    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
    MOD = 'mod'
    
    CONCAT = 'concat'
    CONCAT_SPACES = 'concats'
    CONTAINS = 'contains'
    START = 'start'
    
    AND = 'and'
    OR = 'or'
    
    LT = 'lt'
    LTE = 'lte'
    GT = 'gt'
    GTE = 'gte'
    EQ = 'eq'
    NE = 'ne'
    
    INTERSECTS = 'intersects'
    WITHIN = 'within'
  
  
  
#
# Unary Operation names enumeration.
# 
class UnaryOperationNames(Enum):
    MINUS = 'minus'
    NOT = 'not'
    FIELD = 'field'
    
    HILITE = 'hilite'
    DELETE = 'delete'
    LAST = 'last'
    NUMBER = 'number'
  

#
# String Operation names enumeration.
# 
class StringOperationNames(Enum):
    WORD = 'word'
    CHAR = 'char'
    ITEM = 'item'
    LINE = 'line'



#
# Unary Operation class.
# 
class UnaryOperation(Node):
    """This class represents an unary operation in the AST"""
    
    def __init__(self, name: UnaryOperationNames, position: int):
        Node.__init__(self, name.value, position)
        self.operand: Optional[Node] = None

    def generate_lingo(self, indentation: int) -> str:
        operand = cast(Node, self.operand)
        operation = self.name
        if operation == 'minus':
            operation = '-'
        else:
            operation = operation + ' '
        return "%s%s"%(operation, operand.generate_lingo(indentation))

    def generate_js(self, indentation: int) -> str:
        operand = cast(Node, self.operand)
        operation = JS_UNA_OP[self.name]
        return "%s(%s)"%(operation, operand.generate_js(indentation))

#
# Binary Operation class.
# 
class BinaryOperation(Node):
    """This class represents a binary operation in the AST"""
    
    def __init__(self, name: BinaryOperationNames, position: int):
        Node.__init__(self, name.value, position)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def generate_lingo(self, indentation: int) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        
        if self.name == 'assign':
            return "put %s into %s"%(r.generate_lingo(indentation),
                                     l.generate_lingo(indentation))            
        
        op = LINGO_BIN_OP[self.name]
        
        return "(%s %s %s)"%(l.generate_lingo(indentation), op,
                             r.generate_lingo(indentation))

    def generate_js(self, indentation: int) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        
        if self.name == 'assign':
            return "%s = %s"%(l.generate_js(indentation),
                              r.generate_js(indentation))            
        
        op: str = JS_BIN_OP[self.name]
        if op.startswith('.'):
            return "%s%s(%s)"%(l.generate_js(indentation), op,
                               r.generate_js(indentation))
        else:  
            return "(%s %s %s)"%(l.generate_js(indentation), op,
                                 r.generate_js(indentation))

#
# Special Assign Operation class.
# 
class SpAssignOperation(Node):
    """This class represents a special assign operation in the AST"""
    
    def __init__(self, name: BinaryOperationNames, position: int):
        Node.__init__(self, name.value, position)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.mode: Optional[str] = None
    
    def generate_lingo(self, indentation: int) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        return "put %s %s %s"%(l.generate_lingo(indentation),
                                self.mode,
                                r.generate_lingo(indentation))
    
    def generate_js(self, indentation: int) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        return "put_%s(%s, %s)"%(self.mode,
                                 l.generate_js(indentation),
                                 r.generate_js(indentation))
#
# String Operation class.
# 
class StringOperation(Node):
    """This class represents a string operation in the AST"""
    
    def __init__(self, name: StringOperationNames, position: int):
        Node.__init__(self, name.value, position)
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.of: Optional[Node] = None
    
#
# Unary String Operation class.
# 
class UnaryStringOperation(Node):
    """This class represents an unary string operation in the AST"""
    
    def __init__(self, name: UnaryOperationNames, position: int):
        Node.__init__(self, name.value, position)
        self.type: Optional[StringOperationNames] = None
        self.of: Optional[Node] = None
    
#
# Property accessor operation class.
# 
class PropertyAccessorOperation(Node):
    """This class represents a property access in the AST"""
    
    def __init__(self, obj: Node, name: str, position: int):
        Node.__init__(self, 'accessor', position)
        self.obj: Node = obj
        self.prop: str = name
        
    def generate_lingo(self, indentation: int) -> str:
        obj_str = self.obj.generate_lingo(indentation)
        if obj_str == 'me':
            return '%s'%(self.prop)
        else:
            return "the %s of %s"%(self.prop, obj_str)

    def generate_js(self, indentation: int) -> str: 
        return "%s.%s"%(self.obj.generate_js(indentation), self.prop)
    
#
# Menuitem accessor operation class.
# 
class MenuitemAccessorOperation(Node):
    """This class represents a menu item access in the AST"""
    
    def __init__(self, menu: Menu, item: MenuItem, position: int):
        Node.__init__(self, 'menu_item', position)
        self.menu: Menu = menu
        self.item: MenuItem = item
    
