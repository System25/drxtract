# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .decoder import Decoder
import logging

#
# 4 bits per pixel BITD decoder class.
# 
class Decoder4b(Decoder):
    """This class represents a 4 bits BITD image decoder"""
    
    def __init__(self):
        super().__init__(4, 16)

    def decode_compressed_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:
        raise NotImplementedError()

    def decode_raw_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:
        raise NotImplementedError()

    def decode(self, fdata:bytes, bmp_width: int, bmp_height: int,
               bmp_padding_w: int, bmp_padding_h: int,
               palette_name: str, palette_data: bytes) -> bytes:
    
        bmp_bpp = 4
        
        # Sometimes the padding is negative
        if bmp_padding_h < 0:
            bmp_height = bmp_height - bmp_padding_h
            bmp_padding_h = 0 
        
        # The size of the BMP file in bytes
        size: int = bmp_width*bmp_height+(self.ncolors*4)+40+14
        # Data offset
        offset: int = ((self.ncolors*4)+40+14)
        
        self.writeBmpHeader(size, offset)

        self.writeBitmapInfoHeader(bmp_width, bmp_height, bmp_bpp)
    
        self.writeColorPalette(palette_name, palette_data)
    
        width = bmp_width
        if (width%4) > 0:
            # The image width must be divisible by four
            width = width + 4 - (width%4)    
    
        # get the pixel information
        w = bmp_width - bmp_padding_w
    
        w_size = int(w/2)
        if (w%2) > 0:
            w_size = w_size + 1
        # Must be an even number
        w_size = w_size + (w_size%2)  
    
        if len(fdata) == w_size*(bmp_height-bmp_padding_h):
            logging.debug("The size of the data matches the image resolution."
                         + "Not RLE compressed!")    
            bmp = self.decode_raw_data(fdata, bmp_width, bmp_height,
                                       bmp_padding_w, bmp_padding_h,
                                       width, w_size)
        
        else:
            logging.debug("The image must be compressed!")
            bmp = self.decode_compressed_data(fdata, bmp_width, bmp_height,
                                       bmp_padding_w, bmp_padding_h,
                                       width, w_size)
        

    
        self.writeColorData(bmp)
        
        return self.getBmpImage()
