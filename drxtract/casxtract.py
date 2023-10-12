#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to extract Macromedia Director casting files from a "bin" directory
# into a "cas" directory.
# 

import sys
import os
import struct
import re
import logging
import json
import base64
from shutil import copyfile

logging.basicConfig(level=logging.DEBUG)


# Default bit order for MAC
bit_order_type = 'mac'
bit_order = ">"

BINDIR = 'bin'
CASDIR = 'cas'

# -- Casting data types --
DIR_IMAGE_TYPE = 1
DIR_TEXT_INPUT_TYPE = 3
DIR_CLUT_TYPE = 4
DIR_SND_TYPE = 6
DIR_PUSH_BUTTON_TYPE = 7
DIR_SHAPE_TYPE = 8
DIR_LSCR_TYPE = 11
DIR_TEXT_TYPE = 12
DIR_TRAN_TYPE = 14

if len(os.path.dirname(sys.argv[0])) == 0:
    basepath = '%s '%(sys.executable)
else:
    basepath = ('%s/'%(os.path.dirname(sys.argv[0])))

# ==============================================================================
# Replace the extension in a filename
def replace_ext(filename, new_extension):
    f = filename
    if '.' in f:
        f = filename[0:filename.rfind('.')]
        f = '%s.%s'%(f, new_extension)
        
    return f
    
# ==============================================================================
# Translate shape type ID to string representation    
def get_shape_type(shape_type_id):    
    if shape_type_id == 1:
        return 'rect'
    elif shape_type_id == 2:
        return 'roundRect'
    elif shape_type_id == 3:
        return 'oval'
    elif shape_type_id == 4:
        return 'line'    
    
    # Unknown id
    return shape_type_id    
    
# ==============================================================================
# Translate palette number to string representation
def get_palette(palette_id):
    
    # I found this in a german book called
    # "Macromedia Director: Multimediaprogrammierung mit Lingo"
    # https://books.google.es/books?id=UxLuBQAAQBAJ&pg=PA282&lpg=PA282&dq=macromedia+director+ntsc+web+grayscale+rainbow&source=bl&ots=tlcNQFqWod&sig=ACfU3U2d0o3Kv3y7_9umDgOCPGBDqooIzQ&hl=es&sa=X&ved=2ahUKEwjXs-rnlNXiAhVDrxoKHdcACWIQ6AEwB3oECAUQAQ#v=onepage&q=macromedia%20director%20ntsc%20web%20grayscale%20rainbow&f=false
    
    if palette_id <= 0:
        # There is no zero casting member so
        # it must be a predefined palette
        palette_id = palette_id - 1
    
    if palette_id == -1:
        return 'systemMac'
    elif palette_id == -102:
        return 'systemWin'
    elif palette_id == -2:
        return 'rainbow'
    elif palette_id == -3:
        return 'grayscale'
    elif palette_id == -4:
        return 'pastels'
    elif palette_id == -5:
        return 'vivid'
    elif palette_id == -6:
        return 'ntsc'
    elif palette_id == -7:
        return 'metallic'
    elif palette_id == -8:
        return 'web216'
    elif palette_id == -101:
        return 'systemWinDir4'
    
    # Unknown id
    return palette_id


# ==============================================================================
# Translate a transition number to string representation
def get_transtition(transition_id):
    
    # I found this in: Director 8 Demystified
    # (puppetTransition lingo script reference)
    
    if transition_id == 1:
        return 'wipe right'
    elif transition_id == 2:
        return 'wipe left'
    elif transition_id == 3:
        return 'wipe down'
    elif transition_id == 4:
        return 'wipe up'
    elif transition_id == 5:
        return 'center out, horizontal'
    elif transition_id == 6:
        return 'edges in, horizontal'
    elif transition_id == 7:
        return 'center out, vertical'
    elif transition_id == 8:
        return 'edges in, vertical'
    elif transition_id == 9:
        return 'center out, square'
    elif transition_id == 10:
        return 'edges in, square'
    elif transition_id == 11:
        return 'push left'
    elif transition_id == 12:
        return 'push right'
    elif transition_id == 13:
        return 'push down'
    elif transition_id == 14:
        return 'push up'
    elif transition_id == 15:
        return 'reveal up'
    elif transition_id == 16:
        return 'reveal up, right'
    elif transition_id == 17:
        return 'reveal right'
    elif transition_id == 18:
        return 'reveal down, right'
    elif transition_id == 19:
        return 'reveal down'
    elif transition_id == 20:
        return 'reveal down, left'
    elif transition_id == 21:
        return 'reveal left'
    elif transition_id == 22:
        return 'reveal up, left'
    elif transition_id == 23:
        return 'dissolve, pixels fast'
    elif transition_id == 24:
        return 'dissolve, boxy rectangles'
    elif transition_id == 25:
        return 'dissolve, boxy squares'
    elif transition_id == 26:
        return 'dissolve, patterns'
    elif transition_id == 27:
        return 'random rows'
    elif transition_id == 28:
        return 'random columns'
    elif transition_id == 29:
        return 'cover down'
    elif transition_id == 30:
        return 'cover down, left'
    elif transition_id == 31:
        return 'cover down, right'
    elif transition_id == 32:
        return 'cover left'
    elif transition_id == 33:
        return 'cover right'
    elif transition_id == 34:
        return 'cover up'
    elif transition_id == 35:
        return 'cover up, left'
    elif transition_id == 36:
        return 'cover up, right'
    elif transition_id == 37:
        return 'venetian blinds'
    elif transition_id == 38:
        return 'checkerboard'
    elif transition_id == 39:
        return 'strips on bottom, build left'
    elif transition_id == 40:
        return 'strips on bottom, build right'
    elif transition_id == 41:
        return 'strips on left, build down'
    elif transition_id == 42:
        return 'strips on left, build up'
    elif transition_id == 43:
        return 'strips on right, build down'
    elif transition_id == 44:
        return 'strips on right, build up'
    elif transition_id == 45:
        return 'strips on top, build left'
    elif transition_id == 46:
        return 'strips on top, build right'
    elif transition_id == 47:
        return 'zoom open'
    elif transition_id == 48:
        return 'zoom close'
    elif transition_id == 49:
        return 'vertical blinds'
    elif transition_id == 50:
        return 'dissolve, bits fast'
    elif transition_id == 51:
        return 'dissolve, pixels'
    elif transition_id == 52:
        return 'dissolve, bits'

    # Unknown id
    return transition_id


