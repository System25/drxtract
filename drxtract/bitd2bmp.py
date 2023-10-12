#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director image files.
# 

import sys
import os
import struct
import logging
import json
from .palettes.grayscale import GRAYSCALE_256COLORS_PALETTE
from .palettes.metallic import METALLIC_256COLORS_PALETTE
from .palettes.ntsc import NTSC_256COLORS_PALETTE
from .palettes.pastels import PASTELS_256COLORS_PALETTE
from .palettes.rainbow import RAINBOW_256COLORS_PALETTE
from .palettes.systemMac import SYSTEM_MAC_256COLORS_PALETTE
from .palettes.systemWinDir4 import SYSTEM_WINDOWS_DIR4_256COLORS_PALETTE
from .palettes.systemWin import SYSTEM_WINDOWS_256COLORS_PALETTE
from .palettes.vivid import VIVID_256COLORS_PALETTE
from .palettes.web216 import WEB_256COLORS_PALETTE

logging.basicConfig(level=logging.DEBUG)


DIR5_IMAGE_TYPE = 1
DIR4_IMAGE_TYPE = 0x1C0000



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

# ====================================================================================================================================
def save_2bit_bmp(bmp_width, bmp_height, file, fdata, bmp_padding_w, bmp_padding_h):
    bmp_bpp = 8
    ncolors = 2
    
    # Sometimes the padding is negative
    if bmp_padding_h < 0:
        bmp_height = bmp_height - bmp_padding_h
        bmp_padding_h = 0 
    
    values = (bmp_width*bmp_height+(ncolors*4)+40+14, # The size of the BMP file in bytes
              0, # Reserved
              0, # Reserved
              ((ncolors*4)+40+14) # Data offset
             )
    s = struct.Struct('<ihhi')
    packed_data = s.pack(*values)
    file.write(packed_data)
    
    width = bmp_width
    if (width%4) > 0:
        # The image width must be divisible by four
        width = width + 4 - (width%4)
    
    # Write BITMAPINFOHEADER
    values = (40, # the size of this header (40 bytes)
              bmp_width, # the bitmap width in pixels (signed integer)
              bmp_height, # the bitmap height in pixels (signed integer)
              1, # the number of color planes (must be 1)
              bmp_bpp, # the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
              0, # the compression method being used
              0, # the image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
              0, # the horizontal resolution of the image. (pixel per meter, signed integer)
              0, # the vertical resolution of the image. (pixel per meter, signed integer)
              ncolors, # the number of colors in the color palette, or 0 to default to 2n
              ncolors  # the number of important colors used, or 0 when every color is important; generally ignored
             )
    s = struct.Struct('<iiihhiiiiii')
    packed_data = s.pack(*values)
    file.write(packed_data)

    # Write the black and white color palette
    s = struct.Struct('B'*(ncolors*4))
    packed_data = s.pack(*BW_PALETTE)   
    file.write(packed_data)

    # get the pixel information
    # RLE encoded bytes contains 1 pixel color
    w = bmp_width - bmp_padding_w

    w_size = int(w/8)
    if (w%8) > 0:
        w_size = w_size + 1
    # Must be an even number
    w_size = w_size + (w_size%2)  

    if len(fdata) == w_size*(bmp_height-bmp_padding_h):
        logging.info("The size of the data matches the image resolution. Not RLE compressed!")      
        # Write the pixel information
        white = '\0'
        y = bmp_height - 1 - bmp_padding_h
        idx = 0
        while y>=0:
            if bmp_padding_w > 0:
                file.write(bytearray(white * bmp_padding_w, 'ascii'))
            
            idx = (y * w_size)
            
            x = 0
            while x < w:
                for j in range(0, 8):
                    bitval = ((fdata[idx] >> (7-j)) & 1)                 
                    file.write(struct.pack('B', bitval))
                    x = x + 1
                    if x >= w:
                        break
                idx = idx + 1
                
            if width - bmp_width > 0:
                file.write(bytearray(white *(width - bmp_width), 'ascii'))
            
            y = y - 1
             
        for _ in range(0, bmp_padding_h):
            file.write(bytearray(white * width, 'ascii'))
          
        file.close()
        return    
    
    # w must be an even number in compressed images
    inc = (w%2)
    if bmp_width + inc > width:
        inc = 0
    w = w + inc    

    castData = [0 for x in range(width*bmp_height)]
    x = 0
    y = bmp_height - 1 - bmp_padding_h
    idx = 0
    while (idx < len(fdata)) and (y>=0):
        val = fdata[idx]
        if (val & 0x80) != 0:
            # RLE encoded
            run_length = 257 - val
            if idx+1 >= len(fdata):
                logging.error("Unexpected end of data! (data length=%s)"%(len(fdata)))
                break
            run_value = fdata[idx+1]
            idx = idx + 2

            if x + run_length > w:
                logging.error("Run too long! (%s, %s)"%(run_length, w-x))

            for _ in range(0, run_length):
                for j in range(0, 8):
                    bitval = ((run_value >> (7-j)) & 1)
                    if x >= w:
                        logging.error("Painting out of image (rle)! (x=%s y=%s col=%s)"%(x-1, y, bitval))
                        break

                    castData[y*width + x + bmp_padding_w] = bitval
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
                logging.error("Bad run length! (value=%s, available=%s)"%(run_length, len(fdata)-idx))
                break

            for _ in range(0, run_length):
                for j in range(0, 8):
                    bitval = ((fdata[idx] >> (7-j)) & 1)
                    if x >= w:
                        logging.error("Painting out of image (no-rle)! (x=%s y=%s col=%s)"%(x-1, y, bitval))
                        break
                    
                    castData[y*width + x + bmp_padding_w] = bitval
                    x += 1            

                idx = idx + 1
                if idx > len(fdata):
                    logging.error("Bad run length! (value=%s)"%(run_length))
                    break


            if x >= w:           
                x = 0
                y -= 1
                if y < 0:
                    break

    if y!=-1 or x!=0:
        logging.warning("Not enought data to decode. Probably the image is not properly generated. (y=%s, x=%s)"%(y, x))

    if idx != len(fdata):
        logging.warning("there is more data to decode. Probably the image is not properly generated. (%s != %s)"%(idx, len(fdata)))
        
    # Write the pixel information
    file.write(struct.pack("B"*(width*bmp_height), *castData))
    file.close()


