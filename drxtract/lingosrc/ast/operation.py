# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from .variable import Menu, MenuItem
from enum import Enum
from typing import Optional, cast, Dict
from ..util import vsprintf
import re

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
    'number': 'length',
    'name': 'name'
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
    
    'intersects': 'sprite... intersects', 
    'within': 'sprite... within'
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
    NAME = 'name'
  

#
# String Operation names enumeration.
# 
class StringOperationNames(Enum):
    UNKNOWN = 'UNKNOWN'
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
        super().__init__(name.value, position)
        self.operand: Optional[Node] = None

    def generate_lingo(self, indentation: int) -> str:
        operand = cast(Node, self.operand)
        operation = self.name
        if operation == 'minus':
            operation = '-'
        else:
            operation = operation + ' '
        return vsprintf("%s%s", operation, operand.generate_lingo(indentation))

    def generate_js(self, indentation: int, factory_method: bool) -> str:
        operand = cast(Node, self.operand)
        operation = self.name
        operation = JS_UNA_OP[operation]
        return vsprintf("%s(%s)", operation,
                        operand.generate_js(indentation, factory_method))

#
# Binary Operation class.
# 
class BinaryOperation(Node):
    """This class represents a binary operation in the AST"""
    
    def __init__(self, name: BinaryOperationNames, position: int):
        super().__init__(name.value, position)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def generate_lingo(self, indentation: int) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        
        operation = self.name
        if operation == 'assign':
            left: str = l.generate_lingo(indentation)
            right: str = r.generate_lingo(indentation)
            if left.startswith('field(') and left.endswith(')'):
                return vsprintf("put %s into %s", right, left)       
            else:
                return vsprintf("set %s = %s", left, right)
        
        op:str = LINGO_BIN_OP[operation]
        if op.startswith('sprite... '):
            return vsprintf("sprite %s %s %s", l.generate_lingo(indentation),
                                      op.removeprefix('sprite... '),
                                      r.generate_lingo(indentation))
                
        return vsprintf("(%s %s %s)", l.generate_lingo(indentation), op,
                             r.generate_lingo(indentation))

    def generate_js(self, indentation: int, factory_method: bool) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        
        operation = self.name
        if operation == 'assign':
            return vsprintf("%s = %s",
                              l.generate_js(indentation, factory_method),
                              r.generate_js(indentation, factory_method))            
        
        op: str = JS_BIN_OP[operation]
        if op.startswith('.'):
            return vsprintf("sprite(%s)%s(sprite(%s))",
                            l.generate_js(indentation, factory_method), op,
                            r.generate_js(indentation, factory_method))
        else:  
            return vsprintf("(%s %s %s)",
                                 l.generate_js(indentation, factory_method), op,
                                 r.generate_js(indentation, factory_method))

#
# Special Assign Operation class.
# 
class SpAssignOperation(Node):
    """This class represents a special assign operation in the AST"""
    
    def __init__(self, name: BinaryOperationNames, position: int):
        super().__init__(name.value, position)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.mode: Optional[str] = None
    
    def generate_lingo(self, indentation: int) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        return vsprintf("put %s %s %s", r.generate_lingo(indentation),
                                self.mode,
                                l.generate_lingo(indentation))
    
    def generate_js(self, indentation: int, factory_method: bool) -> str:
        l = cast(Node, self.left)
        r = cast(Node, self.right)
        left: str = l.generate_js(indentation, factory_method);
        if left.startswith('field(') and left.endswith(')'):
            left = re.sub('(field\\([^\\)]+\\))', '\\1.text', left)
        
        if self.mode == 'after':
            return vsprintf("%s = %s + %s", left, left,
                            r.generate_js(indentation, factory_method))
        elif self.mode == 'before':
            return vsprintf("%s = %s + %s", left,
                            r.generate_js(indentation, factory_method),
                            left)
        else:
            return vsprintf("%s = %s", left,
                            r.generate_js(indentation, factory_method))
#
# String Operation class.
# 
class StringOperation(Node):
    """This class represents a string operation in the AST"""
    
    def __init__(self, name: StringOperationNames, position: int):
        super().__init__(name.value, position)
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.of: Optional[Node] = None
    
    def generate_lingo(self, indentation: int) -> str:
        if self.end is None:
            return vsprintf('%s %s of %s', self.name,
                                  cast(Node, self.start).generate_lingo(0),
                                  cast(Node, self.of).generate_lingo(0))
            
        return vsprintf('%s %s to %s of %s', self.name,
                      cast(Node, self.start).generate_lingo(0),
                      cast(Node, self.end).generate_lingo(0),
                      cast(Node, self.of).generate_lingo(0))
    
    def generate_js(self, indentation: int, factory_method: bool) -> str:
        if self.end is None:
            return vsprintf('%s.getPropRef("%s", %s)',
                cast(Node, self.of).generate_js(0, factory_method),
                self.name,
                cast(Node, self.start).generate_js(0, factory_method))
            
        return vsprintf('%s.getPropRef("%s", %s, %s)',
            cast(Node, self.of).generate_js(0, factory_method),
            self.name,
            cast(Node, self.start).generate_js(0, factory_method),
            cast(Node, self.end).generate_js(0, factory_method))
