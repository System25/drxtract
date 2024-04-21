#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director string files.
# 

import sys
import os
import logging
import json
from .stxt import parse_stxt_data, TextData

logging.basicConfig(level=logging.DEBUG)


# ==============================================================================
def stxt2json(castData, fontmap, stxt_file):
    with open(stxt_file, mode='rb') as file:
        fdata = file.read()
        
        txtData: TextData = parse_stxt_data(fdata, fontmap)
        
        castData['text'] = txtData['text']
        castData['txt_format'] = txtData['txt_format']

        # Write CAST data to JSON file
        dest_dir = os.path.dirname(stxt_file)        
        with open(os.path.join(dest_dir, 'data.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(castData, indent=4, sort_keys=True).encode(
                'utf-8'))


# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: stxt2json <work directory> <stxt file name>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file", os.path.join(sys.argv[1],
                                                              sys.argv[2]))
            sys.exit(-1)

        if not sys.argv[2].endswith('.STXT'):
            logging.error(" '%s' does not end in '.STXT'", sys.argv[2])
            sys.exit(-1)

        # Get the font map
        fontmap = []
        fontfile = os.path.join(os.path.dirname(os.path.dirname(sys.argv[1])),
                                'fonts.json')
        if os.path.isfile(fontfile):
            with open(fontfile, mode='r', encoding='utf-8') as file:
                text = file.read()
                fontmap = json.loads(text)
        else:
            logging.warning("Fonts map not found in: %s", fontfile)
            
            
        # Get cast file data
        castData = {}
        with open(os.path.join(sys.argv[1], 'data.json'), mode='r',
                  encoding='utf-8') as file:
            text = file.read()
            castData = json.loads(text)

        stxt2json(castData, fontmap, os.path.join(sys.argv[1], sys.argv[2]))

if __name__ == '__main__':
    main()

        