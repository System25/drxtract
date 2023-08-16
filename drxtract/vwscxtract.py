#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director VWSC files.
# VWLB files contains the score.
# 

import sys
import os
import struct
import logging
import json
import math

BINDIR = 'bin'

DEBUG_MAIN_CHANNEL_INFO = False
DEBUG_PALETTE_CHANNEL_INFO = False
DEBUG_SPRITE_INFO = True

#logging.basicConfig(level=logging.DEBUG)

# ==============================================================================
# Translate operation to string representation (Director 5)
def get_operation_dir5(operation):
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
    
    return operation


# ====================================================================================================================================
# Translate sprite type to string representation (Director 4)
def get_sprite_type_dir4(sprite_type):
    # I got this from D4Player project
    if sprite_type == 0:
        return 'empty'
    elif sprite_type == 1:
        return 'image'
    elif sprite_type == 2:
        return 'rectangle'
    elif sprite_type == 3:
        return 'round_rectangle'
    elif sprite_type == 4:
        return 'ellipse'
    elif sprite_type == 5:
        return 'line_lt_br'
    elif sprite_type == 6:
        return 'line_bl_tr'
    elif sprite_type == 7:
        return 'text'
    elif sprite_type == 8:
        return 'button'
    elif sprite_type == 9:
        return 'checkbox'
    elif sprite_type == 10:
        return 'radio_button'
    elif sprite_type == 16:
        return 'shape'
    
    return sprite_type


# ====================================================================================================================================
# Translate ink number to string representation (Director 5)
def get_ink(ink_type):
    
    # I found this online:
    # http://users.design.ucla.edu/~cariesta/MayaCourseNotes/html/body_director_basic.html
    
    if ink_type == 0:
        return 'copy'
    elif ink_type == 1:
        return 'transparent'
    elif ink_type == 2:
        return 'reverse'
    elif ink_type == 3:
        return 'ghost'
    elif ink_type == 4:
        return 'not copy'
    elif ink_type == 5:
        return 'not transparent'
    elif ink_type == 6:
        return 'not reverse'
    elif ink_type == 7:
        return 'not ghost'
    elif ink_type == 8:
        return 'matte'
    elif ink_type == 9:
        return 'mask'
    elif ink_type == 32:
        return 'blend'
    elif ink_type == 33:
        return 'add pin'
    elif ink_type == 34:
        return 'add'
    elif ink_type == 35:
        return 'subtract pin'
    elif ink_type == 36:
        return 'background transparent'
    elif ink_type == 37:
        return 'lightest'
    elif ink_type == 38:
        return 'subtract'
    elif ink_type == 39:
        return 'darkest'
    elif ink_type == 40:
        return 'lighten'
    elif ink_type == 41:
        return 'darken'
    
    # Unknown id
    return ink_type