# ====================================================================================================================================
def save_4bit_bmp(bmp_width, bmp_height, file, palette, previous_clut, fdata, bmp_padding_h):
    bmp_bpp = 4
    values = (bmp_width*bmp_height+(16*4)+40+14, # The size of the BMP file in bytes
              0, # Reserved
              0, # Reserved
              ((16*4)+40+14) # Data offset
             )
    s = struct.Struct('<ihhi')
    packed_data = s.pack(*values)
    file.write(packed_data)

    ncolors = 16

    width = bmp_width
    if (width%4) > 0:
        # The image width must be divisible by four
        width = width + 4 - (width%4)    
    
    # Write BITMAPINFOHEADER
    values = (40, # the size of this header (40 bytes)
              bmp_width, # the bitmap width in pixels (signed integer)
              bmp_height, # the bitmap height in pixels (signed integer)
              1, # the number of color planes (must be 1)
              bmp_bpp, # the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
              0, # the compression method being used
              0, # the image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
              0, # the horizontal resolution of the image. (pixel per meter, signed integer)
              0, # the vertical resolution of the image. (pixel per meter, signed integer)
              ncolors, # the number of colors in the color palette, or 0 to default to 2n
              ncolors  # the number of important colors used, or 0 when every color is important; generally ignored
             )
    s = struct.Struct('<iiihhiiiiii')
    packed_data = s.pack(*values)
    file.write(packed_data)

    # Write the color palette
    if previous_clut is not None:
        s = struct.Struct('B'*(ncolors*4))
        packed_data = s.pack(*previous_clut[0:(ncolors*4)])
        file.write(packed_data)

    else:
        # Use a standar color palette
        s = struct.Struct('B'*(ncolors*4))
        if palette == 'systemMac':
            packed_data = s.pack(*SYSTEM_MAC_16COLORS_PALETTE)
        elif palette == 'systemWin':
            packed_data = s.pack(*SYSTEM_WINDOWS_16COLORS_PALETTE)       
        else:
            logging.warn("Using default windows color palette!")
            packed_data = s.pack(*SYSTEM_WINDOWS_16COLORS_PALETTE)               
            
        file.write(packed_data)
        
        
    # get the pixel information
    w = bmp_width + (bmp_width%2)
    print("w: %s"%(w))  

    castData = [0 for _ in range(w*bmp_height)]
    x = 0
    y = bmp_height - 1 - bmp_padding_h
    idx = 0
    while (idx < len(fdata)) and (y>=0):
        val = fdata[idx]
        print("val=%s"%(val))        
        if (val & 0x80) != 0:
            # RLE encoded
            run_length = 257 - val
            print("RLE: run length: %s"%(run_length))            
            run_value = fdata[idx+1]
            print("RLE: run value: %s"%(run_value))            
            idx = idx + 2
            for _ in range(0, run_length):
                if x >= w:
                    logging.error("Painting out of image! (x=%s y=%s col=%s)"%(x-1, y, run_value))
                    break
                castData[y*w + x] = run_value
                x += 1
            
            if x >= w:
                x = 0
                y -= 1
                print("RLE: jump to next row!")                
            
            
        else:
            # Not RLE encoded
            run_length = (val + 1)
            print("NoRLE: run length: %s"%(run_length))            
            idx = idx + 1
            for _ in range(0, run_length):
                if x >= w:
                    logging.error("Painting out of image! (x=%s y=%s col=%s)"%(x-1, y, run_value))
                    break
                castData[y*w + x] = fdata[idx]
                idx = idx + 1
                x += 1
                if idx > len(fdata):
                    logging.error("Bad run length! (value=%s)"%(run_length))
                    break
                    
            if x >= w:
                x = 0
                y -= 1
                print("NoRLE: jump to next row!") 

    if y!=-1 or x!=0:
        logging.warn("Not enought data to decode. Probably the image is not properly generated. (y=%s, x=%s)"%(y, x))

    if idx != len(fdata):
        logging.warn("there is more data to decode. Probably the image is not properly generated. (%s != %s)"%(idx, len(fdata)))

    # RLE encoded bytes contains 2 pixel colors
    ow = int(bmp_width/2) + (bmp_width%2)
    outData = [0 for x in range(ow*bmp_height)]
    for y in range(bmp_height):
        for x in range(ow):
            val = (castData[y*w + x*2] << 4)
            outData = val
        
    # Write the pixel information
    file.write(struct.pack("B"*(bmp_width*bmp_height), *outData))
    file.close()

