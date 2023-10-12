#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract contents from Director RIFF files into a "bin" directory.
# 



import sys
import os
import struct
import re
import logging

#logging.basicConfig(level=logging.DEBUG)


# Default bit order for MAC
bit_order_type = 'mac'
bit_order = ">"


BINDIR = 'bin'

MV93_FILE_TYPE = 'MV93'
RIFX_FILE_FORMAT = 'RIFX'
IMAP_FILE_FORMAT = 'imap'
MMAP_FILE_FORMAT = 'mmap'
FREE_FILE_FORMAT = 'free'
JUNK_FILE_FORMAT = 'junk'

# Save other blocks (for investigation purposes)
SAVE_OTHER_BLOCKS = False

# ====================================================================================================================================
def read_chunk(fileContent, index):
    block_type = struct.unpack("cccc", fileContent[index:(index+4)])
    bt = []
    for c in range(0,4):
        if (block_type[c].decode('ascii') > '\0' and
            block_type[c].decode('ascii') >= ' ' and
            block_type[c].decode('ascii') <= 'z'):
            bt.append(block_type[c].decode('ascii'))
        else:
            bt.append('_')
    block_type = ('%c%c%c%c'%(bt[0], bt[1], bt[2], bt[3]))
    logging.info("==================================")
    logging.info(" Block type: %s"%(block_type))

    block_size = struct.unpack(bit_order+"i", fileContent[(index+4):(index+8)])[0]
    logging.info(" Block size: %s"%(block_size))

    padding = (block_size % 2)
    logging.info(" Padding: %s"%(padding))

    block_data = fileContent[(index+8):(index + 8 + block_size)]
    
    return block_type, block_size, padding, block_data

# ====================================================================================================================================
def parse_imap(data):
    # Input MAP
    # https://docs.google.com/document/d/1jDBXE4Wv1AEga-o1Wi8xtlNZY4K2fHxW2Xs8RgARrqk/edit#heading=h.dq1rrg8abhxt
    logging.debug("==================================")
    logging.debug(" Parse input map: %s bytes"%(len(data)))
    content = struct.unpack(bit_order+"iiihhii", data)
    logging.debug("IMAP[0] Memory MAP count: %s"%(content[0]))
    logging.debug("IMAP[1] Memory MAP offset  %s"%(content[1]))
    logging.debug("IMAP[2] Memory MAP file version: %s"%(content[2]))
    logging.debug("IMAP[3] Reserved: %s"%(content[3]))
    logging.debug("IMAP[4] Unknown: %s"%(content[4]))
    logging.debug("IMAP[5] Reserved2: %s"%(content[5]))
    
    return content[1]

