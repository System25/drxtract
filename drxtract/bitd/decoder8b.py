# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .decoder import Decoder
import logging

#
# 8 bits per pixel BITD decoder class.
# 
class Decoder8b(Decoder):
    """This class represents a 8 bits BITD image decoder"""
    
    def __init__(self):
        super().__init__(8, 256)

    def decode_compressed_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:
        # Create a white image        
        w = w - padding_w
        w = w + (w%2)
        
        if w + padding_w > width:
            bw =  width + 4
        else:
            bw = width
        
        data = bytearray(bw * h)
        logging.debug("w=%d, h=%d, width=%d, padding_w=%d, bw=%d",
                     w, h-padding_h, width, padding_w, bw)
        x = 0
        y = h - 1 - padding_h
        idx = 0
        while (idx < len(fdata)) and (y>=0):
            val = fdata[idx]
            if (val & 0x80) != 0:
                # RLE encoded
                run_length = 257 - val
                if idx+1 >= len(fdata):
                    logging.error("Unexpected end of data! (data length=%s)",
                                  len(fdata))
                    break
                idx = idx + 1
                run_value = fdata[idx]
                idx = idx + 1
    
                if x + run_length > w:
                    logging.debug("Run too long! (%s, %s)", run_length, w-x)
    
                for _ in range(0, run_length):
                    if x >= w:
                        logging.debug("Painting out of image (rle)! "
                                      +"(x=%s y=%s col=%s)", x, y, run_value)
                        break

                    p = y*width + x + padding_w
                    data[p] = run_value
                    x += 1
                
                if x >= w:
                    x = 0
                    y -= 1
                    if y < 0:
                        break
    
            else:
                # Not RLE encoded
                run_length = val + 1
                idx = idx + 1
                if idx + run_length > len(fdata):
                    logging.error("Bad run length! (value=%s, available=%s)",
                                  run_length, len(fdata)-idx)
                    break
    
                for _ in range(0, run_length):
                    if x >= w:
                        logging.debug("Painting out of image (no-rle)! "
                                      + "(x=%s y=%s col=%s)", x, y,
                                      fdata[idx])
                        break
                    
                    p = y*width + x + padding_w
                    data[p] = fdata[idx]
                    x += 1            
    
                    idx = idx + 1
                    if idx > len(fdata):
                        logging.error("Bad run length! (value=%s)", run_length)
                        break
    
    
                if x >= w:           
                    x = 0
                    y -= 1
                    if y < 0:
                        break
    
        if y!=-1 or x!=0:
            logging.warning("Not enought data to decode. Probably the image"
                            + " is not properly generated. (y=%s, x=%s)", y, x)
    
        if idx != len(fdata):
            logging.warning("there is more data to decode. Probably the image "
                            + "is not properly generated. (%s != %s)", idx,
                            len(fdata))
        
        return data

    def decode_raw_data(self, fdata: bytes,
                        w:int, h:int,
                        padding_w:int, padding_h:int,
                        width:int, w_size:int) -> bytes:
        # Create a white image
        data = bytearray(width * h)
        y = h - 1 - padding_h
        w = w - padding_w
        idx = 0
        data_idx = 0
        
        while y>=0:
            # Fill left padding with white color
            data_idx = data_idx + padding_w
            
            # Get colors from BITD data
            idx = (y * w_size)
            
            x = 0
            while x < w:
                data[data_idx] = fdata[idx]
                data_idx = data_idx + 1
                x = x + 1
                if x >= w:
                    break
                idx = idx + 1
                
            if width - w  - padding_w > 0:
                # Fill with whites up to the end of the line
                data_idx = data_idx + width - w - padding_w
            
            y = y - 1
          
        return data    

    def decode(self, fdata:bytes, bmp_width: int, bmp_height: int,
               bmp_padding_w: int, bmp_padding_h: int,
               palette_name: str, palette_data: bytes) -> bytes:
    
        bmp_bpp = 8
        
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
        # RLE encoded bytes contains 1 pixel color
        w = bmp_width - bmp_padding_w
        
        # Must be an even number
        w_size = w + (w%2)
    
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