# ====================================================================================================================================
# Translate a transition number to string representation (Director 4)
def get_transtition_dir4(transition_id):
    
    # I found this in: Director 8 Demystified (puppetTransition lingo script reference)
    
    if transition_id == 1:
        return 'wipe right'
    elif transition_id == 2:
        return 'wipe left'
    elif transition_id == 3:
        return 'wipe down'
    elif transition_id == 4:
        return 'wipe up'
    elif transition_id == 5:
        return 'center out, horizontal'
    elif transition_id == 6:
        return 'edges in, horizontal'
    elif transition_id == 7:
        return 'center out, vertical'
    elif transition_id == 8:
        return 'edges in, vertical'
    elif transition_id == 9:
        return 'center out, square'
    elif transition_id == 10:
        return 'edges in, square'
    elif transition_id == 11:
        return 'push left'
    elif transition_id == 12:
        return 'push right'
    elif transition_id == 13:
        return 'push down'
    elif transition_id == 14:
        return 'push up'
    elif transition_id == 15:
        return 'reveal up'
    elif transition_id == 16:
        return 'reveal up, right'
    elif transition_id == 17:
        return 'reveal right'
    elif transition_id == 18:
        return 'reveal down, right'
    elif transition_id == 19:
        return 'reveal down'
    elif transition_id == 20:
        return 'reveal down, left'
    elif transition_id == 21:
        return 'reveal left'
    elif transition_id == 22:
        return 'reveal up, left'
    elif transition_id == 23:
        return 'dissolve, pixels fast'
    elif transition_id == 24:
        return 'dissolve, boxy rectangles'
    elif transition_id == 25:
        return 'dissolve, boxy squares'
    elif transition_id == 26:
        return 'dissolve, patterns'
    elif transition_id == 27:
        return 'random rows'
    elif transition_id == 28:
        return 'random columns'
    elif transition_id == 29:
        return 'cover down'
    elif transition_id == 30:
        return 'cover down, left'
    elif transition_id == 31:
        return 'cover down, right'
    elif transition_id == 32:
        return 'cover left'
    elif transition_id == 33:
        return 'cover right'
    elif transition_id == 34:
        return 'cover up'
    elif transition_id == 35:
        return 'cover up, left'
    elif transition_id == 36:
        return 'cover up, right'
    elif transition_id == 37:
        return 'venetian blinds'
    elif transition_id == 38:
        return 'checkerboard'
    elif transition_id == 39:
        return 'strips on bottom, build left'
    elif transition_id == 40:
        return 'strips on bottom, build right'
    elif transition_id == 41:
        return 'strips on left, build down'
    elif transition_id == 42:
        return 'strips on left, build up'
    elif transition_id == 43:
        return 'strips on right, build down'
    elif transition_id == 44:
        return 'strips on right, build up'
    elif transition_id == 45:
        return 'strips on top, build left'
    elif transition_id == 46:
        return 'strips on top, build right'
    elif transition_id == 47:
        return 'zoom open'
    elif transition_id == 48:
        return 'zoom close'
    elif transition_id == 49:
        return 'vertical blinds'
    elif transition_id == 50:
        return 'dissolve, bits fast'
    elif transition_id == 51:
        return 'dissolve, pixels'
    elif transition_id == 52:
        return 'dissolve, bits'

    # Unknown id
    return transition_id


# ====================================================================================================================================
# Translate palette number to string representation (Director 5)
def get_palette_dir5(palette_id):
    
    # I found this in a german book called "Macromedia Director: Multimediaprogrammierung mit Lingo"
    # https://books.google.es/books?id=UxLuBQAAQBAJ&pg=PA282&lpg=PA282&dq=macromedia+director+ntsc+web+grayscale+rainbow&source=bl&ots=tlcNQFqWod&sig=ACfU3U2d0o3Kv3y7_9umDgOCPGBDqooIzQ&hl=es&sa=X&ved=2ahUKEwjXs-rnlNXiAhVDrxoKHdcACWIQ6AEwB3oECAUQAQ#v=onepage&q=macromedia%20director%20ntsc%20web%20grayscale%20rainbow&f=false
    
    if palette_id == -1:
        return 'systemMac'
    elif palette_id == -102:
        return 'systemWin'
    elif palette_id == -2:
        return 'rainbow'
    elif palette_id == -3:
        return 'grayscale'
    elif palette_id == -4:
        return 'pastels'
    elif palette_id == -5:
        return 'vivid'
    elif palette_id == -6:
        return 'ntsc'
    elif palette_id == -7:
        return 'metallic'
    elif palette_id == -8:
        return 'web216'
    elif palette_id == -101:
        return 'systemWinDir4'
    
    # Unknown id
    return palette_id


# ====================================================================================================================================
# Translate palette number to string representation (Director 4)
def get_palette_dir4(palette_id):
    if palette_id == -1:
        return 'systemMac'
    elif palette_id == -65:
        return 'systemWin'
    elif palette_id == -2:
        return 'rainbow'
    elif palette_id == -3:
        return 'grayscale'
    elif palette_id == -4:
        return 'pastels'
    elif palette_id == -5:
        return 'vivid'
    elif palette_id == -6:
        return 'ntsc'
    elif palette_id == -7:
        return 'metallic'
    elif palette_id == -8:
        return 'web216'

    
    # Unknown id
    return palette_id


