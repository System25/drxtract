#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to decompile lingo scripts.
# LSCR file format details from: 
# http://fileformats.archiveteam.org/wiki/Lingo_bytecode
# 

import sys
import os
import logging
from .lingosrc.parse import parse_lnam_file, parse_lrcr_file
from .lingosrc.ast import Script
from .lingosrc.codegen import generate_lingo_code

logging.basicConfig(level=logging.DEBUG)

# Default bit order for MAC
bit_order_type = 'mac'
bit_order = ">"


# =============================================================================
def main():
    if len(sys.argv) < 5:
        print("USAGE: lscr2lingo [pc|mac] <work directory> <lscr file name>"
            + " <lnam file path>")

    else:
        if sys.argv[1] != 'pc' and sys.argv[1] != 'mac':
            logging.error(" First argument must be 'pc' or 'mac'")
            sys.exit(-1)

        if sys.argv[1] == 'pc':
            bit_order_type = 'pc'
            bit_order = "<"

        if not os.path.isdir(sys.argv[2]):
            logging.error(" '%s' is not a directory"%(sys.argv[2]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[2], sys.argv[3])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[2],
                sys.argv[3])))
            sys.exit(-1)

        if not sys.argv[3].endswith('.Lscr'):
            logging.error(" '%s' does not end in .Lscr"%(sys.argv[3]))
            sys.exit(-1)

        if not os.path.isfile(sys.argv[4]):
            logging.error(" '%s' is not a file"%(sys.argv[4]))
            sys.exit(-1)

        if not sys.argv[4].endswith('.Lnam'):
            logging.error(" '%s' does not end in .Lnam"%(sys.argv[4]))
            sys.exit(-1)

        # Parse the LNAM and LSCR files into an AST
        name_list = parse_lnam_file(sys.argv[4])

        script: Script =  parse_lrcr_file(
            os.path.join(sys.argv[2], sys.argv[3]),
            name_list)
        
        lingo: str = generate_lingo_code(script)
        
        #print("========================\n")
        #print(lingo)

        # Save file
        file_ext = "lingo"
        lscr_file = os.path.join(sys.argv[2], sys.argv[3])
        nfiles = lscr_file[0:lscr_file.rfind('.')]
        file_name = "%s.%s"%(nfiles, file_ext)
        with open(file_name, 'wb') as file:
            file.write(lingo.encode('utf-8'))
        