# ====================================================================================================================================
def save_8bit_bmp(bmp_width, bmp_height, file, palette, previous_clut, fdata, bmp_padding_w, bmp_padding_h):
    bmp_bpp = 8
    values = (bmp_width*bmp_height+(256*4)+40+14, # The size of the BMP file in bytes
              0, # Reserved
              0, # Reserved
              ((256*4)+40+14) # Data offset
             )
    s = struct.Struct('<ihhi')
    packed_data = s.pack(*values)
    file.write(packed_data)

    ncolors = 256

    width = bmp_width
    if (width%4) > 0:
        # The image width must be divisible by four
        width = width + 4 - (width%4)
    
    # Write BITMAPINFOHEADER
    values = (40, # the size of this header (40 bytes)
              bmp_width, # the bitmap width in pixels (signed integer)
              bmp_height, # the bitmap height in pixels (signed integer)
              1, # the number of color planes (must be 1)
              bmp_bpp, # the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
              0, # the compression method being used
              0, # the image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
              0, # the horizontal resolution of the image. (pixel per meter, signed integer)
              0, # the vertical resolution of the image. (pixel per meter, signed integer)
              ncolors, # the number of colors in the color palette, or 0 to default to 2n
              ncolors  # the number of important colors used, or 0 when every color is important; generally ignored
             )
    s = struct.Struct('<iiihhiiiiii')
    packed_data = s.pack(*values)
    file.write(packed_data)

    # Write the color palette
    if previous_clut is not None:
        s = struct.Struct('B'*(256*4))
        packed_data = s.pack(*previous_clut)
        file.write(packed_data)

    else:
        # Load a standar color palette from a file
        s = struct.Struct('B'*(256*4))
        if palette == 'grayscale':
            packed_data = s.pack(*GRAYSCALE_256COLORS_PALETTE)
        elif palette == 'metallic':
            packed_data = s.pack(*METALLIC_256COLORS_PALETTE)
        elif palette == 'ntsc':
            packed_data = s.pack(*NTSC_256COLORS_PALETTE)
        elif palette == 'pastels':
            packed_data = s.pack(*PASTELS_256COLORS_PALETTE)
        elif palette == 'rainbow':
            packed_data = s.pack(*RAINBOW_256COLORS_PALETTE)
        elif palette == 'systemMac':
            packed_data = s.pack(*SYSTEM_MAC_256COLORS_PALETTE)
        elif palette == 'systemWinDir4':
            packed_data = s.pack(*SYSTEM_WINDOWS_DIR4_256COLORS_PALETTE)
        elif palette == 'systemWin':
            packed_data = s.pack(*SYSTEM_WINDOWS_256COLORS_PALETTE)
        elif palette == 'vivid':
            packed_data = s.pack(*VIVID_256COLORS_PALETTE)          
        elif palette == 'web216':
            packed_data = s.pack(*WEB_256COLORS_PALETTE)           
        else:
            logging.warn("Using default windows color palette!")
            packed_data = s.pack(*SYSTEM_WINDOWS_256COLORS_PALETTE)   
        file.write(packed_data)

    # get the pixel information
    # RLE encoded bytes contains 1 pixel color
    w = bmp_width - bmp_padding_w
    inc = (w%2)
    w = w + inc

    if len(fdata) == w*(bmp_height-bmp_padding_h):
        logging.info("The size of the data matches the image resolution. Not RLE compressed!")
        # Write the pixel information
        white = '\0'
        y = bmp_height - 1 - bmp_padding_h
        while y>=0:
            if bmp_padding_w > 0:
                file.write(bytearray(white * bmp_padding_w, 'ascii'))
            idx = y*w
            file.write(fdata[idx:(idx+w)])
            y -= 1
            if width - bmp_width - inc > 0:
                file.write(bytearray(white *(width - bmp_width - inc), 'ascii'))
            
        for _ in range(0, bmp_padding_h):
            file.write(bytearray(white * width, 'ascii'))
          
        file.close()
        return


    castData = [0 for _ in range(width*bmp_height)]
    x = 0
    y = bmp_height - 1 - bmp_padding_h
    idx = 0
    logging.debug("w=%s h=%s"%(w, bmp_height-bmp_padding_h))
    while (idx < len(fdata)) and (y>=0):
        val = fdata[idx]
        if (val & 0x80) != 0:
            # RLE encoded
            run_length = 257 - val
            if idx+1 >= len(fdata):
                logging.error("Unexpected end of data! (data length=%s)"%(len(fdata)))
                break
            run_value = fdata[idx+1]
            idx = idx + 2

            if x + run_length > w:
                logging.error("Run too long! (%s, %s)"%(run_length, w-x))

            for _ in range(0, run_length):
                if x >= w:
                    logging.error("Painting out of image! (x=%s y=%s col=%s)"%(x-1, y, run_value))
                    break
                 
                castData[y*width + x + bmp_padding_w] = run_value
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
                logging.error("Bad run length! (value=%s, available=%s)"%(run_length, len(fdata)-idx))
                break

            for _ in range(0, run_length):
                if x >= w:
                    logging.error("Painting out of image! (x=%s y=%s col=%s)"%(x-1, y, fdata[idx-1]))
                    break

                castData[y*width + x + bmp_padding_w] = fdata[idx]
                  
                idx = idx + 1
                if idx > len(fdata):
                    logging.error("Bad run length! (value=%s)"%(run_length))
                    break

                x += 1            

            if x >= w:           
                x = 0
                y -= 1
                if y < 0:
                    break

    if y!=-1 or x!=0:
        logging.warning("Not enought data to decode. Probably the image is not properly generated. (y=%s, x=%s)"%(y, x))

    if idx != len(fdata):
        logging.warning("there is more data to decode. Probably the image is not properly generated. (%s != %s)"%(idx, len(fdata)))
        
    # Write the pixel information
    file.write(struct.pack("B"*(width*bmp_height), *castData))
    file.close()

