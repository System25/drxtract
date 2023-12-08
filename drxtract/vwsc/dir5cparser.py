# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .cparser import VwscChannelParser, DEBUG_SPRITE_INFO, \
    DEBUG_PALETTE_CHANNEL_INFO, DEBUG_MAIN_CHANNEL_INFO
import logging
import struct
from typing import Dict, Any


#
# Director 5 VWSC Channel parser class.
#
class D5VwscChannelParser(VwscChannelParser):  
    def __init__(self):
        super().__init__(24)
        
    def read_main_channel_info(self, frameData: bytes):
        """Main channel info"""
        indx = 0
        # Main channel info
        unknown01 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown01: %04x", unknown01)
    
        script = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("script: %04x", script)
    
        unknown03 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown03: %04x", unknown03)
    
        sound1_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("sound1_cast: %04x", sound1_cast)
    
        unknown05 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown05: %04x", unknown05)
    
        sound2_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("sound2_cast: %04x", sound2_cast)
            
        unknown07 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown07: %04x", unknown07)
    
        transition_cast_id = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("transition_cast_id: %d", transition_cast_id)
    
        unknown08 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown08: %04x", unknown08)
    
        unknown09 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown09: %04x", unknown09)
    
        fps = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("fps: %d", fps)
    
        unknown10 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown10: %04x", unknown10)
    
        main_data = {}
        if fps != 0 or sound1_cast != 0 or sound2_cast != 0 or script != 0:
            main_data['fps'] = fps
            main_data['transition_cast_id'] = transition_cast_id
            main_data['sound1_cast'] = sound1_cast
            main_data['sound2_cast'] = sound2_cast
            main_data['script'] = script
    
        return main_data


    # ==========================================================================
    # ==========================================================================
    # ==========================================================================
    def read_palette_channel_info(self, frameData: bytes):
        """Palette channel info"""
        indx = 0
        # Palette channel info
        unknown01 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown01: %04x", unknown01)
    
        palette_id = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        
        palette_name = self.get_palette_name(palette_id)
        
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("palette: %s", palette_name)
            
        fps = int(frameData[indx])
        indx += 1
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("fps: %d", fps)
    
        operation_code = int(frameData[indx])
        indx += 1
        
        operation: str = self.get_operation_name(operation_code)
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("operation: %s", operation)
    
        unknown02 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown02: %04x", unknown02)
    
        unknown03 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown03: %04x", unknown03)
            
        cycles = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("cycles: %d", cycles)
    
        
        palette_data: Dict[str, Any] = {}
        if palette_id != 0:
            palette_data['fps'] = fps
            palette_data['palette_id'] = palette_id
            palette_data['operation'] = operation
            palette_data['cycles'] = cycles
    
        return palette_data
    
    # ==========================================================================
    # ==========================================================================
    # ==========================================================================
    def read_sprite_channel_info(self, frameData: bytes, i: int):
        """ Sprite channel info"""
        indx = 0
        # Sprite info
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] ----------------------------", i)
        # Read sprite info
        unknown01 = int(frameData[indx])
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] unknown01: %d", i, unknown01)
    
        ink_type = int(frameData[indx])
        
        # The first two bits of ink_type is also a flag bit
        unknown_flag = ((ink_type >> 7) & 1)
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] unknown_flag: %d", i, unknown_flag)
    
        trails = ((ink_type >> 6) & 1)
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] trails: %d", i, trails)
    
        ink_type_name = self.get_ink_name(ink_type & 0x3F)
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] ink_type: %s (%s)", i, ink_type,
                          ink_type_name)
            
        spriteType = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        spriteTypeName = self.get_sprite_type(spriteType) 
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] spriteType: %s (%s)", i, spriteType,
                          spriteTypeName)
    
        castId = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] castId: %d", i, castId)
    
        unknown02 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] unknown02: %04x", i, unknown02)
    
        unknown03 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] unknown03: %04x", i, unknown03)
    
        foregroundColor = frameData[indx]
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] foregroundColor: %d", i, foregroundColor)
    
        backgroundColor = frameData[indx]
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] backgroundColor: %d", i, backgroundColor)
    
        y = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] y: %d", i, y)
    
        x = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] x: %d", i, x)
    
        height = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] height: %d", i, height)
    
        width = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] width: %d", i, width)
    
        flag2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        flag2 = (flag2 & 0xFFFF)
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] flag2: %04x", i, flag2)
            
        flag1 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        flag1 = (flag1 & 0xFFFF)
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] flag1: %04x", i, flag1)
    
        
        if castId > 0:
            sprite_data = {}
            sprite_data['spriteType'] = spriteType
            sprite_data['castId'] = castId
            sprite_data['foregroundColor'] = foregroundColor
            sprite_data['backgroundColor'] = backgroundColor
            sprite_data['ink_type'] = ink_type
            sprite_data['y'] = y
            sprite_data['x'] = x
            sprite_data['height'] = height
            sprite_data['width'] = width
            sprite_data['trails'] = trails
            sprite_data['moveable'] = (((flag2 >> 15) & 1) != 0)
            sprite_data['editable'] = (((flag2 >> 14) & 1) != 0)
            return sprite_data
        
        else:
            # Empty sprite
            if DEBUG_SPRITE_INFO:
                logging.debug("Empty castId (%d) in Sprite[%d]", castId, i)
            
            return {}
    
        return sprite_data
