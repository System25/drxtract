# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Node class.
# 
class Node:
    """This class represents a node value in the AST"""
    
    def __init__(self, name: str, position: int):
        self.name: str = name
        self.position: int = position

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.position == other.position
        return False

    def generate_lingo(self, indentation: int) -> str: 
        return self.name

    def generate_js(self, indentation: int) -> str: 
        return self.name
