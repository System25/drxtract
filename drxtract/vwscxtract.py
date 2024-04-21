#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director VWSC files.
# VWLB files contains the score.
# 

import sys
import os
import logging
import json
from .vwsc import parse_vwsc_file_data, vwsc_to_score

BINDIR = 'bin'

DEBUG_MAIN_CHANNEL_INFO = False
DEBUG_PALETTE_CHANNEL_INFO = False
DEBUG_SPRITE_INFO = True

#logging.basicConfig(level=logging.DEBUG)

# ==============================================================================
# Reads from VWSC file the score elements
def parse_vwsc_file(vwsc_file):    
    with open(vwsc_file, mode='rb') as file:
        fdata = file.read()
        return parse_vwsc_file_data(fdata)


# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("USAGE: vwscxtract <work directory>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        vwsc_file = None
        
        for f in os.listdir(os.path.join(sys.argv[1], BINDIR)):
            if f.endswith('VWSC'):
                vwsc_file = f
                break
        
        if vwsc_file is None:
            logging.error('Can not find a VWSC file!')
            sys.exit(-1)
        
        vwsc_elements = parse_vwsc_file(os.path.join(sys.argv[1],
                                                     BINDIR, vwsc_file))
        
        data = vwsc_to_score(vwsc_elements)
        
        # Write score data to JSON file
        with open(os.path.join(sys.argv[1], 'score.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(data, indent=4, sort_keys=True).encode(
                'utf-8'))

        
if __name__ == '__main__':
    main()