# ====================================================================================================================================
def save_16bit_bmp(bmp_width, bmp_height, file, fdata):
    bmp_bpp = 16
    hsize = 124
    values = (bmp_width*bmp_height*2+hsize+14, # The size of the BMP file in bytes
              0, # Reserved
              0, # Reserved
              (hsize+14) # Data offset
             )
    s = struct.Struct('<ihhi')
    packed_data = s.pack(*values)
    file.write(packed_data)

    # Write BITMAPINFOHEADER
    values = (hsize, # the size of this header (hsize bytes)
              bmp_width, # the bitmap width in pixels (signed integer)
              bmp_height, # the bitmap height in pixels (signed integer)
              1, # the number of color planes (must be 1)
              bmp_bpp, # the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
              3, # the compression method being used (BI_BITFIELDS)
              0, # the image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
              0, # the horizontal resolution of the image. (pixel per meter, signed integer)
              0, # the vertical resolution of the image. (pixel per meter, signed integer)
              0, # the number of colors in the color palette, or 0 to default to 2n
              0, # the number of important colors used, or 0 when every color is important; generally ignored
              0x00007C00, # Red channel bitmask
              0x000003E0, # Green channel bitmask
              0x0000001F, # Blue channel bitmask
              0x00000000, # Alpha channel bitmask
              0x73524742, # "BGRs"
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, # CIEXYZTRIPLE Color Space endpoints
              0, # Red Gamma
              0, # Green Gamma
              0, # Blue Gamma
             )
    s = struct.Struct('<iiihhIIIIIIIIIIIIIIIIIIIIIIIIIII')
    packed_data = s.pack(*values)
    file.write(packed_data)

    # get the pixel information
    # RLE encoded bytes are:
    #   - RLE encoded lower byte
    #   - RLE encoded upper byte

    w = bmp_width*2
    h = bmp_height

    castData = [0 for _ in range(w*bmp_height)]
    x = 0
    y = bmp_height - 1
    idx = 0
    while (idx < len(fdata)) and (y>=0):
        val = struct.unpack("B", fdata[idx])[0]
        if (val & 0x80) != 0:
            # RLE encoded
            run_length = 257 - val
            run_value = struct.unpack("B", fdata[idx+1])[0]
            idx = idx + 2

            # Jump to next byte when necessary
            if ((x + run_length) > bmp_width) and (x < bmp_width):
                x = bmp_width

            # Jump to next row when necessary
            if ((x + run_length) > w):
                x = 0
                y -= 1

            for _ in range(0, run_length):
                castData[y*w + x] = run_value
                x += 1
            

        else:
            # Not RLE encoded
            run_length = val + 1
            idx = idx + 1

            # Jump to next byte when necessary
            if ((x + run_length) > bmp_width) and (x < bmp_width):
                x = bmp_width

            # Jump to next row when necessary
            if ((x + run_length) > w):
                x = 0
                y -= 1

            for _ in range(0, run_length):
                castData[y*w + x] = struct.unpack("B", fdata[idx])[0]
                idx = idx + 1
                x += 1
                if x >= w:
                    x = 0
                    y -= 1

    if y!=0 or x!=w:
        logging.warn("Not enought data to decode. Probably the image is not properly generated. (y=%s, x=%s)"%(y, x))

    if idx != len(fdata):
        logging.warn("there is more data to decode. Probably the image is not properly generated. (%s != %s)"%(idx, len(fdata)))


    # Order lower and upper bytes
    castDatamix = [0 for x in range(bmp_width*2*bmp_height)]
    w2 = bmp_width*2
    w1 = bmp_width
    w0 = 0
    for y in range(0, bmp_height):
        yw1 = y*w1
        yw2 = y*w2
        for x in range(0, bmp_width):
            castDatamix[yw2 + x*2 + 0] = castData[yw2 + w1 + x]  # Upper
            castDatamix[yw2 + x*2 + 1] = castData[yw2 + w0 + x]  # Lower

    # Write the pixel information
    file.write(struct.pack("B"*(bmp_width*2*bmp_height), *castDatamix))
    file.close()