# ====================================================================================================================================
# Main channel info (Director 4) 
def read_main_channel_info_v4(frameData):
    indx = 0
    # Main channel info
    flags = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("flags: %04x"%(flags))

    transition_duration = int(frameData[indx])
    
    # The first bit indicates if is stage area or changing area
    transition_in_changing_area = ((transition_duration >> 7) & 1)
    transition_duration = (transition_duration & 0x7F)
    indx += 1
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("transition_in_changing_area: %d"%(transition_in_changing_area))
        logging.debug("transition_duration: %d"%(transition_duration))
    
    transition_chunk_size = int(frameData[indx])
    indx += 1
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("transition_chunk_size: %d"%(transition_chunk_size))

    fps = int(frameData[indx])
    indx += 1
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("Frames per second: %d"%(fps))
    
    transition_id = get_transtition_dir4(int(frameData[indx]))
    indx += 1
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("transition_id: %s"%(transition_id))

    sound1_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("sound1_cast: %d"%(sound1_cast))

    sound2_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("sound2_cast: %d"%(sound2_cast))

    sound_flags = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("sound_flags: %04x"%(sound_flags))
    
    unknown1 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown1: %04x"%(unknown1))

    unknown2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown2: %04x"%(unknown2))

    script = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("script: %04x"%(script))

    unknown3 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown3: %04x"%(unknown3))

    main_data = {}
    if fps != 0 or sound1_cast != 0 or sound2_cast != 0 or script != 0:
        main_data['fps'] = fps
        main_data['transition_id'] = transition_id
        main_data['sound1_cast'] = sound1_cast
        main_data['sound2_cast'] = sound2_cast
        main_data['script'] = script
        main_data['transition_chunk_size'] = transition_chunk_size
        main_data['transition_duration'] = transition_duration

    return main_data


# ====================================================================================================================================
# Main channel info (Director 5) 
def read_main_channel_info_v5(frameData):
    indx = 0
    # Main channel info
    unknown01 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown01: %04x"%(unknown01))

    script = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("script: %04x"%(script))

    unknown03 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown03: %04x"%(unknown03))

    sound1_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("sound1_cast: %04x"%(sound1_cast))

    unknown05 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown05: %04x"%(unknown05))

    sound2_cast = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("sound2_cast: %04x"%(sound2_cast))
        
    unknown07 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown07: %04x"%(unknown07))

    transition_cast_id = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("transition_cast_id: %d"%(transition_cast_id))

    unknown08 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown08: %04x"%(unknown08))

    unknown09 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown09: %04x"%(unknown09))

    fps = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("fps: %d"%(fps))

    unknown10 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_MAIN_CHANNEL_INFO:
        logging.debug("unknown10: %04x"%(unknown10))

    main_data = {}
    if fps != 0 or sound1_cast != 0 or sound2_cast != 0 or script != 0:
        main_data['fps'] = fps
        main_data['transition_cast_id'] = transition_cast_id
        main_data['sound1_cast'] = sound1_cast
        main_data['sound2_cast'] = sound2_cast
        main_data['script'] = script

    return main_data


# ====================================================================================================================================
# Palette channel info (Director 4) 
def read_palette_channel_info_v4(frameData):
    indx = 0
    # Palette channel info
    palette_id = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    
    palette_name = get_palette_dir4(palette_id)
    
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("palette: %s"%(palette_name))

    unknown2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown2: %04x"%(unknown2))

    operation = int(frameData[indx])
    indx += 1
    
    operation = get_operation_dir5(operation)
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("operation: %s"%(operation))

    fps = int(frameData[indx])
    indx += 1
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("fps: %d"%(fps))

    unknown4 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown4: %04x"%(unknown4))

    cycles = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("cycles: %d"%(cycles))

    unknown6 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown6: %04x"%(unknown6))

    unknown7 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown7: %04x"%(unknown7))

    unknown8 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown8: %04x"%(unknown8))

    unknown9 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown9: %04x"%(unknown9))
        
    palette_data = {}
    if palette_id != 0:
        palette_data['fps'] = fps
        palette_data['operation'] = operation
        palette_data['palette_id'] = palette_id
        palette_data['cycles'] = cycles

    return palette_data
    
