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
import logging
import re
import json
import base64
from shutil import copyfile

from .vwcf import parse_vwcf_file_data
from .cas import parse_cas_file_data
from .key import parse_key_file_data
from .lctx import parse_lctx_file_data, LingoScripReference
from .cast import parse_cast_file_data

logging.basicConfig(level=logging.DEBUG)


# Default byte order for MAC
byte_order_type = 'mac'
byte_order = ">"

BINDIR = 'bin'
CASDIR = 'cas'


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
def parse_key_file(byte_order, key_file):
    logging.debug("Parsing key file: %s ---------------------------", key_file)

    with open(key_file, mode='rb') as file:
        fdata = file.read()

        return parse_key_file_data(byte_order, fdata)
    return {}

# ==============================================================================
def parse_cas_file(cas_file):
    logging.debug("Parsing cas file: %s ---------------------------", cas_file)

    with open(cas_file, mode='rb') as file:
        fdata = file.read()

        return parse_cas_file_data(fdata)
            
    return []


# ==============================================================================
def parse_vwcf_file(vwcf_file):
    logging.debug("Parsing vwcf file: %s -------------------------", vwcf_file)
    with open(vwcf_file, mode='rb') as file:
        fdata = file.read()

        return parse_vwcf_file_data(fdata)
    
    return {}

# ==============================================================================
def parse_lctx_file(lctx_file):
    logging.debug("Parsing lctx file: %s -------------------------", lctx_file)

    with open(lctx_file, mode='rb') as file:
        fdata = file.read()

        return parse_lctx_file_data(fdata)
    
    return []
# ==============================================================================
def parse_cast_file(cast_file, kelm, dest_dir, lctx_elements, lnam_file):
    logging.debug("Parsing cast file: %s -------------------------", cast_file)

    with open(cast_file, mode='rb') as file:
        fdata = file.read()

        copyfile(cast_file, os.path.join(dest_dir, os.path.basename(cast_file)))

        castData = parse_cast_file_data(fdata)
        #logging.debug("casData: " + json.dumps(castData))

        # Check if there is a CAST member script
        if (('content' in castData) and ('extra' in castData['content'])
            and len(castData['content']['extra']) > 0
            and castData['content']['extra'][0] != ''):
            with open(os.path.join(dest_dir, 'member.lingo'), 'wb') as cfile:
                cfile.write(base64.b64decode(castData['content']['extra'][0]))

        # Decompile script (if any)
        if ('content' in castData) and ('basic' in castData['content']):
            scridx = castData['content']['basic']['script_index']
        else:
            scridx = 0
        if scridx > 0:
            logging.debug("Script index: %d", scridx)
            if scridx <= 0 or lctx_elements[scridx - 1]['index'] < 0:
                logging.debug("Empty script file!")
            else:
                reference: LingoScripReference = lctx_elements[scridx - 1]
                script_file = "%d.Lscr"%(reference['index'])
                logging.debug("Script file: %s", script_file)

                src = os.path.join(os.path.dirname(cast_file), script_file)
                dst = os.path.join(dest_dir, script_file)
                if os.path.isfile(src):
                    copyfile(src, dst)
                else:
                    logging.warning("There is no %s file (maybe empty file)", src)

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
                        logging.debug("Decompiled code file: %s", codefile)
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
                        logging.debug("Decompiled code file: %s", codefile)
                        with open(codefile, mode='rb') as cfile:
                            castData['jscode'] = base64.b64encode(cfile.read()).decode()
        
        # Write CAST data to JSON file
        with open(os.path.join(dest_dir, 'data.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(castData, indent=4, sort_keys=True
                                    ).encode('utf-8'))
        
        if kelm is None or len(kelm) <= 0:
            logging.info("%s: has no related data!", cast_file)
        else:
            for rf in kelm:
                f = "%s.%s"%(rf['index'], rf['chunkID'])
                f = re.sub(r"[^A-Za-z0-9\-_\.]", "_", f)
                logging.debug("Related file: %s", f)
                src = os.path.join(os.path.dirname(cast_file), f)
                dst = os.path.join(dest_dir, f)
                if os.path.isfile(src):
                    copyfile(src, dst)
                else:
                    logging.warning("There is no %s file (maybe empty file)", src)

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
    global byte_order_type, byte_order

    if len(sys.argv) < 3:
        print("USAGE: casxtract [pc|mac] <base directory>")

    else:
        if sys.argv[1] != 'pc' and sys.argv[1] != 'mac':
            logging.error(" First argument must be 'pc' or 'mac'")
            sys.exit(-1)

        if sys.argv[1] == 'pc':
            byte_order_type = 'pc'
            byte_order = "<"

        if not os.path.isdir(sys.argv[2]):
            logging.error(" '%s' is not a directory", sys.argv[2])
            sys.exit(-1)

        bin_dir = os.path.join(sys.argv[2], BINDIR)
        if not os.path.isdir(bin_dir):
            logging.error(" '%s' is not a directory", bin_dir)
            sys.exit(-1)

        if not os.path.isdir(os.path.join(sys.argv[2], CASDIR)):
            os.mkdir(os.path.join(sys.argv[2], CASDIR))
        
        # Look for KEY_ and CAS_ files
        key_file = None
        cas_file = None
        lctx_file = None
        lnam_file = None
        
        sord_file = None
        
        for f in os.listdir(bin_dir):
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
            logging.warning('Can not find a Lnam file!')
        else:
            lnam_file = os.path.join(bin_dir, lnam_file)
            
        if sord_file is None:
            logging.error('Can not find a Sord file!')
            sys.exit(-1)
            
        if vwcf_file is None:
            logging.error('Can not find a VWCF or DRCF file!')
            sys.exit(-1)
        
        config = parse_vwcf_file(os.path.join(bin_dir, vwcf_file))
        # Write config data to JSON file
        with open(os.path.join(sys.argv[2], CASDIR, 'config.json'), 'wb') as jsfile:
            jsfile.write(json.dumps(config, indent=4, sort_keys=True).encode('utf-8'))
        
        cas_elements = parse_cas_file(os.path.join(bin_dir, cas_file))
        key_elements = parse_key_file(byte_order,
                                      os.path.join(bin_dir, key_file))
        if lctx_file is None:
            logging.warning('Can not find a Lctx file!')
            lctx_elements = []
        else:
            lctx_elements = parse_lctx_file(os.path.join(bin_dir, lctx_file))
        
        
        logging.info('There are %i elements in the casting!', len(cas_elements))
        
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
            
            fname = '%i.CASt'%(cas_elements[elm - 1])
            if os.path.isfile(os.path.join(bin_dir, fname)):
                logging.info('Casting element number %i is %s file!',
                             elm, fname)
                parse_cast_file(os.path.join(bin_dir, fname), kelm,
                                os.path.join(sys.argv[2], CASDIR, str(elm)),
                               lctx_elements, lnam_file)
            else:
                logging.warning('File %s for casting element %i does not '
                                + 'exists!', fname, elm)

if __name__ == '__main__':
    main()

