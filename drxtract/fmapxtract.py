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
import logging
import json
from .fmap import parse_fmap_data

BINDIR = 'bin'

logging.basicConfig(level=logging.DEBUG)

# ==============================================================================
# Reads from Fmap file the fonts information
def parse_fmap_file(fmap_file):
    with open(fmap_file, mode='rb') as file:
        fdata = file.read()
        return parse_fmap_data(fdata)

    return []

# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("USAGE: fmapxtract <work directory>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        fmap_file = None
        
        for f in os.listdir(os.path.join(sys.argv[1], BINDIR)):
            if f.endswith('Fmap'):
                fmap_file = f
                break
        
        if fmap_file is None:
            logging.error('Can not find a Fmap file!')
            sys.exit(-1)
        
        fmap_elements = parse_fmap_file(os.path.join(sys.argv[1], BINDIR,
                                                     fmap_file))
        # Write font map data to JSON file
        with open(os.path.join(sys.argv[1], 'fonts.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(fmap_elements, indent=4, sort_keys=True
                                    ).encode('utf-8'))

if __name__ == '__main__':
    main()