# ====================================================================================================================================
# Palette channel info (Director 5) 
def read_palette_channel_info_v5(frameData):
    indx = 0
    # Palette channel info
    unknown01 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown01: %04x"%(unknown01))

    palette_id = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    
    palette_name = get_palette_dir5(palette_id)
    
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("palette: %s"%(palette_name))
        
    fps = int(frameData[indx])
    indx += 1
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("fps: %d"%(fps))

    operation = int(frameData[indx])
    indx += 1
    
    operation = get_operation_dir5(operation)
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("operation: %s"%(operation))

    unknown02 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown02: %04x"%(unknown02))

    unknown03 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("unknown03: %04x"%(unknown03))
        
    cycles = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_PALETTE_CHANNEL_INFO:
        logging.debug("cycles: %d"%(cycles))

    
    palette_data = {}
    if palette_id != 0:
        palette_data['fps'] = fps
        palette_data['palette_id'] = palette_id
        palette_data['operation'] = operation
        palette_data['cycles'] = cycles

    return palette_data
# ====================================================================================================================================
# Sprite channel info (Director 4) 
def read_sprite_channel_info_v4(frameData, i):
    indx = 0
    # Sprite info
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] ----------------------------"%(i))
    # Read sprite info
    spriteType = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    spriteTypeName = get_sprite_type_dir4(spriteType)
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] spriteType: %s (%s)"%(i, spriteType, spriteTypeName))

    foregroundColor = int(frameData[indx])
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] foregroundColor: %d"%(i, foregroundColor))

    backgroundColor = int(frameData[indx])
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] backgroundColor: %d"%(i, backgroundColor))

    flags = int(frameData[indx])
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] flags: %x"%(i, flags))

    ink_type = int(frameData[indx])
    
    # The first two bits of ink_type is also a flag bit
    unknown_flag = ((ink_type >> 7) & 1)
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] unknown_flag: %d"%(i, unknown_flag))

    trails = ((ink_type >> 6) & 1)
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] trails: %d"%(i, trails))

    ink_type_name = get_ink(ink_type & 0x3F)
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] ink_type: %s (%s)"%(i, ink_type, ink_type_name))

    castId = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] castId: %d"%(i, castId))

    y = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] y: %d"%(i, y))

    x = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] x: %d"%(i, x))

    height = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] height: %d"%(i, height))

    width = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] width: %d"%(i, width))

    flag1 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    flag1 = (flag1 & 0xFFFF)
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] flag1: %04x"%(i, flag1))
    
    flag2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    flag2 = (flag2 & 0xFFFF)
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] flag2: %04x"%(i, flag2))
    
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
            logging.debug("Empty castId (%d) in Sprite[%d]"%(castId, i))
        
        return {}

