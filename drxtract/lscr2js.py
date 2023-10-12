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
from .lingosrc.codegen import generate_js_code

logging.basicConfig(level=logging.DEBUG)

# =============================================================================
def main():
    if len(sys.argv) < 4:
        print("USAGE: lscr2js <work directory> <lscr file name>"
            + " <lnam file path>")

    else:
        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[1],
                sys.argv[2])))
            sys.exit(-1)

        if not sys.argv[2].endswith('.Lscr'):
            logging.error(" '%s' does not end in .Lscr"%(sys.argv[2]))
            sys.exit(-1)

        if not os.path.isfile(sys.argv[3]):
            logging.error(" '%s' is not a file"%(sys.argv[3]))
            sys.exit(-1)

        if not sys.argv[3].endswith('.Lnam'):
            logging.error(" '%s' does not end in .Lnam"%(sys.argv[3]))
            sys.exit(-1)

        # Parse the LNAM and LSCR files into an AST
        name_list = parse_lnam_file(sys.argv[3])

        script: Script =  parse_lrcr_file(
            os.path.join(sys.argv[1], sys.argv[2]),
            name_list)
        
        jscode: str = generate_js_code(script)
        
        #print("========================\n")
        #print(jscode)

        # Save file
        file_ext = "js"
        lscr_file = os.path.join(sys.argv[1], sys.argv[2])
        nfiles = lscr_file[0:lscr_file.rfind('.')]
        file_name = "%s.%s"%(nfiles, file_ext)
        with open(file_name, 'wb') as file:
            file.write(jscode.encode('utf-8'))
        