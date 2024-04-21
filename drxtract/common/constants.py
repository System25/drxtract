# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import Dict

# I got this from D4Player project
DIR_SPRITE_TYPES: Dict[int, str] = {
    0: 'empty',
    1: 'image',
    2: 'rectangle',
    3: 'round_rectangle',
    4: 'ellipse',
    5: 'line_lt_br',
    6: 'line_bl_tr',
    7: 'text',
    8: 'button',
    9: 'checkbox',
    10: 'radio_button',
    16: 'shape'    
}

# I found this online:
# http://users.design.ucla.edu/~cariesta/MayaCourseNotes/html/body_director_basic.html
DIR_INK_NAMES: Dict[int, str] = {
    0: 'copy',
    1: 'transparent',
    2: 'reverse',
    3: 'ghost',
    4: 'not copy',
    5: 'not transparent',
    6: 'not reverse',
    7: 'not ghost',
    8: 'matte',
    9: 'mask',
    32: 'blend',
    33: 'add pin',
    34: 'add',
    35: 'subtract pin',
    36: 'background transparent',
    37: 'lightest',
    38: 'subtract',
    39: 'darkest',
    40: 'lighten',
    41: 'darken'
}



# I found this in: Director 8 Demystified
# (puppetTransition lingo script reference)
DIR_TRANSITION_NAMES: Dict[int, str] = {
    1: 'wipe right',
    2: 'wipe left',
    3: 'wipe down',
    4: 'wipe up',
    5: 'center out, horizontal',
    6: 'edges in, horizontal',
    7: 'center out, vertical',
    8: 'edges in, vertical',
    9: 'center out, square',
    10: 'edges in, square',
    11: 'push left',
    12: 'push right',
    13: 'push down',
    14: 'push up',
    15: 'reveal up',
    16: 'reveal up, right',
    17: 'reveal right',
    18: 'reveal down, right',
    19: 'reveal down',
    20: 'reveal down, left',
    21: 'reveal left',
    22: 'reveal up, left',
    23: 'dissolve, pixels fast',
    24: 'dissolve, boxy rectangles',
    25: 'dissolve, boxy squares',
    26: 'dissolve, patterns',
    27: 'random rows',
    28: 'random columns',
    29: 'cover down',
    30: 'cover down, left',
    31: 'cover down, right',
    32: 'cover left',
    33: 'cover right',
    34: 'cover up',
    35: 'cover up, left',
    36: 'cover up, right',
    37: 'venetian blinds',
    38: 'checkerboard',
    39: 'strips on bottom, build left',
    40: 'strips on bottom, build right',
    41: 'strips on left, build down',
    42: 'strips on left, build up',
    43: 'strips on right, build down',
    44: 'strips on right, build up',
    45: 'strips on top, build left',
    46: 'strips on top, build right',
    47: 'zoom open',
    48: 'zoom close',
    49: 'vertical blinds',
    50: 'dissolve, bits fast',
    51: 'dissolve, pixels',
    52: 'dissolve, bits'
}

# I found this in a german book called
# "Macromedia Director: Multimediaprogrammierung mit Lingo"
# https://books.google.es/books?id=UxLuBQAAQBAJ&pg=PA282&lpg=PA282&dq=macromedia+director+ntsc+web+grayscale+rainbow&source=bl&ots=tlcNQFqWod&sig=ACfU3U2d0o3Kv3y7_9umDgOCPGBDqooIzQ&hl=es&sa=X&ved=2ahUKEwjXs-rnlNXiAhVDrxoKHdcACWIQ6AEwB3oECAUQAQ#v=onepage&q=macromedia%20director%20ntsc%20web%20grayscale%20rainbow&f=false
DIR_PALETTE_NAMES: Dict[int, str] = {
    -1: 'systemMac',
    -102: 'systemWin',
    -2: 'rainbow',
    -3: 'grayscale',
    -4: 'pastels',
    -5: 'vivid',
    -6: 'ntsc',
    -7: 'metallic',
    -8: 'web216',
    -101: 'systemWinDir4'   
}

DIR4_PALETTE_NAMES: Dict[int, str] = {
    -1: 'systemMac',
    -65: 'systemWin',
    -2: 'rainbow',
    -3: 'grayscale',
    -4: 'pastels',
    -5: 'vivid',
    -6: 'ntsc',
    -7: 'metallic',
    -8: 'web216'
}

DIR_SHAPE_NAMES: Dict[int, str] = {
    1: 'rect',
    2: 'roundRect',
    3: 'oval',
    4: 'line'
}

__all__ = ['DIR_SPRITE_TYPES', 'DIR_INK_NAMES', 'DIR_TRANSITION_NAMES', 
    'DIR_PALETTE_NAMES', 'DIR4_PALETTE_NAMES', 'DIR_SHAPE_NAMES']