# ====================================================================================================================================
def save_24bit_bmp(bmp_width, bmp_height, file, fdata):
    bmp_bpp = 24
    values = (bmp_width*bmp_height*3+40+14, # The size of the BMP file in bytes
              0, # Reserved
              0, # Reserved
              (40+14) # Data offset
             )
    s = struct.Struct('<ihhi')
    packed_data = s.pack(*values)
    file.write(packed_data)

    ncolors = 0

    # Write BITMAPINFOHEADER
    values = (40, # the size of this header (40 bytes)
              bmp_width, # the bitmap width in pixels (signed integer)
              bmp_height, # the bitmap height in pixels (signed integer)
              1, # the number of color planes (must be 1)
              bmp_bpp, # the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
              0, # the compression method being used
              0, # the image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
              0, # the horizontal resolution of the image. (pixel per meter, signed integer)
              0, # the vertical resolution of the image. (pixel per meter, signed integer)
              ncolors, # the number of colors in the color palette, or 0 to default to 2n
              ncolors  # the number of important colors used, or 0 when every color is important; generally ignored
             )
    s = struct.Struct('<iiihhiiiiii')
    packed_data = s.pack(*values)
    file.write(packed_data)

    # get the pixel information
    # RLE encoded bytes are:
    #   - RLE encoded Alpha channel for 1 row
    #   - RLE encoded Blue channel for 1 row
    #   - RLE encoded Green channel for 1 row
    #   - RLE encoded Red channel for 1 row

    w = bmp_width*4
    h = bmp_height

    castData = [0 for _ in range(w*bmp_height)]
    x = 0
    y = bmp_height - 1
    idx = 0
    while (idx < len(fdata)) and (y>=0):
        val = struct.unpack("B", fdata[idx])[0]
        if (val & 0x80) != 0:
            # RLE encoded
            run_length = 257 - val
            run_value = struct.unpack("B", fdata[idx+1])[0]
            idx = idx + 2
            for _ in range(0, run_length):
                castData[y*w + x] = run_value
                x += 1
                if x >= w:
                    x = 0
                    y -= 1
            

        elif val != 0:
            # Not RLE encoded
            run_length = val + 1
            idx = idx + 1
            for _ in range(0, run_length):
                castData[y*w + x] = struct.unpack("B", fdata[idx])[0]
                idx = idx + 1
                x += 1
                if x >= w:
                    x = 0
                    y -= 1

        else: # val is zero
            run_value = struct.unpack("B", fdata[idx+1])[0]
            idx = idx + 2
            castData[y*w + x] = run_value
            x += 1
            if x >= w:
                x = 0
                y -= 1

    if y!=-1 or x!=0:
        logging.warn("Not enought data to decode. Probably the image is not properly generated. (y=%s, x=%s)"%(y, x))

    if idx != len(fdata):
        logging.warn("there is more data to decode. Probably the image is not properly generated. (%s != %s)"%(idx, len(fdata)))


    # Order RGB bytes and discard Alpha channel
    castDatamix = [0 for x in range(bmp_width*3*bmp_height)]
    w4 = bmp_width*4
    w3 = bmp_width*3
    w2 = bmp_width*2
    w1 = bmp_width
    w0 = 0
    for y in range(0, bmp_height):
        yw4 = y*w4
        yw3 = y*w3
        for x in range(0, bmp_width):
            castDatamix[yw3 + x*3 + 0] = castData[yw4 + w3 + x]  # Red
            castDatamix[yw3 + x*3 + 1] = castData[yw4 + w2 + x]  # Green
            castDatamix[yw3 + x*3 + 2] = castData[yw4 + w1 + x]  # Blue

    # Write the pixel information
    file.write(struct.pack("B"*(bmp_width*3*bmp_height), *castDatamix))
    file.close()



