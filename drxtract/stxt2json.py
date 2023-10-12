#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director string files.
# 

import sys
import os
import struct
import logging
import json

logging.basicConfig(level=logging.DEBUG)


# Default bit order for MAC
bit_order_type = 'mac'
bit_order = ">"


# ==============================================================================
def stxt2json(castData, fontmap, stxt_file):
    txt_data = None
    logging.debug("bit_order_type = %s"%(bit_order_type))
    
    with open(stxt_file, mode='rb') as file:
        fdata = file.read()
        
        idx = 0

        # Read STXT file header
        idxb = struct.unpack(bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4
        logging.debug("base index = %08x"%(idxb))

        nchars =  struct.unpack(bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4
        logging.debug("number of characters: %d"%(nchars))

        font_data_size =  struct.unpack(bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4
        logging.debug("font_data_size = %08x"%(font_data_size))
        
        
        txt_data = fdata[idxb:idxb+nchars].decode('ISO-8859-1')
        idx = idxb+nchars
        

        txt_format = []
        nformat_info =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2
        logging.debug("nformat_info = %s"%(nformat_info))
        for i in range(nformat_info):
            unknown2 =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown2 = %s"%(unknown2))             
            
            start =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            logging.debug("start = %s"%(start))             
            
            unknown4 =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown4 = %s"%(unknown4))             
            
            unknown5 =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown5 = %s"%(unknown5))            
            
            font_family =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            
            for font in fontmap:
                if font['id'] == font_family:
                    font_family = font['name']

            logging.debug("font_family = %s"%(font_family))                    
                    
            font_format =  int(fdata[idx])
            idx += 1
            logging.debug("font_format = %s"%(font_format))
            
            bold = False
            italic = False
            underline = False
            if (font_format & 1) != 0:
                bold = True

            if (font_format & 2) != 0:
                italic = True        
                
            if (font_format & 4) != 0:
                underline = True               
                
            unknown7 =  int(fdata[idx])
            idx += 1    
            logging.debug("unknown7 = %s"%(unknown7))
            
            font_size =  struct.unpack(bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            logging.debug("font_size = %s"%(font_size))
            
            fg_color_red =  int(fdata[idx])
            idx += 1    
            logging.debug("fg_color_red = %s"%(fg_color_red))            
            
            unknown9 =  int(fdata[idx])
            idx += 1    
            logging.debug("unknown9 = %s"%(unknown9))
            
            fg_color_green =  int(fdata[idx])
            idx += 1    
            logging.debug("fg_color_green = %s"%(fg_color_green))            
            
            unknown10 =  int(fdata[idx])
            idx += 1    
            logging.debug("unknown10 = %s"%(unknown10))
            
            fg_color_blue =  int(fdata[idx])
            idx += 1    
            logging.debug("fg_color_blue = %s"%(fg_color_blue))            
            
            unknown11 =  int(fdata[idx])
            idx += 1    
            logging.debug("unknown11 = %s"%(unknown11))              
            
            tformat = {}
            tformat['color'] = '#%0.2X%0.2X%0.2X'%(
                fg_color_red, fg_color_green, fg_color_blue)
            tformat['start'] = start
            tformat['bold'] = bold
            tformat['italic'] = italic
            tformat['underline'] = underline
            tformat['font_size'] = font_size
            tformat['font_family'] = font_family
            
            txt_format.append(tformat)
            
        castData['text'] = txt_data
        castData['txt_format'] = txt_format

        # Write CAST data to JSON file
        dest_dir = os.path.dirname(stxt_file)        
        with open(os.path.join(dest_dir, 'data.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(castData, indent=4, sort_keys=True).encode('utf-8'))



# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: stxt2json <work directory> <stxt file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[1], sys.argv[2])))
            sys.exit(-1)

        if not sys.argv[2].endswith('.STXT'):
            logging.error(" '%s' does not end in '.STXT'"%(sys.argv[2]))
            sys.exit(-1)

        # Get the font map
        fontmap = []
        fontfile = os.path.join(os.path.dirname(os.path.dirname(sys.argv[1])), 'fonts.json')
        if os.path.isfile(fontfile):
            with open(fontfile, mode='r', encoding='utf-8') as file:
                text = file.read()
                fontmap = json.loads(text)
        else:
            logging.warn("Fonts map not found in: %s"%(fontfile))
            
            
        # Get cast file data
        castData = {}
        with open(os.path.join(sys.argv[1], 'data.json'), mode='r', encoding='utf-8') as file:
            text = file.read()
            castData = json.loads(text)

        stxt2json(castData, fontmap, os.path.join(sys.argv[1], sys.argv[2]))
        