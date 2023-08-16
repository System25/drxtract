#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director RTE bimap files.
# 

import sys
import os
import struct
import logging


logging.basicConfig(level=logging.DEBUG)


# Default bit order for MAC
bit_order_type = 'mac'
bit_order = ">"

DIR5_IMAGE_TYPE = 1
DIR4_IMAGE_TYPE = 0x1C0000

# ============================================ Default color palettes ================================================================

BW_PALETTE = (
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  0, 0, 0, 0,       # black
  255, 255, 255, 0 # white
 )




# ====================================================================================================================================
def save_4bit_bmp(bmp_width, bmp_height, file, fdata, bmp_padding_h):
    bmp_bpp = 8
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

    # Use a black and white color palette
    s = struct.Struct('B'*(ncolors*4))
    packed_data = s.pack(*BW_PALETTE)


    file.write(packed_data)
        
        
    # get the pixels information
    castData = [0xF for x in range(width*bmp_height)]
    x = 0
    y = bmp_height - 1 - bmp_padding_h
    idx = 0
    while (idx < len(fdata)) and (y>=0):
        # RLE encoded
        run_length = int(fdata[idx])
        idx = idx + 1
        if idx >= len(fdata):
          break
        run_value = int(fdata[idx])          
        idx = idx + 1
        
        if run_length == 0:
            x = 0
            y -= 1     
            continue
        
        
        for i in range(0, run_length):
            if x >= width:
                logging.error("Painting out of image! (x=%s y=%s col=%s)"%(x-1, y, run_value))
                break
            castData[y*width + x] = run_value
            x += 1

        if x >= width:
            x = 0
            y -= 1

    if idx != len(fdata):
        logging.warn("there is more data to decode. Probably the image is not properly generated. (%s != %s)"%(idx, len(fdata)))
        
    # Write the pixel information
    file.write(struct.pack("B"*(width*bmp_height), *castData))
    file.close()



# ====================================================================================================================================
def rte22bmp(rte2_file):
    
    with open(rte2_file, mode='rb') as file:
        fdata = file.read()
        
        file_ext = 'bmp'

        idx = 0
        width =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2                
        logging.debug("width = %s"%(width))         

        height =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2                
        logging.debug("height = %s"%(height))       
        
        unknown0 = int(fdata[idx])
        idx += 1                
        logging.debug("unknown0 = %s"%(unknown0)) 
        
        bpp = int(fdata[idx])
        idx += 1                
        logging.debug("bpp = %s"%(bpp))         
                
        unknown1 = int(fdata[idx])
        idx += 1                
        logging.debug("unknown1 = %s"%(unknown1)) 
        
        fdata = fdata[idx:]
        
        padding_w = 0
        padding_h = 0
        
        file_name = "%s.%s"%(os.path.basename(rte2_file)[:-5], file_ext)

        with open(os.path.join(sys.argv[1], file_name), 'wb') as file:
            # Write Windows bitmap file header
            file.write('BM'.encode('ascii'))
                
            # 4 bits per pixel image
            save_4bit_bmp(width, height, file, fdata, padding_h)



# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: rte22bmp <work directory> <rte2 file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[1], sys.argv[2])))
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.RTE2'):
            logging.error(" '%s' does not end in .RTE2"%(sys.argv[2]))
            sys.exit(-1)
        
        # Generate BMP image
        rte2_file = os.path.join(sys.argv[1], sys.argv[2])
        rte22bmp(rte2_file)
        
        # Use ImageMagick to remove the background
        inp_name = os.path.join(sys.argv[1], "%s.%s"%(os.path.basename(rte2_file)[:-5], 'bmp'))
        out_name = os.path.join(sys.argv[1], "%s.%s"%(os.path.basename(rte2_file)[:-5], 'png'))
        command = '-transparent white'
        os.system('convert %s %s %s'%(
            inp_name, # input file
            command, # command
            out_name #output file
        ))
        