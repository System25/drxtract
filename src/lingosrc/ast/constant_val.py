# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .node import Node

#
# Constant value class.
# 
class ConstantValue(Node):
    """This class represents a constant value in the AST"""
    
    def __init__(self, name: str, position: int):
        Node.__init__(self, name, position)

#
# Symbol class.
# 
class Symbol(Node):
    """This class represents a symbol in the AST"""
    def __init__(self, name:str, position: int):
        Node.__init__(self, name, position)

    def generate_lingo(self, indentation: int) -> str:
        return '#' + self.name

    def generate_js(self, indentation: int) -> str:
        return 'symbol("' + self.name + '")'
