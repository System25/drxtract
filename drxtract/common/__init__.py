# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .constants import DIR_SPRITE_TYPES, DIR_INK_NAMES, DIR_TRANSITION_NAMES, \
    DIR_PALETTE_NAMES, DIR4_PALETTE_NAMES, DIR_SHAPE_NAMES

from ..lingosrc.util import get_keys

# ==============================================================================
# Translate palette number to string representation
def get_palette_name(value: int) -> str:
    if value <= 0:
        # There is no zero casting member so
        # it must be a predefined palette
        value = value - 1
    
    if value in get_keys(DIR_PALETTE_NAMES):
        return DIR_PALETTE_NAMES[value]
    
    return str(value)



# ==============================================================================
# Translate a transition number to string representation
def get_transition_name(value: int) -> str:
    if value in get_keys(DIR_TRANSITION_NAMES):
        return DIR_TRANSITION_NAMES[value]
    
    return str(value)

# ==============================================================================
# Translate a shape number to string representation
def get_shape_name(value: int) -> str:
    if value in get_keys(DIR_SHAPE_NAMES):
        return DIR_SHAPE_NAMES[value]
    
    return str(value)

__all__ = ['get_palette_name', 'get_transition_name', 'get_shape_name',
           'DIR_SPRITE_TYPES', 'DIR_INK_NAMES', 'DIR_TRANSITION_NAMES',
           'DIR_PALETTE_NAMES', 'DIR4_PALETTE_NAMES', 'DIR_SHAPE_NAMES']
