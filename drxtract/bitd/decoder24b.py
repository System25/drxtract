# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .decoder import Decoder
import logging

#
# 24 bits per pixel BITD decoder class.
# 
class Decoder24b(Decoder):
    """This class represents a 24 bits BITD image decoder"""
    
    def __init__(self):
        super().__init__(24, 0)

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
                for _ in range(0, run_length):
                    p = y*width + x
                    data[p] = run_value
                    x += 1
                    if x >= width:
                        x = 0
                        y -= 1
                
    
            elif val != 0:
                # Not RLE encoded
                run_length = val + 1
                idx = idx + 1
                for _ in range(0, run_length):
                    p = y*width + x
                    data[p] = fdata[idx]
                    idx = idx + 1
                    x += 1
                    if x >= width:
                        x = 0
                        y -= 1
    
            else: # val is zero
                idx = idx + 1
                run_value = fdata[idx]
                idx = idx + 1
                p = y*width + x
                data[p] = run_value
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
    
    
        # Order RGB bytes and discard Alpha channel
        dataMix = bytearray(w*3 * h)
        w4 = w*4
        w3 = w*3
        w2 = w*2
        w1 = w
        for y in range(0, h):
            yw4 = y*w4
            yw3 = y*w3
            for x in range(0, w):
                sr = yw4 + w3 + x
                dr = yw3 + x*3 + 0
                dataMix[dr] = data[sr]  # Red
                
                sg = yw4 + w2 + x
                dg = yw3 + x*3 + 1
                dataMix[dg] = data[sg]  # Green
                
                sb = yw4 + w1 + x
                db = yw3 + x*3 + 2
                dataMix[db] = data[sb]  # Blue
        
        return dataMix

    def decode_raw_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:

          
        raise NotImplementedError()



    def decode(self, fdata:bytes, bmp_width: int, bmp_height: int,
               bmp_padding_w: int, bmp_padding_h: int,
               palette_name: str, palette_data: bytes) -> bytes:
    
        bmp_bpp = 24
        hsize = 40
        
        # Sometimes the padding is negative
        if bmp_padding_h < 0:
            bmp_height = bmp_height - bmp_padding_h
            bmp_padding_h = 0 
        
        # The size of the BMP file in bytes
        size: int = bmp_width*bmp_height*3+hsize+14
        # Data offset
        offset: int = hsize+14
        
        self.writeBmpHeader(size, offset)

        self.writeBitmapInfoHeader(bmp_width, bmp_height, bmp_bpp)
    
        width = bmp_width*4
    
        # get the pixel information
        # RLE encoded bytes are:
        #   - RLE encoded Alpha channel for 1 row
        #   - RLE encoded Blue channel for 1 row
        #   - RLE encoded Green channel for 1 row
        #   - RLE encoded Red channel for 1 row
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
