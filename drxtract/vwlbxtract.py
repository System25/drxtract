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
import struct
import logging
import json

BINDIR = 'bin'

#logging.basicConfig(level=logging.DEBUG)


# ==============================================================================
# Reads from VWLB file the markers channel of the score and its frame
def parse_vwlb_file(vwlb_file):
    vwlb_data = []
    
    with open(vwlb_file, mode='rb') as file:
        fdata = file.read()

        indx = 0
        nmarkers = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("N Markers: %d"%(nmarkers))
        
        mnidx = 2 + 4 * (nmarkers + 1)
        
        for _ in range(0, nmarkers):
            marker = {}
            
            frame = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
            indx = indx + 2
            logging.debug("Frame: %d"%(frame))
            marker['frame'] = frame
            
            name_start = mnidx + struct.unpack(">h", fdata[(indx):(indx+2)])[0]
            indx = indx + 2
            logging.debug("name_start: %d"%(name_start))
            
            name_end = mnidx + struct.unpack(">h", fdata[(indx+2):(indx+4)])[0]
            logging.debug("name_end: %d"%(name_end))
            
            name = fdata[name_start:name_end].decode('utf-8')
            logging.debug("Name: %s"%(name))
            marker['name'] = name
            
            vwlb_data.append(marker)
            
    return vwlb_data

# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("USAGE: vwlbxtract <work directory>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        vwlb_file = None
        
        for f in os.listdir(os.path.join(sys.argv[1], BINDIR)):
            if f.endswith('VWLB'):
                vwlb_file = f
                break
        
        if vwlb_file is None:
            logging.error('Can not find a VWLB file!')
            sys.exit(-1)
        
        vwlb_elements = parse_vwlb_file(os.path.join(sys.argv[1], BINDIR, vwlb_file))
        # Write markers data to JSON file
        with open(os.path.join(sys.argv[1], 'markers.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(vwlb_elements, indent=4, sort_keys=True).encode('utf-8'))

