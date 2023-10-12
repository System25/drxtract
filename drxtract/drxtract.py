#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract contents from Macromedia Director 4.0 and 5.0 DRX files.
# Also can extract contents from "updated" Macromedia Director DRI files.
# 

import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG)

def main():   
    if len(sys.argv) < 4:
        print("USAGE: drxtract [pc|mac] <file.drx> <directory>")

    else:
        if sys.argv[1] != 'pc' and sys.argv[1] != 'mac':
            logging.error("First argument must be 'pc' or 'mac'")
            sys.exit(-1)

        if len(os.path.dirname(sys.argv[0])) == 0:
            basepath = '%s '%(sys.executable)
        else:
            basepath = ('%s/'%(os.path.dirname(sys.argv[0])))

        if not os.path.isfile(sys.argv[2]):
            logging.error("'%s' is not a file"%(sys.argv[2]))
            sys.exit(-1)
        
        if not os.path.isdir(sys.argv[3]):
            logging.error("'%s' is not a directory"%(sys.argv[3]))
            sys.exit(-1)

        # Extract RIFF file content
        cmd = '%sriffxtract %s %s %s'%(
            basepath, # Scripts path
            sys.argv[1], # pc or mac
            sys.argv[2], # director file
            sys.argv[3]  # work directory
        )
        logging.debug("======================================================")
        logging.debug("Extracting the RIFF file content by using the command:")
        logging.debug(cmd)
        logging.debug("------------------------------------------------------")
        os.system(cmd)
        
        # Extract the score labels
        cmd = '%svwlbxtract %s'%(
            basepath, # Scripts path
            sys.argv[3] # work directory
        )
        logging.debug("======================================================")
        logging.debug("Extracting the score labels by using the command:")        
        logging.debug(cmd)
        logging.debug("------------------------------------------------------")
        os.system(cmd)
        
        # Extract the font map
        cmd = '%sfmapxtract %s'%(
            basepath, # Scripts path
            sys.argv[3] # work directory
        )
        logging.debug("======================================================")
        logging.debug("Extracting the font map by using the command:")  
        logging.debug(cmd)
        logging.debug("------------------------------------------------------")
        os.system(cmd)        
        
        # Extract the casting elements
        cmd = '%scasxtract %s %s'%(
            basepath, # Scripts path
            sys.argv[1], # pc or mac
            sys.argv[3]  # work directory
        )
        logging.debug("======================================================")
        logging.debug("Extracting the casting elements by using the command:")  
        logging.debug(cmd)
        logging.debug("------------------------------------------------------")
        os.system(cmd)
        
        # Extract the score
        cmd = '%svwscxtract %s'%(
            basepath, # Scripts path
            sys.argv[3] # work directory
        )
        logging.debug("======================================================")
        logging.debug("Extracting the score by using the command:")  
        logging.debug(cmd)
        logging.debug("------------------------------------------------------")
        os.system(cmd)
