# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from abc import ABCMeta, abstractmethod
import io
import struct
import logging
from typing import Dict
from ..lingosrc.util import repeat_string, get_keys

from ..palettes import GRAYSCALE_256COLORS_PALETTE, \
    METALLIC_256COLORS_PALETTE, \
    NTSC_256COLORS_PALETTE, PASTELS_256COLORS_PALETTE, \
    RAINBOW_256COLORS_PALETTE, SYSTEM_MAC_256COLORS_PALETTE, \
    SYSTEM_WINDOWS_DIR4_256COLORS_PALETTE, SYSTEM_WINDOWS_256COLORS_PALETTE, \
    VIVID_256COLORS_PALETTE, WEB_256COLORS_PALETTE

# ============================================ Default color palettes =========
BW_PALETTE = (
  255, 255, 255, 0, # white  
  0, 0, 0, 0        # black  
)

SYSTEM_MAC_16COLORS_PALETTE = (

  255, 255, 0, 0,   # yellow
  255, 160, 0, 0,   # orange
  255, 0, 0, 0,     # red
  255, 0, 255, 0,   # magenta
  128, 0, 128, 0,   # purple
  0, 0, 255, 0,     # blue
  0, 255, 255, 0,   # cyan

  0, 128, 0, 0,     # green
  0, 100, 0, 0,     # dark green
  165, 42, 42, 0,   # brown
  210, 180, 140, 0, # tan
  211, 211, 211, 0, # light gray
  128, 128, 128, 0, # gray
  169, 169, 169, 0, # dark gray
  0, 0, 0, 0        # black
 )


SYSTEM_WINDOWS_16COLORS_PALETTE = (
  255, 255, 255, 0, # white
  0, 255, 255, 0,   # aqua
  255, 0, 255, 0,   # fuchsia
  0, 0, 255, 0,     # blue
  255, 255, 0, 0,   # yellow
  0, 255, 0, 0,     # lime
  255, 0, 0, 0,     # red
  128, 128, 128, 0, # gray

  192, 192, 192, 0, # silver
  0, 128, 128, 0,   # teal
  128, 0, 128, 0,   # purple
  0, 0, 128, 0,     # navy
  128, 128, 0, 0,   # olive
  0, 128, 0, 0,     # green
  128, 0, 0, 0,     # maroon
  0, 0, 0, 0        # black
 )


PALETTES: Dict[int, Dict[str, tuple]] = {
    2: {
        'black and white': BW_PALETTE
    },
    4: {
        'systemMac': SYSTEM_MAC_16COLORS_PALETTE,
        'systemWin': SYSTEM_WINDOWS_16COLORS_PALETTE,
        'default': SYSTEM_WINDOWS_16COLORS_PALETTE
    },
    8: {
        'grayscale': GRAYSCALE_256COLORS_PALETTE,
        'metallic': METALLIC_256COLORS_PALETTE,
        'ntsc': NTSC_256COLORS_PALETTE,
        'pastels': PASTELS_256COLORS_PALETTE,
        'rainbow': RAINBOW_256COLORS_PALETTE,
        'systemMac': SYSTEM_MAC_256COLORS_PALETTE,
        'systemWinDir4': SYSTEM_WINDOWS_DIR4_256COLORS_PALETTE,
        'systemWin': SYSTEM_WINDOWS_256COLORS_PALETTE,
        'vivid': VIVID_256COLORS_PALETTE,
        'web216': WEB_256COLORS_PALETTE,
        'default': SYSTEM_WINDOWS_256COLORS_PALETTE
    }
}



#
# Abstract BITD decoder class.
# 
class Decoder:
    """This class represents a BITD decoder"""
    __metaclass__ = ABCMeta
    
    def __init__(self, nbits: int, ncolors: int):
        self.nbits: int = nbits
        self.ncolors: int = ncolors
        self.bytesIo: io.BytesIO = io.BytesIO()

    def writeBmpHeader(self, size:int, offset:int):
        # Write Windows bitmap file header
        self.bytesIo.write('BM'.encode('ascii'))
        
        values = (size, # The size of the BMP file in bytes
                  0, # Reserved
                  0, # Reserved
                  offset # Data offset
                 )
        packed_data = struct.pack('<ihhi', *values)
        self.bytesIo.write(packed_data)
        
    def writeBitmapInfoHeader(self, width:int, height:int, bpp: int):
        # Write BITMAPINFOHEADER
        values = (40, # the size of this header (40 bytes)
                  width, # the bitmap width in pixels (signed integer)
                  height, # the bitmap height in pixels (signed integer)
                  1, # the number of color planes (must be 1)
                  # the number of bits per pixel, which is the color depth of
                  # the image. Typical values are 1, 4, 8, 16, 24 and 32.
                  bpp, 
                  0, # the compression method being used
                  # the image size. This is the size of the raw bitmap data;
                  # a dummy 0 can be given for BI_RGB bitmaps.
                  0,
                  # the horizontal resolution of the image.
                  # (pixel per meter, signed integer)
                  0,
                  # the vertical resolution of the image.
                  #(pixel per meter, signed integer)
                  0, 
                  # the number of colors in the color palette,
                  # or 0 to default to 2n
                  self.ncolors, 
                  # the number of important colors used, or 0 when every color
                  # is important; generally ignored
                  self.ncolors  
                 )
        packed_data = struct.pack('<iiihhiiiiii', *values)
        self.bytesIo.write(packed_data)
        
    def writeColorPalette(self, palette_name: str, palette_data: bytes):
        length = self.ncolors*4
        fmt: str = repeat_string('B', length)
        packed_data = bytes()
        if len(palette_data) > 0:
            # Custom palette
            logging.debug('Using custom palette')
            packed_data = struct.pack(fmt, *palette_data[0:length])
        
        else:
            # System palette
            nb = self.nbits
            if nb in get_keys(PALETTES):
                if palette_name in get_keys(PALETTES[nb]):
                    logging.debug('Using %s palette', palette_name)
                    palette = PALETTES[nb][palette_name]
                    packed_data = struct.pack(fmt, *palette)
                else:
                    logging.warning("Using default windows color palette!")
                    palette = PALETTES[nb]['default']
                    packed_data = struct.pack(fmt, *palette)  
        
        self.bytesIo.write(packed_data)
        
    def writeData(self, data: bytes):
        self.bytesIo.write(data)
    
    def getBmpImage(self) -> bytes:
        data = self.bytesIo.getvalue()
        self.bytesIo.close()
        self.bytesIo = io.BytesIO()
        return data
        

    @abstractmethod
    def decode(self, fdata:bytes, bmp_width: int, bmp_height: int,
               bmp_padding_w: int, bmp_padding_h: int,
               palette_name: str, palette_data: bytes) -> bytes:
        pass
