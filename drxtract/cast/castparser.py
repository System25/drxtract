# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from abc import ABCMeta, abstractmethod
from typing import Dict, Any


# -- Casting data types --
DIR_IMAGE_TYPE = 1
DIR_TEXT_INPUT_TYPE = 3
DIR_CLUT_TYPE = 4
DIR_SND_TYPE = 6
DIR_PUSH_BUTTON_TYPE = 7
DIR_SHAPE_TYPE = 8
DIR_LSCR_TYPE = 11
DIR_TEXT_TYPE = 12
DIR_TRAN_TYPE = 14

#
# Abstract Cast element data parser class.
# 
class CastParser:
    """This class represents a Cast header file parser"""
    __metaclass__ = ABCMeta
    
    def __init__(self, dataType: int):
        self.dataType: int = dataType
        
    @abstractmethod
    def parse(self, header_data: bytes,
              basic_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

__all__ = ['DIR_IMAGE_TYPE', 'DIR_TEXT_INPUT_TYPE', 'DIR_CLUT_TYPE',
           'DIR_SND_TYPE', 'DIR_PUSH_BUTTON_TYPE', 'DIR_SHAPE_TYPE',
           'DIR_LSCR_TYPE', 'DIR_TEXT_TYPE', 'DIR_TRAN_TYPE']