# ====================================================================================================================================
def parse_mmap(data, fileContent, offset):
    # This file types will be ignored
    types_to_ignore = [IMAP_FILE_FORMAT, MMAP_FILE_FORMAT, FREE_FILE_FORMAT, JUNK_FILE_FORMAT]

    # Unknown block data
    content = struct.unpack(bit_order+"hhiiiii", data[0:24])
    logging.debug("MMAP[0] Property size: %s"%(content[0]))
    logging.debug("MMAP[1] Resource size?: %s"%(content[1]))
    # Number Of Files (including nulls at the end of the directory)
    no_files_wnull = content[2]
    # Number Of Files (not including the nulls at the end of the directory)
    no_files_wonull = content[3]
    logging.debug("MMAP: Number of files (including nulls) %s"%(no_files_wnull))
    logging.debug("MMAP: Number of files (without nulls) %s"%(no_files_wonull))

    logging.debug("MMAP[4] First junk resource ID?: %s"%(content[6]))
    logging.debug("MMAP[5] Old memory map resource ID?: %s"%(content[6]))
    logging.debug("MMAP[6] First free resource ID?: %s"%(content[6]))

    # Ignore RIFX file data
    file_format = struct.unpack("cccc", data[24:28])
    file_format = ('%c%c%c%c'%(file_format[0].decode('ascii'),
                               file_format[1].decode('ascii'),
                               file_format[2].decode('ascii'),
                               file_format[3].decode('ascii')))
    logging.debug("MMAP: Meta file: %s"%(file_format))
    if RIFX_FILE_FORMAT != file_format:
        logging.error(" nmap internal format is not %s"%(RIFX_FILE_FORMAT))
        sys.exit(-1)

    # Read file length
    file_length = struct.unpack(bit_order+"i", data[28:32])[0]
    logging.debug("NMAP: Meta file length (must be the whole data length): %s"%(file_length))

    if len(fileContent) != file_length + 8 + offset:
        logging.warning(" Bad file length! Using %d as file length"%(len(fileContent)))
        
    # Read file offset
    file_offset = struct.unpack(bit_order+"i", data[32:36])[0]
    logging.debug("NMAP: Meta file offset: %s"%(file_offset))
    if file_offset != 0 and file_offset != offset:
        logging.error(" Bad file offset!")
        sys.exit(-1)

    # Unknown
    unknown0 = struct.unpack(bit_order+"i", data[36:40])[0]
    logging.debug("NMAP: Unknown 0: %s"%(unknown0))

    unknown1 = struct.unpack(bit_order+"i", data[40:44])[0]
    logging.debug("NMAP: Unknown 1: %s"%(unknown1))

    name_list = []
    cast_index = []
    cast_info = {}

    # Look for list of names
    index = 44
    nfiles = 1
    while index < len(data) and nfiles < no_files_wonull:
        logging.debug("---------------------------------------")
        logging.debug("FILE: Number: %s"%(nfiles))

        # Read file format
        file_format = struct.unpack("cccc", data[index:(index+4)])
        file_format = ('%c%c%c%c'%(file_format[0].decode('ascii'),
                                   file_format[1].decode('ascii'),
                                   file_format[2].decode('ascii'),
                                   file_format[3].decode('ascii')))
        logging.debug("FILE: File format: %s"%(file_format))

        # Read file length
        file_length = struct.unpack(bit_order+"i", data[(index+4):(index+8)])[0]
        logging.debug("FILE: Length: %s"%(file_length))

        # Read file offset
        file_offset = struct.unpack(bit_order+"i", data[(index+8):(index+12)])[0]
        logging.debug("FILE: Offset: %s"%(file_offset))

        # Unknown
        unknown0 = struct.unpack(bit_order+"i", data[(index+12):(index+16)])[0]
        logging.debug("FILE: Unknown 0: %s"%(unknown0))

        unknown1 = struct.unpack(bit_order+"i", data[(index+16):(index+20)])[0]
        logging.debug("FILE: Unknown 1: %s"%(unknown1))

        if (file_format in types_to_ignore) or (file_length == 0):
            logging.debug("FILE: Empty file data or must ignore file!")

        else:
            # Save file content
            file_ext = file_format
            if sys.argv[1] == 'pc':
                file_ext = file_format[3] + file_format[2] + file_format[1] + file_format[0]

            file_name = "%s.%s"%(nfiles, file_ext)
            # Remove strange chars
            file_namer = re.sub(r"[^A-Za-z0-9\-_\.]", "_", file_name)
            if file_namer != file_name:
                try:
                    # Maybe is a japanese file name
                    file_name = file_name.decode('shift-jis')
                except:
                    file_name = file_namer
            file_name = file_name.replace("/", "_")
            file_name = file_name.replace("*", "_")


            try:
                logging.debug(u"FILE: Saving file content to: %s"%(file_name))
            except:
                file_name = file_namer
                logging.debug(u"FILE: Saving file content to: %s"%(file_name))

            with open(os.path.join(sys.argv[3], BINDIR, file_name), 'wb') as file:
                fdata = fileContent[file_offset:(file_offset+file_length+8)]
                # Read data format
                data_format = struct.unpack("cccc", fdata[0:4])
                data_format = ('%c%c%c%c'%(data_format[0].decode('ascii'),
                                           data_format[1].decode('ascii'),
                                           data_format[2].decode('ascii'),
                                           data_format[3].decode('ascii')))
                if data_format != file_format:
                    logging.error(" Bad data format! (%s != %s)"%(data_format, file_format))
                    sys.exit(-1)

                if len(fdata)<8:
                    logging.debug("WARNING: Creating empty file!")
                    file.close()
                    index = index + 20
                    nfiles = nfiles + 1
                    continue

                # Read file length
                data_length = struct.unpack(bit_order+"i", fdata[4:8])[0]
                if data_length != file_length:
                    logging.error(" Bad data length! (%s != %s)"%(data_length, file_length))
                    sys.exit(-1)

                file.write(fdata[8:])
                file.close()

        index = index + 20
        nfiles = nfiles + 1


