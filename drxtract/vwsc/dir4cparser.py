# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .cparser import VwscChannelParser, DEBUG_SPRITE_INFO, \
    DEBUG_PALETTE_CHANNEL_INFO, DEBUG_MAIN_CHANNEL_INFO
from ..common import DIR4_PALETTE_NAMES
import logging
import struct
from typing import Dict, Any



#
# Director 4 VWSC Channel parser class.
#
class D4VwscChannelParser(VwscChannelParser):  
    def __init__(self):
        super().__init__(20)
        self.paletteNames: Dict[int, str] = DIR4_PALETTE_NAMES
        
    def read_main_channel_info(self, frameData: bytes):
        """Main channel info"""
        indx = 0
        # Main channel info
        flags = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("flags: %04x", flags)
    
        transition_duration = int(frameData[indx])
        
        # The first bit indicates if is stage area or changing area
        transition_in_changing_area = ((transition_duration >> 7) & 1)
        transition_duration = (transition_duration & 0x7F)
        indx += 1
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("transition_in_changing_area: %d",
                          transition_in_changing_area)
            logging.debug("transition_duration: %d", transition_duration)
        
        transition_chunk_size = int(frameData[indx])
        indx += 1
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("transition_chunk_size: %d", 
                          transition_chunk_size)
    
        fps = int(frameData[indx])
        indx += 1
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("Frames per second: %d", fps)
        
        transition_id = self.get_transition_name(int(frameData[indx]))
        indx += 1
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("transition_id: %s", transition_id)
    
        sound1_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("sound1_cast: %d", sound1_cast)
    
        sound2_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("sound2_cast: %d", sound2_cast)
    
        sound_flags = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("sound_flags: %04x", sound_flags)
        
        unknown1 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown1: %04x", unknown1)
    
        unknown2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown2: %04x", unknown2)
    
        script = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("script: %04x", script)
    
        unknown3 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("unknown3: %04x", unknown3)
    
        main_data: Dict[str, Any] = {}
        if fps != 0 or sound1_cast != 0 or sound2_cast != 0 or script != 0:
            main_data['fps'] = fps
            main_data['transition_id'] = transition_id
            main_data['sound1_cast'] = sound1_cast
            main_data['sound2_cast'] = sound2_cast
            main_data['script'] = script
            main_data['transition_chunk_size'] = transition_chunk_size
            main_data['transition_duration'] = transition_duration
    
        return main_data

    # ==========================================================================
    # ==========================================================================
    # ==========================================================================
    def read_palette_channel_info(self, frameData: bytes):
        """Palette channel info"""
        indx = 0
        # Palette channel info
        palette_id = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        
        palette_name = self.get_palette_name(palette_id)
        
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("palette: %s", palette_name)
    
        unknown2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown2: %04x", unknown2)
    
        operation_code = int(frameData[indx])
        indx += 1
        
        operation = self.get_operation_name(operation_code)
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("operation: %s", operation)
    
        fps = int(frameData[indx])
        indx += 1
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("fps: %d", fps)
    
        unknown4 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown4: %04x", unknown4)
    
        cycles = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("cycles: %d", cycles)
    
        unknown6 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown6: %04x", unknown6)
    
        unknown7 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown7: %04x", unknown7)
    
        unknown8 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown8: %04x", unknown8)
    
        unknown9 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("unknown9: %04x", unknown9)
            
        palette_data: Dict[str, Any] = {}
        if palette_id != 0:
            palette_data['fps'] = fps
            palette_data['operation'] = operation
            palette_data['palette_id'] = palette_id
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
        spriteType = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        spriteTypeName = self.get_sprite_type(spriteType)
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] spriteType: %s (%s)", i, spriteType,
                          spriteTypeName)
    
        foregroundColor = int(frameData[indx])
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] foregroundColor: %d", i, foregroundColor)
    
        backgroundColor = int(frameData[indx])
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] backgroundColor: %d", i, backgroundColor)
    
        flags = int(frameData[indx])
        indx += 1
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] flags: %x", i, flags)
    
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
    
        castId = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] castId: %d", i, castId)
    
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
    
        flag1 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        flag1 = (flag1 & 0xFFFF)
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] flag1: %04x", i, flag1)
        
        flag2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
        flag2 = (flag2 & 0xFFFF)
        indx = indx + 2
        if DEBUG_SPRITE_INFO:
            logging.debug("Sprite[%d] flag2: %04x", i, flag2)
        
        if castId > 0:
            sprite_data = {}
            sprite_data['spriteType'] = spriteType
            sprite_data['castId'] = castId
            sprite_data['foregroundColor'] = foregroundColor
            sprite_data['backgroundColor'] = backgroundColor
            sprite_data['ink_type'] = ink_type
            sprite_data['flags'] = flags
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
