# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, Dict
import struct
import logging
from ..riff import parse_chunk_id
from ..lingosrc.util import get_keys, Dictionary, vsprintf

#
# File reference class
# 
# =============================================================================
class FileReference(Dictionary):
    """This class represents a reference to a
    Director File Memory MAP Resource"""
    
    def __init__(self, chunkID: str, index: int):
        super().__init__()
        self['chunkID'] = chunkID
        self['index'] = index

#
# Reads from KEY data the relationship between casting elements and data files
# =============================================================================
def parse_key_file_data(byte_order: str,
                        fdata: bytes) -> Dict[int, List[FileReference]]:
    """
    Parse a KEY file and return its content.
    
    Parameters
    ----------
    byte_order : str
        Python's struct module byte order.
    fdata : bytes
        The bytes in KEY CAS file that contain the relationship between casting
        members and data files.
        
    Returns
    -------
    Dict[int, List[FileReference]]
        a dictionary of list of FileReference.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    key_data: Dict[int, List[FileReference]] = {}
    indx = 0
    
    # Unknown header data
    unk = struct.unpack(byte_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Unknown: %08x", unk)

    unk = struct.unpack(byte_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Unknown: %08x", unk)

    nelements = struct.unpack(byte_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Number of elements: %08x", nelements)

    for _ in range(nelements-1):
        nfile = struct.unpack(byte_order+"i", fdata[(indx+0):(indx+4)])[0]
        cas_index = struct.unpack(byte_order+"i", fdata[(indx+4):(indx+8)])[0]

        chunkId = parse_chunk_id(fdata, indx+8, byte_order)
        indx = indx + 12
        
        if cas_index > 0 and nfile > 0:
            if not cas_index in get_keys(key_data):
                key_data[cas_index] = []

            key_data[cas_index].append(FileReference(chunkId, nfile))

            key_value = vsprintf("KEY['%08x'] = '%s.%s'",
                                 cas_index, nfile, chunkId)
            logging.debug(key_value)

    return key_data
