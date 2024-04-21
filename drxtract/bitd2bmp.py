#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director image files.
# 

import sys
import os
import logging
import json
from .bitd import bitd2bmp
from .clut import clut2palette

logging.basicConfig(level=logging.DEBUG)




# ==============================================================================
def bitd_file2bmp(castData, bitd_file):
    clutData = bytearray()
    
    with open(bitd_file, mode='rb') as file:
        fdata = file.read()
        
        file_ext = 'bmp'

        bmp_bpp = castData['depth']
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
                logging.error('Can\'t find cast member: %s', bmp_palette)
                sys.exit(-1)
            
            # Check if there is any CLUT file in the directory
            clut_dir = os.path.join(base_dir, bmp_palette)
            clut_file = None
            for file in os.listdir(clut_dir):
                if file.endswith(".CLUT"):
                    clut_file = file
                    break
            
            if not clut_file:
                logging.error('Can\'t find any CLUT file in cast member: %s',
                              bmp_palette)
                sys.exit(-1)            
            
            with open(os.path.join(clut_dir, clut_file), mode='rb') as cfile:
                cData = cfile.read()
                clutData = clut2palette(cData)
           
            logging.debug('Using a custom palette: %s', bmp_palette)
            
        else:
            logging.debug('Using a default palette: %s', bmp_palette)

        logging.info(u"Saving file content to: %s", file_name)


        bmp = bitd2bmp(castData, clutData, fdata)
        with open(os.path.join(sys.argv[1], file_name), 'wb') as file:
            file.write(bmp)

# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: bitd2bmp <work directory> <bitd file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file",os.path.join(sys.argv[1],
                                                              sys.argv[2]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], 'data.json')):
            logging.error(" '%s' is not a file", os.path.join(sys.argv[1],
                                                              'data.json'))
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.BITD'):
            logging.error(" '%s' does not end in .BITD"%(sys.argv[2]))
            sys.exit(-1)
            
        # Get cast file data
        json_data = None
        with open(os.path.join(sys.argv[1], 'data.json'),
                  encoding='utf-8') as json_file:
            text = json_file.read()
            json_data = json.loads(text)
        
        # Generate BMP image
        bitd_file = os.path.join(sys.argv[1], sys.argv[2])
        bitd_file2bmp(json_data, bitd_file)
        
        # Use ImageMagick to remove the background
        basename = os.path.basename(bitd_file)[:-5]
        inp_name = os.path.join(sys.argv[1], "%s.%s"%(basename, 'bmp'))
        tmp_name = os.path.join(sys.argv[1], "%s.%s"%(basename, 'tmp.png'))
        out_name = os.path.join(sys.argv[1], "%s.%s"%(basename, 'png'))
        command = '-alpha off -bordercolor white -border 1 \\( +clone -fill '\
                  'none -floodfill +0+0 white '\
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
        
if __name__ == '__main__':
    main()