# ====================================================================================================================================
# Sprite channel info (Director 5) 
def read_sprite_channel_info_v5(frameData, i):
    indx = 0
    # Sprite info
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] ----------------------------"%(i))
    # Read sprite info
    unknown01 = int(frameData[indx])
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] unknown01: %d"%(i, unknown01))

    ink_type = int(frameData[indx])
    
    # The first two bits of ink_type is also a flag bit
    unknown_flag = ((ink_type >> 7) & 1)
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] unknown_flag: %d"%(i, unknown_flag))

    trails = ((ink_type >> 6) & 1)
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] trails: %d"%(i, trails))

    ink_type_name = get_ink(ink_type & 0x3F)
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] ink_type: %s (%s)"%(i, ink_type, ink_type_name))
        
    spriteType = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    spriteTypeName = get_sprite_type_dir4(spriteType) 
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] spriteType: %s (%s)"%(i, spriteType, spriteTypeName))

    castId = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] castId: %d"%(i, castId))

    unknown02 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] unknown02: %04x"%(i, unknown02))

    unknown03 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] unknown03: %04x"%(i, unknown03))

    foregroundColor = frameData[indx]
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] foregroundColor: %d"%(i, foregroundColor))

    backgroundColor = frameData[indx]
    indx += 1
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] backgroundColor: %d"%(i, backgroundColor))

    y = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] y: %d"%(i, y))

    x = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] x: %d"%(i, x))

    height = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] height: %d"%(i, height))

    width = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] width: %d"%(i, width))

    flag2 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    flag2 = (flag2 & 0xFFFF)
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] flag2: %04x"%(i, flag2))
        
    flag1 = struct.unpack(">h", frameData[(indx):(indx+2)])[0]
    flag1 = (flag1 & 0xFFFF)
    indx = indx + 2
    if DEBUG_SPRITE_INFO:
        logging.debug("Sprite[%d] flag1: %04x"%(i, flag1))

    
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
            logging.debug("Empty castId (%d) in Sprite[%d]"%(castId, i))
        
        return {}

    return sprite_data
    
# ====================================================================================================================================
# Reads from VWSC channel data the score elements
def parse_vwsc_channels(channelData, frame_size, column):
    cdata = {}
    
    indx = 0
    
    cdata['main'] = {}
    cdata['palette'] = {}
    cdata['score'] = []

    if frame_size == 20:
        # Director 4
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("Director 4?")
            logging.debug("[%d] Main channel info ----------------------------"%(column))
        frameData = channelData[indx:(indx+frame_size)]
        cdata['main'] = read_main_channel_info_v4(frameData)
        indx += frame_size
        
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("[%d] Palette channel info ----------------------------"%(column))
        frameData = channelData[indx:(indx+frame_size)]
        cdata['palette'] = read_palette_channel_info_v4(frameData)
        indx += frame_size
    elif frame_size == 24:
        # Director 5
        if DEBUG_MAIN_CHANNEL_INFO:
            logging.debug("Director 5?")
            logging.debug("[%d] Main channel info ----------------------------"%(column))
        frameData = channelData[indx:(indx+frame_size)]
        cdata['main'] = read_main_channel_info_v5(frameData)
        indx += frame_size
        
        if DEBUG_PALETTE_CHANNEL_INFO:
            logging.debug("[%d] Palette channel info ----------------------------"%(column))
        frameData = channelData[indx:(indx+frame_size)]
        cdata['palette'] = read_palette_channel_info_v5(frameData)
        indx += frame_size
        
    else:
        logging.warn("Unknown director frame size: %d"%(frame_size))
        
    i = 1
    SPRITE_DATA_SIZE = 24
    while indx < len(channelData):
        if DEBUG_SPRITE_INFO:
            logging.debug("[%d] Sprite channel info ----------------------------"%(column))
        if frame_size == 20:
            # Director 4
            if DEBUG_SPRITE_INFO:
                logging.debug("Director 4?")
            frameData = channelData[indx:(indx+frame_size)]
            cdata['score'].append(read_sprite_channel_info_v4(frameData, i))
        
        elif frame_size == 24:
            # Director 5
            if DEBUG_SPRITE_INFO:
                logging.debug("Director 5?")
            frameData = channelData[indx:(indx+frame_size)]
            cdata['score'].append(read_sprite_channel_info_v5(frameData, i))
            
        else:
            logging.warn("Unknown director frame size: %d"%(frame_size))

        indx += frame_size
        
        i += 1
        
    
    return cdata

