# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from abc import ABCMeta, abstractmethod
from ..ast import Function, Node
from ..model.context import Context
from typing import List

#
# Abstract Opcode class.
# 
class Opcode:
    """This class represents a Lingo script opcode"""
    __metaclass__ = ABCMeta
    
    def __init__(self, opcode: int):
        self.opcode: int = opcode
        self.nbytes: int = 1

    @abstractmethod
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        pass

#
# Abtract 2-bytes Opcode.
#
class BiOpcode(Opcode):
    """This class represents a Lingo script 2-bytes opcode"""
    
    def __init__(self, opcode1: int, opcode2: int):
        Opcode.__init__(self, opcode1)
        self.opcode2: int = opcode2
        self.nbytes = 2

#
# Abtract 3-bytes Opcode.
#
class TriOpcode(BiOpcode):
    """This class represents a Lingo script 3-bytes opcode"""
    
    def __init__(self, opcode1: int, opcode2: int, opcode3: int):
        BiOpcode.__init__(self, opcode1, opcode2)
        self.opcode3: int = opcode3
        self.nbytes = 3

#
# Abtract 1-byte param Opcode.
#
class Param1Opcode(Opcode):
    """This class represents a Lingo script opcode with 1 byte param"""
    
    def __init__(self, opcode: int):
        Opcode.__init__(self, opcode)
        self.param1: int = 0
        self.nbytes = 2
    
#
# Abtract 2-bytes params Opcode.
#
class Param2Opcode(Opcode):
    """This class represents a Lingo script opcode with 2-bytes param"""
    
    def __init__(self, opcode: int):
        Opcode.__init__(self, opcode)
        self.param1: int = 0
        self.param2: int = 0
        self.nbytes = 3
