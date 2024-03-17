#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director VWLB files.
# VWLB files contains the labels of the score.
# 

import sys
import os
import logging
import json
from .vwlb import parse_vwlb_data

BINDIR = 'bin'

#logging.basicConfig(level=logging.DEBUG)


# ==============================================================================
# Reads from VWLB file the markers channel of the score and its frame
def parse_vwlb_file(vwlb_file):    
    with open(vwlb_file, mode='rb') as file:
        fdata = file.read()
        return parse_vwlb_data(fdata)
            
    return []

# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("USAGE: vwlbxtract <work directory>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        vwlb_file = None
        
        for f in os.listdir(os.path.join(sys.argv[1], BINDIR)):
            if f.endswith('VWLB'):
                vwlb_file = f
                break
        
        if vwlb_file is None:
            logging.error('Can not find a VWLB file!')
            sys.exit(-1)
        
        vwlb_elements = parse_vwlb_file(os.path.join(sys.argv[1], BINDIR,
                                                     vwlb_file))
        # Write markers data to JSON file
        with open(os.path.join(sys.argv[1], 'markers.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(vwlb_elements, indent=4, sort_keys=True
                                    ).encode('utf-8'))

if __name__ == '__main__':
    main()