# ====================================================================================================================================
# Reads from VWSC data the score elements
def parse_vwsc_data(fdata):
    logging.debug("parse_vwsc_data ======================")
    vwsc_data = []
    
    idx = 0
    dataSize = struct.unpack(">i", fdata[(idx):(idx+4)])[0]
    idx = idx + 4
    logging.debug("dataSize = %08x"%(dataSize))

    dataMarker = struct.unpack(">i", fdata[(idx):(idx+4)])[0]
    idx = idx + 4
    logging.debug("dataMarker = %08x"%(dataMarker))

    if dataMarker != 0x14:
        logging.error('Can\'f find data marker in VWSC data!')
        sys.exit(-1)
    
    if len(fdata) != dataSize:
        logging.error('Bad VWSC data size: (%d != %d)'%(len(fdata), dataSize))
        sys.exit(-1)
        
    frame_count =  struct.unpack(">i", fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("frame_count = %08x"%(frame_count))
    
    unknown01 =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown01 = %04x"%(unknown01))
    
    frame_size =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("frame_size = %04x"%(frame_size))
    
    channel_count =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("channel_count = %04x"%(channel_count))
    
    unknown02 =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown02 = %04x"%(unknown02))
    
    channelDataList = ["\0"] * (channel_count * frame_size)
    channelDataStr = "".join(channelDataList)
    
    column = 0
    while idx < dataSize:
        column += 1
        logging.debug("column: %d idx: %08x"%(column, idx))
        channelSize = struct.unpack(">h", fdata[(idx):(idx+2)])[0]
        idx = idx + 2
        logging.debug("channelSize: %d"%(channelSize))
        if channelSize == 2:
            logging.debug('This frame is equals to the previous one!')
            vwsc_data.append(vwsc_data[-1])
            continue
        
        channelSize -= 2
        
        # Channel data
        if channelSize > 0:
            # Apply the differences from the previous channel
            while channelSize > 0:
                delta_size = struct.unpack(">h", fdata[(idx):(idx+2)])[0]
                if (delta_size > channelSize) or (delta_size <= 0):
                    logging.warn("Delta size out of limits: %d > %d"%(delta_size, channelSize))
                    break
                idx = idx + 2
                delta_offset = struct.unpack(">h", fdata[(idx):(idx+2)])[0]
                if delta_offset < 0:
                    delta_offset = (delta_offset & 0xFF)
                
                idx = idx + 2
                channelSize -= 4
            
                logging.debug("delta_size: %d"%(delta_size))
                logging.debug("delta_offset: %d"%(delta_offset))

                deltaData = fdata[(idx):(idx+delta_size)].decode('ISO-8859-1')
                idx = idx + delta_size
                channelSize -= delta_size
                
                for i in range(0, delta_size):
                    channelDataList[delta_offset + i] = deltaData[i]
            
            channelDataStr = ("".join(channelDataList)).encode('ISO-8859-1')
            vwsc_data.append(parse_vwsc_channels(channelDataStr, frame_size, column))
            
        else:
            logging.debug('Empty channel!')
            vwsc_data.append([])
        
        idx += channelSize
        
    
    return vwsc_data

# ====================================================================================================================================
# Reads from VWSC file the score elements
def parse_vwsc_file(vwsc_file):
    vwsc_data = []
    
    with open(vwsc_file, mode='rb') as file:
        fdata = file.read()

        # Check if the real VWSC data is wrapped into other data
        indx = 0
        dataSize = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        
        dataMarker = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        
        logging.debug("parse_vwsc_file ============================================")
        logging.debug("dataSize: %d"%(dataSize))
        logging.debug("dataMarker: %d"%(dataMarker))
        
        markersidx = 0
        if dataMarker != 0x14:
            # VWSC data is wrapped into other data (DIR file and not DRX file)
            if len(fdata) != dataSize:
                logging.error('Bad VWSC file size: (%d != %d)'%(len(fdata), dataSize))
                sys.exit(-1)
            
            unknown_01 =  struct.unpack(">i", fdata[indx:indx+4])[0]
            indx += 4
            logging.debug("unknown_01 = %08x"%(unknown_01))
            
            nmarkers =  struct.unpack(">i", fdata[indx:indx+4])[0]
            indx += 4
            logging.debug("nmarkers = %08x"%(nmarkers))
            
            nmarkers1 =  struct.unpack(">i", fdata[indx:indx+4])[0]
            indx += 4
            logging.debug("nmarkers1 = %08x"%(nmarkers1))
            
            lastMarker =  struct.unpack(">i", fdata[indx:indx+4])[0]
            indx += 4
            logging.debug("lastMarker = %08x"%(lastMarker))
            
            
            markersidx = indx
            
            # Skip the markers because at this moment I don't know what are they
            # useful for
            indx += nmarkers1 * 4
            
            dataSize = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
            indx = indx + 4

            dataMarker = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
            indx = indx + 4
        
        if dataMarker != 0x14:
            logging.error('Can\'f find data marker in VWSC file!')
            sys.exit(-1)
        
        indx -= 8
        data = fdata[indx:(indx+dataSize)]
        indx += dataSize
        
        # VWSC data structure depends on Director version
        vwsc_data = parse_vwsc_data(data)
        
        # Check of many data is left
        logging.debug('Data left: %d'%(len(fdata)-indx))
        
        
    return vwsc_data


# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("USAGE: vwscxtract <work directory>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        vwsc_file = None
        
        for f in os.listdir(os.path.join(sys.argv[1], BINDIR)):
            if f.endswith('VWSC'):
                vwsc_file = f
                break
        
        if vwsc_file is None:
            logging.error('Can not find a VWSC file!')
            sys.exit(-1)
        
        vwsc_elements = parse_vwsc_file(os.path.join(sys.argv[1], BINDIR, vwsc_file))
        
        # Transform the elements to the appropiate format
        data = {}
        data['lastChannel'] = 0
        data['lastFrame'] = len(vwsc_elements)
        if data['lastFrame'] > 0:
            data['lastChannel'] = len(vwsc_elements[0]['score'])
        
        data['transition'] = []
        data['palette'] = []
        data['sound1'] = []
        data['sound2'] = []
        data['tempo'] = []
        data['script'] = []
        data['sprite'] = []
        for i in range(0, data['lastChannel']):
            data['sprite'].append([])
            
        for i in range(0, data['lastFrame']):
            if ('transition_id' in vwsc_elements[i]['main'] and
                 vwsc_elements[i]['main']['transition_id'] != ''):
                tran = {}
                tran['frame'] = i+1
                # TODO! Convertir esto en miembros del casting
                tran['transition_id'] = vwsc_elements[i]['main']['transition_id']
                tran['transition_chunk_size'] = vwsc_elements[i]['main']['transition_chunk_size']
                tran['transition_duration'] = vwsc_elements[i]['main']['transition_duration']
                
                data['transition'].append(tran)
            
            if ('sound1_cast' in vwsc_elements[i]['main'] and
                 vwsc_elements[i]['main']['sound1_cast'] > 0):    
                
                prev = False
                if len(data['sound1']) > 0 and data['sound1'][-1]['endFrame'] == i:
                    prev = data['sound1'][-1]

                if (prev and prev['castId'] == vwsc_elements[i]['main']['sound1_cast']):
                    # This is the same as the previous sound
                    prev['endFrame'] = i+1
                    
                else:
                    # This is a new sound
                    snd = {}
                    snd['startFrame'] = i+1
                    snd['endFrame'] = i+1
                    snd['castId'] = vwsc_elements[i]['main']['sound1_cast']
                    data['sound1'].append(snd)   
                
            if ('sound2_cast' in vwsc_elements[i]['main'] and 
                 vwsc_elements[i]['main']['sound2_cast'] > 0):
                prev = False
                if len(data['sound2']) > 0 and data['sound2'][-1]['endFrame'] == i:
                    prev = data['sound2'][-1]

                if (prev and prev['castId'] == vwsc_elements[i]['main']['sound2_cast']):
                    # This is the same as the previous sound
                    prev['endFrame'] = i+1
                    
                else:
                    # This is a new sound
                    snd = {}
                    snd['startFrame'] = i+1
                    snd['endFrame'] = i+1
                    snd['castId'] = vwsc_elements[i]['main']['sound2_cast']
                    data['sound2'].append(snd)                  
              
            if ('script' in vwsc_elements[i]['main'] and 
                 vwsc_elements[i]['main']['script'] > 0):
                scr = {}
                scr['frame'] = i+1
                scr['castId'] = vwsc_elements[i]['main']['script']
                data['script'].append(scr)             
            
            if ('fps' in vwsc_elements[i]['main'] and 
                 vwsc_elements[i]['main']['fps'] > 0):
                fps = {}
                fps['frame'] = i+1
                fps['fps'] = vwsc_elements[i]['main']['fps']
                data['tempo'].append(fps)             
            
            if 'palette_id' in vwsc_elements[i]['palette']:
                pal = {}
                pal['frame'] = i+1
                pal['palette_id'] = vwsc_elements[i]['palette']['palette_id']
                data['palette'].append(pal)            
            
        for i in range(0, data['lastFrame']):
            for j in range(0, data['lastChannel']):
                if 'castId' in vwsc_elements[i]['score'][j]:
                    sprite = {}
                    sprite['castId'] = vwsc_elements[i]['score'][j]['castId']
                    sprite['backColor'] = vwsc_elements[i]['score'][j]['backgroundColor']
                    sprite['foreColor'] = vwsc_elements[i]['score'][j]['foregroundColor']
                    sprite['width'] = vwsc_elements[i]['score'][j]['width']
                    sprite['height'] = vwsc_elements[i]['score'][j]['height']
                    sprite['ink'] = vwsc_elements[i]['score'][j]['ink_type']
                    sprite['type'] = vwsc_elements[i]['score'][j]['spriteType']
                    sprite['locH'] = vwsc_elements[i]['score'][j]['x']
                    sprite['locV'] = vwsc_elements[i]['score'][j]['y']
                    sprite['editable'] = vwsc_elements[i]['score'][j]['editable']
                    sprite['moveable'] = vwsc_elements[i]['score'][j]['moveable']
                    sprite['trails'] = vwsc_elements[i]['score'][j]['trails']
                    
                    prev = False
                    if len(data['sprite'][j]) > 0 and data['sprite'][j][-1]['endFrame'] == i:
                        prev = data['sprite'][j][-1]
                        
                    if (prev and prev['castId'] == sprite['castId'] and
                        prev['castId'] == sprite['castId'] and
                        prev['backColor'] == sprite['backColor'] and
                        prev['foreColor'] == sprite['foreColor'] and
                        prev['width'] == sprite['width'] and
                        prev['height'] == sprite['height'] and
                        prev['ink'] == sprite['ink'] and
                        prev['type'] == sprite['type'] and
                        prev['locH'] == sprite['locH'] and
                        prev['locV'] == sprite['locV'] and
                        prev['editable'] == sprite['editable'] and
                        prev['moveable'] == sprite['moveable'] and
                        prev['trails'] == sprite['trails']):
                        
                        # This is the same as previous sprite
                        prev['endFrame'] = i+1
                    
                    else:
                        # This is a new sprite
                        sprite['startFrame'] = i+1
                        sprite['endFrame'] = i+1                    
                        sprite['locZ'] = j+1
                        sprite['left'] = math.ceil(sprite['locH'] - sprite['width']/2)
                        sprite['top'] = math.ceil(sprite['locV'] - sprite['height']/2)
                        sprite['right'] = sprite['left'] + sprite['width']
                        sprite['bottom'] = sprite['top'] + sprite['height']

                        data['sprite'][j].append(sprite)                      
        

      
        
        
        # Write score data to JSON file
        with open(os.path.join(sys.argv[1], 'score.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(data, indent=4, sort_keys=True).encode('utf-8'))

