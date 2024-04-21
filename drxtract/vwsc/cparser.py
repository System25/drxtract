# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from abc import ABCMeta, abstractmethod
import logging
from typing import Dict, Any
from ..lingosrc.util import get_keys
from ..common import DIR_INK_NAMES, DIR_PALETTE_NAMES, DIR_TRANSITION_NAMES, \
    DIR_SPRITE_TYPES

DEBUG_MAIN_CHANNEL_INFO: bool = False
DEBUG_PALETTE_CHANNEL_INFO: bool = False
DEBUG_SPRITE_INFO: bool = False

#
# Abstract VWSC Channel parser class.
# 
class VwscChannelParser:
    """This class represents a VWSC file parser"""
    __metaclass__ = ABCMeta
    
    def __init__(self, frame_size: int):
        self.frame_size: int = frame_size
        self.spriteTypes: Dict[int, str] = DIR_SPRITE_TYPES
        self.inkNames: Dict[int, str] = DIR_INK_NAMES
        self.transtionNames: Dict[int, str] = DIR_TRANSITION_NAMES
        self.paletteNames: Dict[int, str] = DIR_PALETTE_NAMES

    def can_parse(self, frame_size: int) -> bool:
        return self.frame_size == frame_size

    def get_operation_name(self, operation: int) -> str:
        operation = ((operation >> 4) & 0xF)
        bit3 = (operation & 0x8)
        bit2 = (operation & 0x4)
        bit1 = (operation & 0x2)
        bit0 = (operation & 0x1)
        
        if bit3 != 0:
            # Color Cycling
            if bit0 != 0:
                return 'color_cycling_auto_reverse'
            else:
                return 'color_cycling_loop'
        
        if bit2 != 0:
            # Fade to color
            if bit1 != 0:
                return 'fade_to_black'
            else:
                return 'fade_to_white'
        
        return str(operation)

    def get_sprite_type(self, value: int) -> str:
        if value in get_keys(self.spriteTypes):
            return self.spriteTypes[value]
        
        return str(value)

    def get_ink_name(self, value: int) -> str:
        if value in get_keys(self.inkNames):
            return self.inkNames[value]
        
        return str(value)

    def get_transition_name(self, value: int) -> str:
        if value in get_keys(self.transtionNames):
            return self.transtionNames[value]
        
        return str(value)
    
    def get_palette_name(self, value: int) -> str:
        if value in get_keys(self.paletteNames):
            return self.paletteNames[value]
        
        return str(value)

    """Reads from VWSC channel data the score elements"""
    def parse_vwsc_channels(self, channelData:bytes, column: int):
        cdata: Dict[str, Any] = {}
        indx = 0
        cdata['score'] = []
        
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("Director 4?")
            logging.debug("[%d] Main channel info --------------------", column)
        frameData = channelData[indx:(indx+self.frame_size)]
        cdata['main'] = self.read_main_channel_info(frameData)
        indx += self.frame_size
        
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("[%d] Palette channel info -----------------", column)
        frameData = channelData[indx:(indx+self.frame_size)]
        cdata['palette'] =  self.read_palette_channel_info(frameData)
        indx += self.frame_size
        
        i = 1
        while indx < len(channelData):
            if DEBUG_SPRITE_INFO:
                logging.debug("[%d] Sprite channel info --------------", column)

            frameData = channelData[indx:(indx+self.frame_size)]
            cdata['score'].append(self.read_sprite_channel_info(frameData, i))
    
            indx += self.frame_size
            
            i += 1
            
        
        return cdata

    @abstractmethod
    def read_main_channel_info(self, frameData: bytes):
        pass

    @abstractmethod
    def read_palette_channel_info(self, frameData: bytes):
        pass
    
    @abstractmethod
    def read_sprite_channel_info(self, frameData: bytes, i: int):
        pass
    
__all__ = ['DEBUG_SPRITE_INFO', 'DEBUG_PALETTE_CHANNEL_INFO',
           'DEBUG_MAIN_CHANNEL_INFO']