# ==============================================================================
def parse_key_file(key_file):
    logging.debug("Parsing key file: %s ---------------------------"%(key_file))
    key_data = {}

    with open(key_file, mode='rb') as file:
        fdata = file.read()

        indx = 0

        # Unknown header data
        unk = struct.unpack(bit_order+"i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Unknown: %08x"%(unk))

        unk = struct.unpack(bit_order+"i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Unknown: %08x"%(unk))

        nelements = struct.unpack(bit_order+"i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Number of elements: %08x"%(nelements))

        for _ in range(nelements-1):
            nfile = struct.unpack(bit_order+"i", fdata[(indx+0):(indx+4)])[0]
            cas_index = struct.unpack(bit_order+"i", fdata[(indx+4):(indx+8)])[0]

            file_ext = struct.unpack("cccc", fdata[indx+8:indx+12])
            indx = indx + 12
            
            if ((not int.from_bytes(file_ext[0], byteorder='little') in range(32, 122)) or
                (not int.from_bytes(file_ext[1], byteorder='little') in range(32, 122)) or
                (not int.from_bytes(file_ext[2], byteorder='little') in range(32, 122)) or
                (not int.from_bytes(file_ext[3], byteorder='little') in range(32, 122))):
                # Not an ASCII char
                continue
                
            file_ext = ('%c%c%c%c'%(file_ext[0].decode('ascii'),
                                    file_ext[1].decode('ascii'),
                                    file_ext[2].decode('ascii'),
                                    file_ext[3].decode('ascii')))
            if sys.argv[1] == 'pc':
                file_ext = file_ext[3] + file_ext[2] + file_ext[1] + file_ext[0]
            
            # Remove strange chars
            file_ext = re.sub(r"[^A-Za-z0-9\-_\.]", "_", file_ext)
            
            if cas_index > 0 and nfile > 0:
                cas_index = ('%08x'%cas_index)

                if not cas_index in key_data:
                    key_data[cas_index] = []

                key_data[cas_index].append("%s.%s"%(nfile, file_ext))

                key_value = "KEY['%s'] = '%s.%s'"%(cas_index, nfile, file_ext)
                logging.debug(key_value)
    

    return key_data

# ==============================================================================
def parse_cas_file(cas_file):
    logging.debug("Parsing cas file: %s ---------------------------"%(cas_file))
    cas_data = []

    with open(cas_file, mode='rb') as file:
        fdata = file.read()

        indx = 0
        i = 0
        while len(fdata) >= indx + 4:
            cas_index = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
            indx = indx + 4
            cas_index = "%08x"%(cas_index)
            cas_data.append(cas_index)
            logging.debug('CAS[%i] = %s'%(i, cas_index))
            i = i + 1
            
    return cas_data


