# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .decoder import Decoder
import logging
import struct

#
# 16 bits per pixel BITD decoder class.
# 
class Decoder16b(Decoder):
    """This class represents a 16 bits BITD image decoder"""
    
    def __init__(self):
        super().__init__(16, 0)

    def decode_compressed_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:
        # Create a white image
        data = bytearray(width * h)
        logging.debug("w: %d witdh: %d", w, width)
        x = 0
        y = h - 1
        idx = 0
        while (idx < len(fdata)) and (y>=0):
            val = fdata[idx]
            if (val & 0x80) != 0:
                # RLE encoded
                run_length = 257 - val
                idx = idx + 1
                run_value = fdata[idx]
                idx = idx + 1
    
                # Jump to next byte when necessary
                if ((x + run_length) > w) and (x < w):
                    x = w
    
                # Jump to next row when necessary
                if ((x + run_length) > width):
                    x = 0
                    y -= 1
    
                for _ in range(0, run_length):
                    p = y*width + x
                    data[p] = run_value
                    x += 1
                
    
            else:
                # Not RLE encoded
                run_length = val + 1
                idx = idx + 1
    
                # Jump to next byte when necessary
                if ((x + run_length) > w) and (x < w):
                    x = w
    
                # Jump to next row when necessary
                if ((x + run_length) > width):
                    x = 0
                    y -= 1
    
                for _ in range(0, run_length):
                    p = y*width + x
                    data[p] = fdata[idx]
                    idx = idx + 1
                    x += 1
                    if x >= width:
                        x = 0
                        y -= 1
    
        if y!=-1 or x!=0:
            logging.warning("Not enought data to decode. Probably the image is "
                         + "not properly generated. (y=%s, x=%s)", y, x)
    
        if idx != len(fdata):
            logging.warning("there is more data to decode. Probably the image "
                         + "is not properly generated. (%s != %s)", idx,
                         len(fdata))
    
    
        # Sort lower and upper bytes
        dataMix = bytearray(width * h)
        w2 = w*2
        w1 = w
        w0 = 0
        for y in range(0, h):
            yw2 = y*w2
            for x in range(0, w):
                psu = yw2 + w1 + x
                pdu = yw2 + x*2 + 0
                dataMix[pdu] = data[psu]  # Upper
                
                psl = yw2 + w0 + x
                pdl = yw2 + x*2 + 1
                dataMix[pdl] = data[psl]  # Lower
        
        return dataMix

    def decode_raw_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:

          
        raise NotImplementedError()

    def writeBitmapInfoHeader(self, witdh:int, height:int, bpp: int):
        # Write BITMAPINFOHEADER
        values = (124, # the size of this header (hsize bytes)
                  witdh, # the bitmap width in pixels (signed integer)
                  height, # the bitmap height in pixels (signed integer)
                  1, # the number of color planes (must be 1)
                  # the number of bits per pixel, which is the color depth of
                  # the image. Typical values are 1, 4, 8, 16, 24 and 32.
                  bpp,
                  3, # the compression method being used (BI_BITFIELDS)
                  # the image size. This is the size of the raw bitmap data;
                  #a dummy 0 can be given for BI_RGB bitmaps.
                  0,
                  # the horizontal resolution of the image. (pixel per meter,
                  # signed integer)
                  0,
                  # the vertical resolution of the image. (pixel per meter,
                  # signed integer)
                  0,
                  # the number of colors in the color palette, or 0 to
                  # default to 2n
                  0,
                  # the number of important colors used, or 0 when every color
                  # is important; generally ignored
                  0,
                  0x00007C00, # Red channel bitmask
                  0x000003E0, # Green channel bitmask
                  0x0000001F, # Blue channel bitmask
                  0x00000000, # Alpha channel bitmask
                  0x73524742, # "BGRs"
                  # CIEXYZTRIPLE Color Space endpoints
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 
                  0, # Red Gamma
                  0, # Green Gamma
                  0, # Blue Gamma
                 )
        packed_data = struct.pack('<iiihhIIIIIIIIIIIIIIIIIIIIIIIIIII', *values)
        self.writeData(packed_data)

    def decode(self, fdata:bytes, bmp_width: int, bmp_height: int,
               bmp_padding_w: int, bmp_padding_h: int,
               palette_name: str, palette_data: bytes) -> bytes:
    
        bmp_bpp = 16
        hsize = 124
        
        # Sometimes the padding is negative
        if bmp_padding_h < 0:
            bmp_height = bmp_height - bmp_padding_h
            bmp_padding_h = 0 
        
        # The size of the BMP file in bytes
        size: int = bmp_width*bmp_height*2+hsize+14
        # Data offset
        offset: int = hsize+14
        
        self.writeBmpHeader(size, offset)

        self.writeBitmapInfoHeader(bmp_width, bmp_height, bmp_bpp)
    
        width = bmp_width*2
    
        # get the pixel information
        # RLE encoded bytes contains 1 pixel color
        w_size = (bmp_width - bmp_padding_w) * 2
        
    
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
        

    
        self.writeData(bmp)
        
        return self.getBmpImage()