def parse_riff(fileContent, offset):
    # Check if file format is RIFX
    file_format = struct.unpack("cccc", fileContent[offset:offset+4])
    file_format = ('%c%c%c%c'%(file_format[0].decode('ascii'),
                               file_format[1].decode('ascii'),
                               file_format[2].decode('ascii'),
                               file_format[3].decode('ascii')))

    logging.info(" File format: %s"%(file_format))
    if RIFX_FILE_FORMAT != file_format:
        logging.error(" File format is not %s"%(RIFX_FILE_FORMAT))
        sys.exit(-1)

    # Read file length
    file_length = struct.unpack(bit_order+"i", fileContent[offset+4:offset+8])[0]
    logging.info(" File contains %s bytes of information."%(file_length))
    
    if len(fileContent) != file_length + 8 + offset:
        logging.warning(" Using %d as file length"%(len(fileContent)))
        
 
    # Check Macromedia Director MV93 header
    mv93_format = struct.unpack("cccc", fileContent[offset+8:offset+12])
    mv93_format = ('%c%c%c%c'%(mv93_format[0].decode('ascii'),
                               mv93_format[1].decode('ascii'),
                               mv93_format[2].decode('ascii'),
                               mv93_format[3].decode('ascii')))
    logging.info(" Data format: %s"%(mv93_format))
    if MV93_FILE_TYPE != mv93_format:
        logging.error(" Data format is not %s"%(MV93_FILE_TYPE))
        sys.exit(-1)

    # Create bin directory (when necessary)
    if not os.path.isdir(os.path.join(sys.argv[3], BINDIR)):
        os.mkdir(os.path.join(sys.argv[3], BINDIR))
        
    index = offset + 12
    nfiles = 1
    while index < len(fileContent):
        block_type, block_size, padding, block_data = read_chunk(fileContent, index)
        
        if block_type == IMAP_FILE_FORMAT:
            # Parse 'imap' block
            mmap_offset = parse_imap(block_data)
            
            block_type, block_size, padding, block_data = read_chunk(fileContent, mmap_offset)
            if block_type == MMAP_FILE_FORMAT:
                # Parse 'mmap' block
                parse_mmap(block_data, fileContent, offset)
            else:
                logging.error("Wrong MMAP location!")
                sys.exit(-1)


        elif SAVE_OTHER_BLOCKS:
            logging.info(" Other block type: %s. Saving!"%(block_type))
            
            # Save file content
            file_ext = block_type
            if sys.argv[1] == 'pc':
                file_ext = block_type[3] + block_type[2] + block_type[1] + block_type[0]

            file_name = "%s.%s"%(nfiles, file_ext)
            # Remove strange chars
            file_namer = re.sub(r"[^A-Za-z0-9\-_\.]", "_", file_name)
            if file_namer != file_name:
                try:
                    # Maybe is a japanese file name
                    file_name = file_name.decode('shift-jis')
                except:
                    file_name = file_namer
            file_name = file_name.replace("/", "_")


            try:
                logging.debug(u"FILE: Saving file content to: %s"%(file_name))
            except:
                file_name = file_namer
                logging.debug(u"FILE: Saving file content to: %s"%(file_name))

            with open(os.path.join(sys.argv[3], BINDIR, file_name), 'wb') as file:
                file.write(block_data)
                file.close()

            
            
        nfiles = nfiles + 1
        index = index + 8 + block_size + padding


def main():
    global bit_order_type, bit_order
    global MV93_FILE_TYPE, RIFX_FILE_FORMAT, IMAP_FILE_FORMAT
    global MMAP_FILE_FORMAT, FREE_FILE_FORMAT, JUNK_FILE_FORMAT

    if len(sys.argv) < 4:
        print("USAGE: riffxtract [pc|mac] <file.drx> <directory>")

    else:
        if sys.argv[1] != 'pc' and sys.argv[1] != 'mac':
            logging.error(" First argument must be 'pc' or 'mac'")
            sys.exit(-1)

        if sys.argv[1] == 'pc':
            bit_order_type = 'pc'
            bit_order = "<"
            MV93_FILE_TYPE = '39VM'
            RIFX_FILE_FORMAT = 'XFIR'
            IMAP_FILE_FORMAT = 'pami'
            MMAP_FILE_FORMAT = 'pamm'
            FREE_FILE_FORMAT = 'eerf'

        if not os.path.isfile(sys.argv[2]):
            logging.error(" '%s' is not a file"%(sys.argv[2]))
            sys.exit(-1)
        
        if not os.path.isdir(sys.argv[3]):
            logging.error(" '%s' is not a directory"%(sys.argv[3]))
            sys.exit(-1)

        logging.debug("Try to parse %s file."%(sys.argv[2]))
        rifx_offset = 0
        with open(sys.argv[2], mode='rb') as file:
            fileContent = file.read()
            if sys.argv[2].upper().endswith('.EXE'):
                # Try to find DRX header inside the EXE file
                content = fileContent
                index = content.find(RIFX_FILE_FORMAT.encode('ascii'))
                found = False
                while index >= 0 and not found:
                    rifx_offset += index
                    content = content[index:]
                    if content[8:12] == MV93_FILE_TYPE.encode('ascii'):
                        found = True
                    else:
                        content = content[4:]
                        rifx_offset += 4
                        index = content.find(RIFX_FILE_FORMAT.encode('ascii'))
                logging.debug("Use %s as RIFX index inside EXE"%(rifx_offset))
            parse_riff(fileContent, rifx_offset)