# ==============================================================================
def parse_vwcf_file(vwcf_file):
    logging.debug("Parsing vwcf file: %s -------------------------"%(vwcf_file))
    config = {}
    with open(vwcf_file, mode='rb') as file:
        fdata = file.read()

        indx = 0
        dataSize = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Data size: %d"%(dataSize))
        
        if (len(fdata) != dataSize):
            logging.error("Bad data size!")
            sys.exit(-1)
            
        version = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Director version: 0x%04x"%(version))
        
        stageTop = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Stage top: %d"%(stageTop))
        
        stageLeft = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Stage left: %d"%(stageLeft))
        
        
        stageBottom = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Stage bottom: %d"%(stageBottom))
        
        
        stageRight = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Stage right: %d"%(stageRight))
        
        castArrayStart = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Cast array start: %d"%(castArrayStart))
        
        castArrayEnd = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Cast array end: %d"%(castArrayEnd))
        
        currentFrameRate = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Current frame rate?: %d"%(currentFrameRate))
        
        indx += 9
        stageColor = int(fdata[indx])
        indx += 1
        
        logging.debug("Stage color: %d"%(stageColor))

        version_major = ((version >> 8) & 0xFF)
        version_minor = ( version       & 0xFF)
        
        if version_major == 4:
            # Director 6 or lower version
            if version_minor < 0xC0:
                version = 'dir4'
                
            elif version_minor < 0xC6:
                version = 'dir5'
            
            else:
                version = 'dir6'
            
        elif version_major == 5:
            # Director 7
            version = 'dir7'
            
        elif version_major == 7:
            # Director 8 or MX
            if version_minor <= 0x3A:
                version = 'dir8'
                
            elif version_minor <= 0x42:
                version = 'dirMX'
            
            else:
                version = 'unknown'
        
        elif version_major == 0x16 and version_minor == 0x3C:
            # When the Director file is published the version
            # is always 0x163C
            version = 'published'
            
        else:
            version = 'unknown'
            
        logging.info("Director version: %s"%(version))
        
        # The default palette position depends on the director version
        if version == 'dir4': 
            indx = 0x46
            palette = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
            palette = get_palette(palette)
        elif version == 'dir5':
            indx = 0x4E
            palette = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
            palette = get_palette(palette)            
        else:
            palette = 'unknonw'
            
            
        logging.debug("palette (%d): %s"%(indx, palette))
        
        
        config['version'] = version
        config['stageTop'] = stageTop
        config['stageLeft'] = stageLeft
        config['stageBottom'] = stageBottom
        config['stageRight'] = stageRight
        config['castArrayStart'] = castArrayStart
        config['castArrayEnd'] = castArrayEnd
        config['currentFrameRate'] = currentFrameRate
        config['stageColor'] = stageColor
        config['palette'] = palette
        
    
    
    return config

# ==============================================================================
def parse_lctx_file(lctx_file):
    logging.debug("Parsing lctx file: %s -------------------------"%(lctx_file))
    lctx_data = []

    with open(lctx_file, mode='rb') as file:
        fdata = file.read()

        indx = 0
        unk = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Unknown: %08x"%(unk))
        
        unk = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Unknown: %08x"%(unk))
        
        nscripts = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("N Scripts: %d"%(nscripts))
        
        nscripts2 = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("N Scripts: %d"%(nscripts2))
        
        scr_idx = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Scripts Index: %08x"%(scr_idx))
        
        indx = scr_idx
        for i in range(0, nscripts):
            key = struct.unpack(">I", fdata[(indx):(indx+4)])[0]
            indx = indx + 4
            logging.debug("Key: %08x"%(key))
            
            scrfile = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
            indx = indx + 4
            logging.debug("Script file: %08x"%(scrfile))
            lctx_data.append(scrfile)
            
            unk = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
            indx = indx + 4
            logging.debug("Unknown: %08x"%(unk))
            
            
    return lctx_data

