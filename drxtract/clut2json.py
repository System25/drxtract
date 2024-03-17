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
from .clut import clut2rgb

logging.basicConfig(level=logging.DEBUG)


# ==============================================================================
def clut2json(clut_file):
    
    with open(clut_file, mode='rb') as file:
        fdata = file.read()
        
        return clut2rgb(fdata)

    return []


# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: clut2json <work directory> <clut file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        clut_file = os.path.join(sys.argv[1], sys.argv[2])
        if not os.path.isfile(clut_file):
            logging.error(" '%s' is not a file", clut_file)
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.CLUT'):
            logging.error(" '%s' does not end in '.CLUT'", sys.argv[3])
            sys.exit(-1)
            
        # Get cast file data
        castData = {}
        with open(os.path.join(sys.argv[1], 'data.json'),
                  encoding='utf-8') as json_file:
            text = json_file.read()
            castData = json.loads(text)

        palette = clut2json(clut_file)
        
        castData['palette'] = palette
        
        # Write CAST data with the palette to JSON file
        with open(os.path.join(sys.argv[1], 'data.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(castData, indent=4, sort_keys=True
                                    ).encode('utf-8'))

        
if __name__ == '__main__':
    main()
