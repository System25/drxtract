# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node
from ..util import get_keys, is_same_class, vsprintf
from typing import List

KNOWN_SYMBOLS: List[str] = [
    "ancestor"
]

KNOWN_PROPERTIES = {
    'actorList': '_movie',
    'ancestor': 'me',
    'floatPrecision': '_system',
    'mouseDownScript': '_system',
    'mouseUpScript': '_system',
    'keyDownScript': '_system',
    'keyUpScript': '_system',
    'timeoutScript': '_system',
    'itemDelimiter': '_player'
}

#
# Local variable class.
# 
class LocalVariable(Node):
    """This class represents a local variable in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

#
# Global variable class.
# 
class GlobalVariable(Node):
    """This class represents a global variable in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def __eq__(self, other):
        if is_same_class(other, self):
            return self.name == other.name
        return False

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("_global.%s", self.name)
#
# Property name class.
# 
class PropertyName(Node):
    """This class represents a property name in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
 

    def generate_lingo(self, indentation: int) -> str: 
        if self.name in KNOWN_SYMBOLS or isinstance(self, DefinedPropertyName):
            return self.name
        else:
            return vsprintf("the %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        obj_name: str = 'me'
        if factory_method:
            obj_name = 'this'
        
        propName = self.name
        if self.name in get_keys(KNOWN_PROPERTIES):
            obj_name = KNOWN_PROPERTIES[propName]
        return vsprintf("%s.%s", obj_name, propName)

#
# Defined Property name class.
# 
class DefinedPropertyName(PropertyName):
    """This class represents a property name in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

#
# Parameter name class.
# 
class ParameterName(Node):
    """This class represents a parameter name in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)


#
# Built-in date/time function class.
# 
class DateTimeFunction(Node):
    """This class represents a date/time function in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def generate_lingo(self, indentation: int) -> str: 
        return vsprintf("the %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("_system.date('%s')", self.name)

#
# Menu class.
# 
class Menu(Node):
    """This class represents a menu in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)
    
    def generate_lingo(self, indentation: int) -> str: 
        return vsprintf("menu %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("_menuBar.menu[%s]", self.name)
    
#
# Menuitem class.
# 
class MenuItem(Node):
    """This class represents a menu item in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def generate_lingo(self, indentation: int) -> str: 
        return vsprintf("menuItem %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("item[%s]", self.name)    

#
# SoundChannel class.
# 
class SoundChannel(Node):
    """This class represents a sound channel in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def generate_lingo(self, indentation: int) -> str: 
        return vsprintf("sound %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("sound(%s)", self.name)

#
# Sprite class.
# 
class Sprite(Node):
    """This class represents a sprite in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def generate_lingo(self, indentation: int) -> str: 
        return vsprintf("sprite %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("sprite(%s)", self.name)


#
# System object reference class.
# 
class SystemObject(Node):
    """This class represents a system object in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

#
# Cast element class.
# 
class Cast(Node):
    """This class represents a cast element in the AST"""
    
    def __init__(self, name: str, position: int):
        super().__init__(name, position)

    def generate_lingo(self, indentation: int) -> str: 
        return vsprintf("cast %s", self.name)

    def generate_js(self, indentation: int, factory_method: bool) -> str: 
        return vsprintf("member(%s)", self.name)
