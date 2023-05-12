# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Abstract Opcode class.
# 
class Opcode:
  def __init__(self, opcode)):
		self.opcode = opcode
		self.nbytes = 1
		

  @abstractmethod
  def process(self, code, stack, statements_list):
    pass

#
# Abtract 2-bytes Opcode.
#
class BiOpcode:
  def __init__(self, opcode1, opcode2)):
    Opcode.__init__(self, opcode1)
    self.opcode2 = opcode2
    self.nbytes = 2

#
# Abtract 3-bytes Opcode.
#
class TriOpcode:
  def __init__(self, opcode1, opcode2, opcode3)):
    BiOpcode.__init__(self, opcode1, opcode2)
    self.opcode3 = opcode3
    self.nbytes = 3

#
# Abtract 1-byte param Opcode.
#
class Param1Opcode:
  def __init__(self, opcode)):
    Opcode.__init__(self, opcode)
    self.param1 = None
    self.nbytes = 2
    
#
# Abtract 2-bytes params Opcode.
#
class Param2Opcode:
  def __init__(self, opcode)):
    Opcode.__init__(self, opcode)
    self.param1 = None
    self.param2 = None
    self.nbytes = 3
