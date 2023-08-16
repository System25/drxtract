#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director Fmap files.
# Fmap files contains information about the fonts used in the file.
# 

import sys
import os
import struct
import logging
import json

BINDIR = 'bin'

logging.basicConfig(level=logging.DEBUG)

bit_order = '>'

# ==============================================================================
# Reads from Fmap file the fonts information
def parse_fmap_file(fmap_file):
    fmap_data = []
    
    with open(fmap_file, mode='rb') as file:
        fdata = file.read()

        idx = 0

        header_size = struct.unpack(bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4
        logging.debug("header_size = %04x"%(header_size))
            
        additional_size = struct.unpack(bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4
        logging.debug("additional_size = %08x"%(additional_size))

        if 8 + header_size + additional_size != len(fdata):
            logging.error("Bad data size! (%d != %d)"%(8 + header_size + additional_size, len(fdata)))
            sys.exit(-1)
 
        header_data = fdata[idx:idx + header_size]
        idx += header_size

        basic_data = fdata[idx:idx + additional_size]
        idx += additional_size
            
        # Parse header data
        idx = 0
        unknown01 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown01 = %s"%(unknown01))         

        unknown02 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown02 = %s"%(unknown02))         
        
        unknown03 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown03 = %s"%(unknown03))         

        unknown04 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown04 = %s"%(unknown04))                
        
        nfonts =  struct.unpack(bit_order+"i", header_data[idx:idx+4])[0]
        idx += 4
        logging.debug("Number of fonts = %s"%(nfonts))        
        
        nfonts_cap =  struct.unpack(bit_order+"i", header_data[idx:idx+4])[0]
        idx += 4
        logging.debug("Number of fonts (including non used ones) = %s"%(nfonts_cap))         
        
        unknown5 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown5 = %s"%(unknown5))         
        
        font_meta_size =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("Font metadata size = %s"%(font_meta_size))          
        
        unknown6 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown6 = %s"%(unknown6))  
        
        unknown7 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown7 = %s"%(unknown7))  
        
        unknown8 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown8 = %s"%(unknown8))  
        
        unknown9 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown9 = %s"%(unknown9))  
        
        metadata = []
        for i in range(nfonts_cap):
            logging.debug("--------------------------")             
            displacement =  struct.unpack(bit_order+"i", header_data[idx:idx+4])[0]
            idx += 4
            logging.debug("displacement = %s"%(displacement))             
        
            unknown00 =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown00 = %s"%(unknown00))          
        
            font_id =  struct.unpack(bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("font_id = %s"%(font_id))  
            
            data = {}
            data['displacement'] = displacement
            data['font_id'] = font_id
            
            metadata.append(data)
            
            
            
        logging.debug("--------------------------")
        
        # Parse font data
        for i in range(nfonts):
            logging.debug("--------------------------")        
            idx = metadata[i]['displacement']
            nchars =  struct.unpack(bit_order+"i", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("nchars = %s"%(nchars))   
            
            font_name = basic_data[idx:idx+nchars].decode('ISO-8859-1')
            idx = idx+nchars       
            logging.debug("font_name = %s"%(font_name))
            
            data = {}
            data['id'] = metadata[i]['font_id']
            data['name'] = font_name
            fmap_data.append(data)
            
        logging.debug("--------------------------")        
        
        
    return fmap_data

# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("USAGE: fmapxtract <work directory>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        fmap_file = None
        
        for f in os.listdir(os.path.join(sys.argv[1], BINDIR)):
            if f.endswith('Fmap'):
                fmap_file = f
                break
        
        if fmap_file is None:
            logging.error('Can not find a Fmap file!')
            sys.exit(-1)
        
        fmap_elements = parse_fmap_file(os.path.join(sys.argv[1], BINDIR, fmap_file))
        # Write font map data to JSON file
        with open(os.path.join(sys.argv[1], 'fonts.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(fmap_elements, indent=4, sort_keys=True).encode('utf-8'))