# ====================================================================================================================================
def bitd2bmp(castData, bitd_file):
    clutData = None
    
    with open(bitd_file, mode='rb') as file:
        fdata = file.read()
        
        file_ext = 'bmp'

        bmp_height = castData['height']
        bmp_width = castData['width']
        bmp_bpp = castData['depth']
        bmp_padding_w = castData['w_padding']
        bmp_padding_h = castData['h_padding']
        if bmp_bpp == 8:
            bmp_palette = castData['palette_txt']
        elif bmp_bpp == 2:
            bmp_palette = 'black and white'          
        else:
            bmp_palette = 'none'

        file_name = "%s.%s"%(os.path.basename(bitd_file)[:-5], file_ext)

        # Check if the palette is a casting member number (custom palette)
        if type(bmp_palette) == int:
            bmp_palette = str(bmp_palette)
            
            # Check if the cast member exists
            base_dir = os.path.dirname(sys.argv[1])
            if not os.path.isdir(os.path.join(base_dir, bmp_palette)):
                logging.error('Can\'t find cast member: %s'%(bmp_palette))
                sys.exit(-1)
            
            # Check if there is any CLUT file in the directory
            clut_dir = os.path.join(base_dir, bmp_palette)
            clut_file = None
            for file in os.listdir(clut_dir):
                if file.endswith(".CLUT"):
                    clut_file = file
                    break
            
            if not clut_file:
                logging.error('Can\'t find any CLUT file in cast member: %s'%(bmp_palette))
                sys.exit(-1)            
            
            with open(os.path.join(clut_dir, clut_file), mode='rb') as cfile:
                cData = cfile.read()
                clutData = [0] * (256*4)
                indx = 0
                cindx = 0
                for _ in range(0, 256):
                    # The same color in RGB - BRG form
                    r0 = cData[indx]
                    indx += 1
                    g0 = cData[indx]
                    indx += 1
                    b0 = cData[indx]
                    indx += 1
                    
                    b1 = cData[indx]
                    indx += 1
                    g1 = cData[indx]
                    indx += 1
                    r1 = cData[indx]
                    indx += 1
                    
                    clutData[cindx] = b1
                    cindx += 1
                    clutData[cindx] = g1
                    cindx += 1
                    clutData[cindx] = r1
                    cindx += 1
                    clutData[cindx] = 0  # Alpha
                    cindx += 1
           
            logging.debug('Using a custom palette: %s'%(bmp_palette))
            
        else:
            logging.debug('Using a default palette: %s'%(bmp_palette))

        try:
            logging.info(u"Saving file content to: %s"%(file_name))
        except:
            file_name = file_namer
            logging.info(u"Saving file content to: %s"%(file_name))


        with open(os.path.join(sys.argv[1], file_name), 'wb') as file:
            # Write Windows bitmap file header
            file.write('BM'.encode('ascii'))

            if bmp_bpp == 2:
                # 2 bits per pixel image (black and white)
                save_2bit_bmp(bmp_width, bmp_height, file, fdata, bmp_padding_w, bmp_padding_h)
                
            elif bmp_bpp == 4:
                # 4 bits per pixel image
                save_4bit_bmp(bmp_width, bmp_height, file, bmp_palette, clutData, fdata, bmp_padding_h)

            elif bmp_bpp == 8:
                # 8 bits per pixel image
                save_8bit_bmp(bmp_width, bmp_height, file, bmp_palette, clutData, fdata, bmp_padding_w, bmp_padding_h)

            elif bmp_bpp == 16:
                # 16 bits per pixel image
                save_16bit_bmp(bmp_width, bmp_height, file, fdata)

            elif bmp_bpp == 24:
                # 24 bits per pixel image
                save_24bit_bmp(bmp_width, bmp_height, file, fdata)

            else:
                logging.error("Bad BPP value (%s)"%(bmp_bpp))
                sys.exit(-1)


# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: bitd2bmp <work directory> <bitd file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[1], sys.argv[2])))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], 'data.json')):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[1], 'data.json')))
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.BITD'):
            logging.error(" '%s' does not end in .BITD"%(sys.argv[2]))
            sys.exit(-1)
            
        # Get cast file data
        json_data = None
        with open(os.path.join(sys.argv[1], 'data.json'), encoding='utf-8') as json_file:
            text = json_file.read()
            json_data = json.loads(text)
        
        # Generate BMP image
        bitd_file = os.path.join(sys.argv[1], sys.argv[2])
        bitd2bmp(json_data, bitd_file)
        
        # Use ImageMagick to remove the background
        inp_name = os.path.join(sys.argv[1], "%s.%s"%(os.path.basename(bitd_file)[:-5], 'bmp'))
        tmp_name = os.path.join(sys.argv[1], "%s.%s"%(os.path.basename(bitd_file)[:-5], 'tmp.png'))
        out_name = os.path.join(sys.argv[1], "%s.%s"%(os.path.basename(bitd_file)[:-5], 'png'))
        command = '-alpha off -bordercolor white -border 1 \\( +clone -fill none -floodfill +0+0 white '\
                  '-alpha extract \\) '\
                  '-compose CopyOpacity -composite -shave 1'
        os.system('convert %s %s %s'%(
            inp_name, # input file
            command, # command
            tmp_name #output file
        ))
        
        # Crop the image
        bmp_height = json_data['height']
        bmp_width = json_data['width']
        bmp_padding_w = json_data['w_padding']
        bmp_padding_h = json_data['h_padding']
        w = bmp_width
        h = bmp_height
        pw = bmp_padding_w
        ph = bmp_padding_h
        if ph < 0:
            h = h - bmp_padding_h
            ph = 0
        
        command = '-crop %sx%s+%s+%s'%(w, h, pw, ph)
        os.system('convert %s %s %s'%(
            tmp_name, # input file
            command, # command
            out_name #output file
        ))