# ==============================================================================
def parse_cast_file(cast_file, kelm, dest_dir, lctx_elements, lnam_file):
    logging.debug("Parsing cast file: %s -------------------------"%(cast_file))

    with open(cast_file, mode='rb') as file:
        fdata = file.read()

        castData = {}
        
        idx = 0
        cast_bit_order = '>'
        data_type = struct.unpack(cast_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4
        
        scridx = 0
        
        header_size = 0
        additional_size = 0
        
        if (data_type & 0xFFFFFF00) != 0:
            # Director 4 structure
            logging.debug("Director 4 CASt file!")
            idx -= 4
            
            header_size = struct.unpack(cast_bit_order+"h", fdata[idx:idx+2])[0]
            idx += 2
            logging.debug("header_size = %04x"%(header_size))
            
            additional_size = struct.unpack(cast_bit_order+"i", fdata[idx:idx+4])[0]
            idx += 4
            logging.debug("additional_size = %08x"%(additional_size))
            
            if 6 + header_size + additional_size != len(fdata):
                logging.error("Bad data size! (%d != %d)"%(6 + header_size + additional_size, len(fdata)))
                sys.exit(-1)
                
            data_type = int(fdata[idx])
            idx += 1
            logging.debug("data_type = %02x"%(data_type))
            
            header_data = fdata[idx:idx + header_size - 1]
            idx += header_size - 1
            
            basic_data = fdata[idx:idx + additional_size]
            idx += additional_size
            
        else:
            # Director 5 structure
            logging.debug("data_type = %08x"%(data_type))
        
            additional_size = struct.unpack(cast_bit_order+"i", fdata[idx:idx+4])[0]
            idx += 4
            logging.debug("additional_size = %08x"%(additional_size))

            header_size =  struct.unpack(cast_bit_order+"i", fdata[idx:idx+4])[0]
            idx += 4
            logging.debug("header_size = %08x"%(header_size))
            
            if 12 + header_size + additional_size != len(fdata):
                logging.error("Bad data size! (%d != %d)"%(12 + header_size + additional_size, len(fdata)))
                sys.exit(-1)
            
            basic_data = fdata[idx:idx + additional_size]
            idx += additional_size
            
            header_data = fdata[idx:idx + header_size]
            idx += header_size

        castData['content'] = {}
        if additional_size > 0:
            # Parse main data
            idx = 0
            contentMarker =  struct.unpack(cast_bit_order+"i", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("contentMarker? = %08x"%(contentMarker))
            
            if contentMarker != 0x00000014:
                logging.error("Bad content marker %08x"%(contentMarker))
                sys.exit(-1)
            
            # Content found!
            castData['content']['basic'] = []
            
            script_key =  struct.unpack(">I", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("basic_data00 = %08x"%(script_key))

            basic_data01 =  struct.unpack(cast_bit_order+"i", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("basic_data01 = %08x"%(basic_data01))

            basic_data02 =  struct.unpack(cast_bit_order+"i", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("basic_data02 = %08x"%(basic_data02))

            script_index =  struct.unpack(cast_bit_order+"i", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("script_index: %08x"%(script_index))
            
            castData['content']['basic'].append('0x%08x'%(script_key & 0xFFFFFFFF))
            castData['content']['basic'].append('0x%08x'%(basic_data01 & 0xFFFFFFFF))
            castData['content']['basic'].append('0x%08x'%(basic_data02 & 0xFFFFFFFF))
            castData['content']['basic'].append('0x%08x'%(script_index & 0xFFFFFFFF))
            
            scridx = script_index

            nstruct =  struct.unpack(cast_bit_order+"h", basic_data[idx:idx+2])[0]
            idx += 2
            logging.debug("number of structures contained = %d"%(nstruct))

            if nstruct > 0:
                castData['content']['extra'] = []
            
                struct_indx = []
                for i in range(0, nstruct+1):
                    stindx =  struct.unpack(cast_bit_order+"i", basic_data[idx:idx+4])[0]
                    idx += 4
                    logging.debug("stindx[%d] = %08x"%(i, stindx))
                    struct_indx.append(stindx)

                base_dir = idx
                for i in range(0, nstruct):
                    stlen = struct_indx[i+1] - struct_indx[i]
                    logging.debug("The %d element of the structure is %d bytes long"%(i, stlen))
                    if stlen > 0:
                        stdata = basic_data[idx:idx+stlen]
                        idx += stlen
                        
                        encodedBytes = base64.b64encode(stdata)
                        encodedStr = encodedBytes.decode('ascii')
                        
                        castData['content']['extra'].append(encodedStr)
                    else:
                        castData['content']['extra'].append('')

                # Check if there is a CAST member script
                if len(castData['content']['extra']) > 0 and castData['content']['extra'][0] != '':
                    with open(os.path.join(dest_dir, 'member.lingo'), 'wb') as cfile:
                        cfile.write(base64.b64decode(castData['content']['extra'][0]))

                # Check if there is a CAST member name
                if len(castData['content']['extra']) > 1 and castData['content']['extra'][1] != '':
                    stdata = base64.b64decode(castData['content']['extra'][1])
                    nchars = int(stdata[0])
                    cast_elm_name = stdata[1:nchars+1].decode('ISO-8859-1')
                    cast_elm_name = re.sub(r"[^A-Za-z0-9\-_\. ]", "_", cast_elm_name)
                    castData['name'] = cast_elm_name
                    logging.debug("Cast member name: '%s'"%(cast_elm_name))
                else:
                    castData['name'] = ''
        
        copyfile(cast_file, os.path.join(dest_dir, os.path.basename(cast_file)))
        logging.debug("%s: data_type = %s"%(cast_file, data_type))
        
        # Parse header data
        idx = 0
        if data_type == DIR_IMAGE_TYPE:
            # Director bitmap type
            logging.info("%s: is a bitmap file"%(cast_file))
            castData['type'] = 'bitmap'
            
            flags =  int(header_data[idx])
            idx += 1
            logging.debug("flags = %s"%(flags))

            bmp_bpp_val =  int(header_data[idx])
            idx += 1
            
            bmp_bpp = 8
            if bmp_bpp_val == 0x80:
                # 8 bit per pixel image
                bmp_bpp = 8
                
            elif bmp_bpp_val == 0x81:
                # 4 bit per pixel image
                bmp_bpp = 4

            elif bmp_bpp_val == 0x82:
                # 8 bit per pixel image
                bmp_bpp = 8

            elif bmp_bpp_val == 0x84:
                # 16 bit per pixel image
                bmp_bpp = 16

            elif bmp_bpp_val == 0x85:
                # 16 bit per pixel image (MAC format)
                bmp_bpp = 16

            elif bmp_bpp_val == 0x8A:
                # 24 bit per pixel image
                bmp_bpp = 24

            elif bmp_bpp_val == 0x0:
                # 2 bit per pixel image (Black and White)
                bmp_bpp = 2               
                
            else:
                logging.warn("Unknown BPP value: %s"%(bmp_bpp_val))

            logging.debug("bmp_bpp = %s"%(bmp_bpp)) 


            unknown_11 =  int(header_data[idx])
            idx += 1                
            logging.debug("unknown_11 = %s"%(unknown_11)) 

            h_padding =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("h_padding = %s"%(h_padding)) 

            w_padding =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("w_padding = %s"%(w_padding)) 

            bmp_height =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2                
            logging.debug("bmp_height = %s"%(bmp_height)) 

            bmp_width =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2                
            logging.debug("bmp_width = %s"%(bmp_width)) 

            top =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("top = %s"%(top)) 

            left =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("left = %s"%(left)) 

            bottom =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("bottom = %s"%(bottom)) 

            right =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("right = %s"%(right)) 
            
            locV =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("locV = %s"%(locV)) 
            
            locH =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("locH = %s"%(locH))

            palette = 'systemMac'
            if (len(header_data) > 24):
                bitdepth =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
                idx += 2
                logging.debug("bitdepth = %s"%(bitdepth))
                if bitdepth > bmp_bpp:
                    bmp_bpp = bitdepth

                palette = struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
                palette_txt =  get_palette(palette)
                idx += 2
                logging.debug("palette_txt = %s"%(palette_txt))
                

            castData['height'] = bmp_height
            castData['width'] = bmp_width
            castData['top'] = top
            castData['left'] = left
            castData['bottom'] = bottom
            castData['right'] = right            
            castData['h_padding'] = h_padding
            castData['w_padding'] = w_padding
            castData['locH'] = locH
            castData['locV'] = locV
            castData['depth'] = bmp_bpp
            if bmp_bpp == 8:
                castData['palette'] = palette
                castData['palette_txt'] = palette_txt
            
            for f in kelm:
                if f.endswith('.BITD'):            
                    castData['fileName'] = replace_ext(f, 'png')
                 
                if f.endswith('.THUM'):            
                    castData['thumbnailFileName'] = replace_ext(f, 'png')
                    
        elif data_type == DIR_SND_TYPE:
            # Director sound type
            logging.info("%s: is a sound file"%(cast_file))
            castData['type'] = 'sound'
            castData['loop'] = (basic_data02 != 0x10)
            for f in kelm:
                if f.endswith('.snd_'):             
                    castData['fileName'] = replace_ext(f, 'mp3')


        elif data_type == DIR_LSCR_TYPE:
            # Director Lingo Script reference
            logging.info("%s: is a script reference file"%(cast_file))
            castData['type'] = 'script'
            
        
        elif data_type == DIR_PUSH_BUTTON_TYPE:
            logging.info("%s: is a push button"%(cast_file))
            castData['type'] = 'button'
            
            unknown1 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown1 = %s"%(unknown1)) 
            
            unknown2 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown2 = %s"%(unknown2))             
            
            text_alignment =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            
            if text_alignment == 0:
                text_alignment = 'left'
            elif text_alignment == 1:
                text_alignment = 'center'
            elif text_alignment == -1:
                text_alignment = 'right'
            else:
                logging.warn("Unknown text alignment = %s"%(text_alignment))  
            
            logging.debug("text_alignment = %s"%(text_alignment))               
            
            bgcolor_red =  int(header_data[idx])
            idx += 1            
            logging.debug("bgcolor_red = %s"%(bgcolor_red))               
            
            unknown4 =  int(header_data[idx])
            idx += 1   
            logging.debug("unknown4 = %s"%(unknown4))               
            
            bgcolor_green =  int(header_data[idx])
            idx += 1            
            logging.debug("bgcolor_green = %s"%(bgcolor_green))               
            
            unknown5 =  int(header_data[idx])
            idx += 1   
            logging.debug("unknown5 = %s"%(unknown5))              
            
            bgcolor_blue =  int(header_data[idx])
            idx += 1            
            logging.debug("bgcolor_blue = %s"%(bgcolor_blue))               
            
            unknown6 =  int(header_data[idx])
            idx += 1   
            logging.debug("unknown6 = %s"%(unknown6))              
            
            unknown7 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown7 = %s"%(unknown7))             
            
            unknown8 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown8 = %s"%(unknown8))             
            
            unknown9 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown9 = %s"%(unknown9))            
            
            unknown10 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown10 = %s"%(unknown10))             
            
            unknown11 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown11 = %s"%(unknown11))  
            
            unknown12 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown12 = %s"%(unknown12))  
            
            unknown13 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown13 = %s"%(unknown13))  
            
            unknown14 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown14 = %s"%(unknown14))  
            
            buttonType =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            if buttonType == 1:
                buttonType = 'pushButton'
            if buttonType == 2:
                buttonType = 'checkBox'
            if buttonType == 3:
                buttonType = 'radioButton'
            
            logging.debug("buttonType = %s"%(buttonType))              
            
            castData['backgroundColor'] = '#%0.2X%0.2X%0.2X'%(
                bgcolor_red, bgcolor_green, bgcolor_blue)
            castData['alignment'] = text_alignment
            castData['buttonType'] = buttonType
            
            
            
        elif data_type == DIR_TEXT_INPUT_TYPE:
            logging.info("%s: is a text input field"%(cast_file))
            castData['type'] = 'field'            

            border =  int(header_data[idx])
            idx += 1            
            logging.debug("border = %s"%(border))  
            
            margin =  int(header_data[idx])
            idx += 1            
            logging.debug("margin = %s"%(margin))               

            boxDropShadow =  int(header_data[idx])
            idx += 1            
            logging.debug("boxDropShadow = %s"%(boxDropShadow))               

            boxType =  int(header_data[idx])
            idx += 1            
            logging.debug("boxType = %s"%(boxType))               
            
            if boxType == 0:
                boxType = 'adjust'
            if boxType == 1:
                boxType = 'scroll'
            if boxType == 2:
                boxType = 'fixed'
            if boxType == 3:
                boxType = 'limit'
            
            logging.debug("boxType = %s"%(boxType))         
            
            alignment =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            
            if alignment == 0:
                alignment = 'left'
            elif alignment == 1:
                alignment = 'center'
            elif alignment == -1:
                alignment = 'right'
            else:
                logging.warn("Unknown text alignment = %s"%(alignment))  
            
            logging.debug("alignment = %s"%(alignment))            
            
            bgcolor_red =  int(header_data[idx])
            idx += 1            
            logging.debug("bgcolor_red = %s"%(bgcolor_red))               
            
            unknown4 =  int(header_data[idx])
            idx += 1   
            logging.debug("unknown4 = %s"%(unknown4))               
            
            bgcolor_green =  int(header_data[idx])
            idx += 1            
            logging.debug("bgcolor_green = %s"%(bgcolor_green))               
            
            unknown5 =  int(header_data[idx])
            idx += 1   
            logging.debug("unknown5 = %s"%(unknown5))              
            
            bgcolor_blue =  int(header_data[idx])
            idx += 1            
            logging.debug("bgcolor_blue = %s"%(bgcolor_blue))               
            
            unknown6 =  int(header_data[idx])
            idx += 1   
            logging.debug("unknown6 = %s"%(unknown6))                          
            
            unknown7 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown7 = %s"%(unknown7))
            
            top =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("top = %s"%(top)) 

            left =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("left = %s"%(left)) 

            bottom =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("bottom = %s"%(bottom)) 

            right =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("right = %s"%(right)) 
            
            pageHeight =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("pageHeight = %s"%(pageHeight))

            dropShadow =  int(header_data[idx])
            idx += 1            
            logging.debug("dropShadow = %s"%(dropShadow))            
            
            options =  int(header_data[idx])
            idx += 1            
            logging.debug("options = %s"%(options))
            
            wordWrap = True
            editable = False
            autoTab = False
            if options & 0x4:
                wordWrap = False
            if options & 0x1:
                editable = True                
            if options & 0x2:
                autoTab = True
            
            scrollHeight =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("scrollHeight = %s"%(scrollHeight))             
            
            castData['wordWrap'] = wordWrap    
            castData['boxType'] = boxType    
            castData['editable'] = editable    
            castData['autoTab'] = autoTab
            castData['alignment'] = alignment 
            castData['border'] = border 
            castData['margin'] = margin 
            castData['boxDropShadow'] = boxDropShadow 
            castData['dropShadow'] = dropShadow 
            castData['backgroundColor'] = '#%0.2X%0.2X%0.2X'%(
                bgcolor_red, bgcolor_green, bgcolor_blue)
            castData['height'] = bottom - top 
            castData['width'] = right - left
            castData['pageHeight'] = pageHeight
            castData['scrollHeight'] = scrollHeight
            
        elif data_type == DIR_TEXT_TYPE:
            logging.info("%s: is a text label"%(cast_file))
            castData['type'] = 'richText'
            
            h_padding =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("h_padding = %s"%(h_padding)) 

            w_padding =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("w_padding = %s"%(w_padding)) 

            txt_height =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2                
            logging.debug("txt_height = %s"%(txt_height)) 

            txt_width =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2                
            logging.debug("txt_width = %s"%(txt_width)) 

            top =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("top = %s"%(top)) 

            left =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("left = %s"%(left)) 

            bottom =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("bottom = %s"%(bottom)) 

            right =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("right = %s"%(right)) 
            
            antialias =  int(header_data[idx])
            idx += 1            
            if antialias==0:
                antialias = False
            else:
                antialias = True                
            logging.debug("antiAlias = %s"%(antialias))
            
            boxType =  int(header_data[idx])
            idx += 1            
            logging.debug("boxType = %s"%(boxType))               
            
            if boxType == 0:
                boxType = 'adjust'
            if boxType == 1:
                boxType = 'scroll'
            if boxType == 2:
                boxType = 'fixed'
            if boxType == 3:
                boxType = 'limit'
            
            unknown2 =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("unknown2 = %s"%(unknown2))

            anti_threshold =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            if anti_threshold < 0:
                anti_threshold = 0
            logging.debug("anti_threshold = %s"%(anti_threshold))
            
            
            castData['boxType'] = boxType
            castData['antiAlias'] = antialias
            castData['antiAliasThreshold'] = anti_threshold
            castData['width'] = txt_width
            castData['height'] = txt_height
            castData['top'] = top
            castData['left'] = left
            castData['bottom'] = bottom
            castData['right'] = right            
            castData['h_padding'] = h_padding
            castData['w_padding'] = w_padding
                
            for f in kelm:
                if f.endswith('.RTE1'):            
                    src = os.path.join(os.path.dirname(cast_file), f)
                    fdata = ''
                    with open(src, mode='rb') as kfile:
                        fdata = kfile.read()
                    castData['text'] = fdata.decode("ISO-8859-1")

                if f.endswith('.RTE2'):            
                    castData['fileName'] = replace_ext(f, 'png')            
            
        elif data_type == DIR_SHAPE_TYPE:
            logging.info("%s: is a shape"%(cast_file))
            castData['type'] = 'shape'
            
            unknown00 =  int(header_data[idx])
            idx += 1                
            logging.debug("unknown00 = %s"%(unknown00)) 

            shape_type =  get_shape_type(struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0])
            idx += 2
            logging.debug("shape_type = %s"%(shape_type))
            
            top =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("top = %s"%(top))
            
            left =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("left = %s"%(left))
            
            bottom =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("bottom = %s"%(bottom))            
            
            right =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("right = %s"%(right))             
            
            unknown02 =  int(header_data[idx])
            idx += 1                
            logging.debug("unknown02 = %s"%(unknown02))             
            
            pattern =  int(header_data[idx])
            idx += 1                
            logging.debug("pattern = %s"%(pattern))            
            
            fgColor =  int(header_data[idx])
            idx += 1                
            logging.debug("fgColor = %s"%(fgColor))                
            
            bgColor =  int(header_data[idx])
            idx += 1                
            logging.debug("bgColor = %s"%(bgColor))              
            
            filled =  int(header_data[idx])
            idx += 1                
            logging.debug("filled = %s"%(filled))
            
            line_width =  int(header_data[idx]) - 1
            idx += 1                
            logging.debug("line_width = %s"%(line_width))                 
            
            unknown08 =  int(header_data[idx])
            idx += 1                
            logging.debug("unknown08 = %s"%(unknown08))             
            
            castData['shapeType'] = shape_type            
            castData['top'] = top            
            castData['left'] = left            
            castData['bottom'] = bottom            
            castData['right'] = right
            castData['pattern'] = pattern     
            castData['foreColor'] = fgColor     
            castData['backColor'] = bgColor     
            castData['filled'] = filled
            castData['lineSize'] = line_width
            
        elif data_type == DIR_CLUT_TYPE:
            logging.info("%s: is a palette"%(cast_file))
            castData['type'] = 'palette'
            
        elif data_type == DIR_TRAN_TYPE:
            logging.info("%s: is a transition"%(cast_file))
            castData['type'] = 'transition'
            
            smoothness =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("smoothness = %s"%(smoothness))
            
            transition =  struct.unpack(cast_bit_order+"B", header_data[idx])[0]
            idx += 1                
            logging.debug("transition = %s"%(transition)) 
            
            stage_or_area =  struct.unpack(cast_bit_order+"B", header_data[idx])[0]
            idx += 1                
            logging.debug("stage_or_area = %s"%(stage_or_area))
            
            # Duration in millisenconds
            duration =  struct.unpack(cast_bit_order+"h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("duration = %s"%(duration))
            
            castData['content']['transition'] = {}
            castData['content']['transition']['type'] = get_transtition(transition)
            castData['content']['transition']['smoothness'] = smoothness
            castData['content']['transition']['duration'] = duration
            castData['content']['transition']['in_changing_area'] = (stage_or_area == 2)

        else:
            logging.warn("%s: data_type unknown (%s)!"%(cast_file, data_type))
            castData['type'] = 'unknown'
        
        # Decompile script (if any)
        if scridx > 0:
            logging.debug("Script index: %d"%(scridx))
            if scridx <= 0 or lctx_elements[scridx - 1] < 0:
                logging.debug("Empty script file!")
            else:
                script_file = "%s.Lscr"%(lctx_elements[scridx - 1])
                logging.debug("Script file: %s"%(script_file))

                src = os.path.join(os.path.dirname(cast_file), script_file)
                dst = os.path.join(dest_dir, script_file)
                if os.path.isfile(src):
                    copyfile(src, dst)
                else:
                    logging.warn("There is no %s file (maybe empty file)"%(src))

                if lnam_file is not None:
                    cmd = '%slscr2lingo %s %s %s'%(
                        basepath, # Scripts path
                        dest_dir, # work directory
                        script_file, # script file name
                        lnam_file
                    )
                    logging.debug("======================================================")
                    logging.debug("Decompiling lingo script by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)
                    
                    codefile = os.path.join(dest_dir, replace_ext(script_file, 'lingo'))
                    if os.path.isfile(codefile):
                        logging.debug("Decompiled code file: %s"%(codefile))
                        with open(codefile, mode='rb') as cfile:
                            castData['code'] = base64.b64encode(cfile.read()).decode()

                    cmd = '%slscr2js %s %s %s'%(
                        basepath, # Scripts path
                        dest_dir, # work directory
                        script_file, # script file name
                        lnam_file
                    )
                    logging.debug("======================================================")
                    logging.debug("Transpiling lingo script by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)
                    
                    codefile = os.path.join(dest_dir, replace_ext(script_file, 'js'))
                    if os.path.isfile(codefile):
                        logging.debug("Decompiled code file: %s"%(codefile))
                        with open(codefile, mode='rb') as cfile:
                            castData['jscode'] = base64.b64encode(cfile.read()).decode()

        
        
        # Write CAST data to JSON file
        with open(os.path.join(dest_dir, 'data.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(castData, indent=4, sort_keys=True).encode('utf-8'))
        
        if kelm is None or len(kelm) <= 0:
            logging.info("%s: has no related data!"%(cast_file))
        else:
            for f in kelm:
                logging.debug("Related file: %s"%(f))
                src = os.path.join(os.path.dirname(cast_file), f)
                dst = os.path.join(dest_dir, f)
                if os.path.isfile(src):
                    copyfile(src, dst)
                else:
                    logging.warn("There is no %s file (maybe empty file)"%(src))

                if f.endswith('.BITD'):
                    cmd = '%s/bitd2bmp %s %s'%(
                        os.path.dirname(sys.argv[0]), # Scripts path
                        dest_dir, # work directory
                        f # BITD file name
                    )
                    logging.debug("======================================================")
                    logging.debug("Extracting image by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)
                    
                if f.endswith('.snd_'):
                    cmd = '%s/snd2wav %s %s'%(
                        os.path.dirname(sys.argv[0]), # Scripts path
                        dest_dir, # work directory
                        f # snd file name
                    )
                    logging.debug("======================================================")
                    logging.debug("Extracting sound by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)
                    
                if f.endswith('.STXT'):
                    cmd = '%s/stxt2json %s "%s"'%(
                        os.path.dirname(sys.argv[0]), # Scripts path
                        dest_dir, # work directory
                        f # stxt file name
                    )
                    logging.debug("======================================================")
                    logging.debug("Extracting text information by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)

                if f.endswith('.RTE2'):
                    cmd = '%s/rte22bmp %s "%s"'%(
                        os.path.dirname(sys.argv[0]), # Scripts path
                        dest_dir, # work directory
                        f # rte2 file name
                    )
                    logging.debug("======================================================")
                    logging.debug("Extracting image by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)
                        
                if f.endswith('.CLUT'):
                    cmd = '%s/clut2json %s %s'%(
                        os.path.dirname(sys.argv[0]), # Scripts path
                        dest_dir, # work directory
                        f # CLUT file name
                    )
                    logging.debug("======================================================")
                    logging.debug("Extracting palette information by using the command:")        
                    logging.debug(cmd)
                    logging.debug("------------------------------------------------------")
                    os.system(cmd)


# ==============================================================================
def main():
    global bit_order_type, bit_order

    if len(sys.argv) < 3:
        print("USAGE: casxtract [pc|mac] <base directory>")

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

        if not os.path.isdir(os.path.join(sys.argv[2], BINDIR)):
            logging.error(" '%s' is not a directory"%(os.path.join(sys.argv[2], BINDIR)))
            sys.exit(-1)

        if not os.path.isdir(os.path.join(sys.argv[2], CASDIR)):
            os.mkdir(os.path.join(sys.argv[2], CASDIR))
        
        # Look for KEY_ and CAS_ files
        key_file = None
        cas_file = None
        lctx_file = None
        lnam_file = None
        
        sord_file = None
        vwsc_file = None
        
        for f in os.listdir(os.path.join(sys.argv[2], BINDIR)):
            if f.endswith('KEY_'):
                key_file = f
            
            if f.endswith('CAS_'):
                cas_file = f
                
            if (f.endswith('Lctx') or f.endswith('LctX')):
                lctx_file = f
                
            if f.endswith('Lnam'):
                lnam_file = f
            
            if f.endswith('Sord'):
                sord_file = f
            
            if (f.endswith('VWCF') or f.endswith('DRCF')):
                vwcf_file = f
                
        if key_file is None:
            logging.error('Can not find a KEY_ file!')
            sys.exit(-1)

        if cas_file is None:
            logging.error('Can not find a CAS_ file!')
            sys.exit(-1)

        if lnam_file is None:
            logging.warn('Can not find a Lnam file!')
        else:
            lnam_file = os.path.join(sys.argv[2], BINDIR, lnam_file)
            
        if sord_file is None:
            logging.error('Can not find a Sord file!')
            sys.exit(-1)
            
        if vwcf_file is None:
            logging.error('Can not find a VWCF or DRCF file!')
            sys.exit(-1)
        
        config = parse_vwcf_file(os.path.join(sys.argv[2], BINDIR, vwcf_file))
        # Write config data to JSON file
        with open(os.path.join(sys.argv[2], CASDIR, 'config.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(config, indent=4, sort_keys=True).encode('utf-8'))
        
        cas_elements = parse_cas_file(os.path.join(sys.argv[2], BINDIR, cas_file))
        key_elements = parse_key_file(os.path.join(sys.argv[2], BINDIR, key_file))
        if lctx_file is None:
            logging.warn('Can not find a Lctx file!')
            lctx_elements = []
        else:
            lctx_elements = parse_lctx_file(os.path.join(sys.argv[2], BINDIR, lctx_file))
        
        
        logging.info('There are %i elements in the casting!'%(len(cas_elements)))
        
        # Extract casting elements
        for elm in range(1, len(cas_elements)+1):
            # Create directory
            if not os.path.isdir(os.path.join(sys.argv[2], CASDIR, str(elm))):
                os.mkdir(os.path.join(sys.argv[2], CASDIR, str(elm)))
            
            # Read CASt file
            kelm = []
            cas_index = (cas_elements[elm - 1])
            if cas_index in key_elements:
                kelm = key_elements[cas_index]
            
            fname = '%i.CASt'%(int(cas_elements[elm - 1], 16))
            if os.path.isfile(os.path.join(sys.argv[2], BINDIR, fname)):
                logging.info('Casting element number %i is %s file!'%(elm, fname))
                parse_cast_file(os.path.join(sys.argv[2], BINDIR, fname), kelm,
                                os.path.join(sys.argv[2], CASDIR, str(elm)),
                               lctx_elements, lnam_file)
            else:
                logging.warn('File %s for casting element %i does not exists!'%(fname, elm))

