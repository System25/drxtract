#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director CLUT files.
# 

import sys
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)


# ==============================================================================
def clut2json(clut_file):
    json = []
    
    with open(clut_file, mode='rb') as file:
        fdata = file.read()
        
        idx = 0
        while idx < len(fdata):
            r0 = fdata[idx]
            idx += 1
            r1 = fdata[idx]
            idx += 1
            g0 = fdata[idx]
            idx += 1
            g1 = fdata[idx]
            idx += 1            
            b0 = fdata[idx]
            idx += 1
            b1 = fdata[idx]
            idx += 1

            
            # Set colors in #RRGGBB format
            json.append('#%02x%02x%02x'%(r0, g0, b0))

    return json


# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: clut2json <work directory> <clut file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[1], sys.argv[2])))
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.CLUT'):
            logging.error(" '%s' does not end in '.CLUT'"%(sys.argv[3]))
            sys.exit(-1)
            
        # Get cast file data
        castData = {}
        with open(os.path.join(sys.argv[1], 'data.json'), encoding='utf-8') as json_file:
            text = json_file.read()
            castData = json.loads(text)

        palette = clut2json(os.path.join(sys.argv[1], sys.argv[2]))
        
        castData['palette'] = palette
        
        # Write CAST data with the palette to JSON file
        with open(os.path.join(sys.argv[1], 'data.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(castData, indent=4, sort_keys=True).encode('utf-8'))
