# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
import struct
import logging

#
# Reads from CAS data the basic casting information
# =============================================================================
def parse_cas_file_data(fdata: bytes) -> List[int]:
    """
    Parse a CAS file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the CAS file that contain the casting element index inside
        the Director file.
        
    Returns
    -------
    List[int]
        a list of file index.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    indx = 0
    i = 0
    cas_data: List[int] = []
    while len(fdata) >= indx + 4:
        cas_index = struct.unpack(">i", fdata[(indx):(indx+4)])[0]
        indx = indx + 4
        cas_data.append(cas_index)
        logging.debug('CAS[%d] = %08x', i, cas_index)
        i = i + 1
    return cas_data