#
# Unary String Operation class.
# 
class UnaryStringOperation(Node):
    """This class represents an unary string operation in the AST"""
    
    def __init__(self, name: UnaryOperationNames, position: int):
        super().__init__(name.value, position)
        self.type: Optional[StringOperationNames] = None
        self.of: Optional[Node] = None

    def generate_lingo(self, indentation: int) -> str:
        operand = cast(Node, self.of)
        if self.type is not None:
            op_type = cast(StringOperationNames, self.type).value
            if self.name == UnaryOperationNames.LAST.value:
                return vsprintf("the %s %s of %s", self.name, op_type,
                                         operand.generate_lingo(indentation))
            else:
                return vsprintf("the %s of %ss of %s", self.name, op_type,
                                         operand.generate_lingo(indentation))
        
        return vsprintf("the %s of %s", self.name,
                        operand.generate_lingo(indentation))

    def generate_js(self, indentation: int, factory_method: bool) -> str:
        operand = cast(Node, self.of)
        operation = self.name
        operation = JS_UNA_OP[operation]
        if self.type is not None:
            op_type = cast(StringOperationNames, self.type).value
            if self.name == UnaryOperationNames.LAST.value:
                return vsprintf("%s.getProp(\"%s\", \"%s\")",
                            operand.generate_js(indentation, factory_method),
                            op_type, operation)
            else:
                return vsprintf("%s.%s.%s",
                               operand.generate_js(indentation, factory_method),
                               op_type,
                               operation)
        
        if operand.name == 'menus':
            operand.name = '_menuBar.menu'
        
        return vsprintf("%s.%s",
                operand.generate_js(indentation, factory_method), operation)
#
# Property accessor operation class.
# 
class PropertyAccessorOperation(Node):
    """This class represents a property access in the AST"""
    
    def __init__(self, obj: Node, name: str, position: int):
        super().__init__('accessor', position)
        self.obj: Node = obj
        self.prop: str = name
        
    def generate_lingo(self, indentation: int) -> str:
        obj_str = self.obj.generate_lingo(indentation)
        if obj_str == 'me':
            return vsprintf('%s', self.prop)
        elif obj_str.startswith('_') or obj_str == 'tell_obj':
            return vsprintf('the %s', self.prop)
        else:
            return vsprintf("the %s of %s", self.prop, obj_str)

    def generate_js(self, indentation: int, factory_method: bool) -> str:
        obj_str = self.obj.generate_js(indentation, factory_method)
        if obj_str == 'tell_obj':
            return vsprintf('%s', self.prop)
        else:
            return vsprintf("%s.%s",
                            self.obj.generate_js(indentation, factory_method),
                            self.prop)

#
# Key property accessor operation class.
# 
class KeyPropertyAccessorOperation(Node):
    """This class represents a _key property access in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__('accessor', position)
        self.prop: str = name
        
    def generate_lingo(self, indentation: int) -> str:
        return vsprintf("the %s", self.prop)

    def generate_js(self, indentation: int, factory_method: bool) -> str:
        if self.prop in ('date', 'time'):
            return vsprintf("_system.date('%s')", self.prop)
        
        return vsprintf("_key.%s", self.prop)
    
#
# Menuitem accessor operation class.
# 
class MenuitemAccessorOperation(Node):
    """This class represents a menu item access in the AST"""
    
    def __init__(self, menu: Menu, item: MenuItem, position: int):
        super().__init__('menu_item', position)
        self.menu: Menu = menu
        self.item: MenuItem = item
        
    def generate_lingo(self, indentation: int) -> str:
        return vsprintf("%s of %s", self.item.generate_lingo(0),
                           self.menu.generate_lingo(0))

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("%s.%s", self.menu.generate_js(0, factory_method),
                        self.item.generate_js(0, factory_method))
    
#
# Menuitems accessor operation class.
# 
class MenuitemsAccessorOperation(Node):
    """This class represents a menu items access in the AST"""
    
    def __init__(self, menu: Menu, position: int):
        super().__init__('menu_items', position)
        self.menu: Menu = menu

    def generate_lingo(self, indentation: int) -> str:
        return vsprintf("menuItems of %s", self.menu.generate_lingo(0))

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("%s.item", self.menu.generate_js(0, factory_method))
    