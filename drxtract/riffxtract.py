#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract contents from Director RIFF files into a "bin" directory.
# 



import sys
import os
import logging
import re
from .lingosrc.util import vsprintf
from .riff.riff import parse_riff, find_riff_in_exe, RiffData, Chunk
from .riff.imap import InputMAP, parse_imap
from .riff.mmap import MemoryMAP, parse_mmap

logging.basicConfig(level=logging.DEBUG)

# Save all blocks (for investigation purposes)
SAVE_ALL_BLOCKS = False

# Default byte order for MAC
byte_order_type = 'mac'
byte_order = ">"


BINDIR = 'bin'

MV93_FILE_TYPE = 'MV93'
RIFX_FILE_FORMAT = 'RIFX'
IMAP_FILE_FORMAT = 'imap'
MMAP_FILE_FORMAT = 'mmap'
FREE_FILE_FORMAT = 'free'
JUNK_FILE_FORMAT = 'junk'

CHUNKS_TO_IGNORE = (RIFX_FILE_FORMAT, IMAP_FILE_FORMAT, MMAP_FILE_FORMAT,
                    FREE_FILE_FORMAT, JUNK_FILE_FORMAT)

#
# Saves a RIFF chunk into a file in a folder
# 
# =============================================================================
def save_chunk(chunk: Chunk, number: int, folder: str):
    file_name =  vsprintf("%s.%s", number, chunk.identifier)
    file_name = re.sub(r"[^A-Za-z0-9\-_\.]", "_", file_name)
    logging.debug("FILE: Saving chunk content to: %s", file_name)
    
    with open(os.path.join(folder, file_name), 'wb') as file:
        file.write(chunk.data)
        file.close()

#
# Main method
# 
# =============================================================================
def main():
    global byte_order_type, byte_order

    if len(sys.argv) < 4:
        print("USAGE: riffxtract [pc|mac] <file.drx> <directory>")

    else:
        if sys.argv[1] != 'pc' and sys.argv[1] != 'mac':
            logging.error("First argument must be 'pc' or 'mac'")
            sys.exit(-1)

        if sys.argv[1] == 'pc':
            byte_order_type = 'pc'
            byte_order = "<"

        if not os.path.isfile(sys.argv[2]):
            logging.error("'%s' is not a file", sys.argv[2])
            sys.exit(-1)
        
        if not os.path.isdir(sys.argv[3]):
            logging.error("'%s' is not a directory", sys.argv[3])
            sys.exit(-1)

        # Create bin directory (when necessary)
        if not os.path.isdir(os.path.join(sys.argv[3], BINDIR)):
            os.mkdir(os.path.join(sys.argv[3], BINDIR))

        logging.debug("Try to parse %s file.", sys.argv[2])
        riffData: RiffData = RiffData(byte_order)
        rifx_offset: int = 0
        with open(sys.argv[2], mode='rb') as file:
            fileContent: bytes = file.read()
            if sys.argv[2].upper().endswith('.EXE'):
                # Try to find DRX header inside the EXE file
                rifx_offset = find_riff_in_exe(fileContent)
            
            riffData = parse_riff(fileContent, rifx_offset, byte_order)

        output_folder: str = os.path.join(sys.argv[3], BINDIR)
        if SAVE_ALL_BLOCKS:
            for i in range(0, len(riffData.chunks)):
                chunk: Chunk = riffData.chunks[i]
                save_chunk(chunk, i+1, output_folder)
                
        else:
            # Parse the imap block
            chunk: Chunk = riffData.chunks[0]
            if chunk.identifier != IMAP_FILE_FORMAT:
                logging.error("The first chunk is not an IMAP chunk: %s",
                              chunk.identifier)
                sys.exit(-1)
            
            imap: InputMAP = parse_imap(chunk.data, byte_order)
            chunk = riffData.get_by_offset(imap.offset - rifx_offset)
            if chunk.identifier != MMAP_FILE_FORMAT:
                logging.error("Wrong MMAP location!")
                sys.exit(-1)

            mmap: MemoryMAP = parse_mmap(chunk.data, byte_order)
            idx = -1
            for resource in mmap.resources:
                idx += 1
                if ((resource.chunkID in CHUNKS_TO_IGNORE) or
                    (resource.size <= 0)):
                    continue
                
                offset: int = resource.offset
                chunk = riffData.get_by_offset(offset - rifx_offset)
                if resource.chunkID != chunk.identifier:
                    logging.error("Wrong resource ID (%s != %s)", 
                                  resource.chunkID, chunk.identifier)
                    sys.exit(-1)
                
                save_chunk(chunk, idx, output_folder)
                

        
if __name__ == '__main__':
    main()
