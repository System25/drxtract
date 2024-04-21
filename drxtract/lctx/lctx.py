# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
import struct
import logging
from ..key import FileReference


#
# Lingo script reference class
# 
# =============================================================================
class LingoScripReference(FileReference):
    """This class represents a reference to a Lingo script inside
    Director File Memory MAP Resource"""
    
    def __init__(self, key: int, index: int):
        super().__init__('Lscr', index)
        self['key'] = key

#
# Reads from Lctx data the Lingo script index
# =============================================================================
def parse_lctx_file_data(fdata: bytes) -> List[LingoScripReference]:
    """
    Parse a Lctx file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the Lctx file that contains the scripts index inside
        the Director file.
        
    Returns
    -------
    List[LingoScripReference]
        a list of script file references.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    lctx_data: List[LingoScripReference] = []
    indx = 0
    unk = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Unknown: %08x", unk)
    
    unk = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Unknown: %08x", unk)
    
    nscripts = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("N Scripts: %d", nscripts)
    
    nscripts2 = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("N Scripts: %d", nscripts2)
    
    scr_idx = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Scripts Index: %08x", scr_idx)
    
    indx = scr_idx
    for _ in range(0, nscripts):
        key = struct.unpack(">I", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Key: %08x", key)
        
        scrfile = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Script file: %08x", scrfile)
        lctx_data.append(LingoScripReference(key, scrfile))
        
        unk = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        logging.debug("Unknown: %08x", unk)
            
            
    return lctx_data

