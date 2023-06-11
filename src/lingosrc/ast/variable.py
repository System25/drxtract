# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node

    
#
# Local variable class.
# 
class LocalVariable(Node):
    """This class represents a local variable in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

#
# Global variable class.
# 
class GlobalVariable(Node):
    """This class represents a global variable in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def generate_js(self, indentation: int) -> str: 
        return "_global.%s"%(self.name)
#
# Property name class.
# 
class PropertyName(Node):
    """This class represents a property name in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
    
#
# Parameter name class.
# 
class ParameterName(Node):
    """This class represents a parameter name in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)


#
# Built-in date/time function class.
# 
class DateTimeFunction(Node):
    """This class represents a date/time function in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

#
# Menu class.
# 
class Menu(Node):
    """This class represents a menu in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)
    
#
# Menuitem class.
# 
class MenuItem(Node):
    """This class represents a menu item in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

    
#
# Sprite class.
# 
class Sprite(Node):
    """This class represents a sprite in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

#
# System object reference class.
# 
class SystemObject(Node):
    """This class represents a system object in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

#
# Cast element class.
# 
class Cast(Node):
    """This class represents a cast element in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

