# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
import struct
import logging

#
# Parse LNAM file data
# 
# =============================================================================
def parse_lnam_file_data(fdata: bytes) -> List[str]:
    """
    Parse a LNAM file data and return the list of names inside it.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
        
    Returns
    -------
    list
        a list of strings that contains variable names and method names.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    name_list = []

    indx = 0
    lnam_bit_order = '>'

    logging.debug("====== parse LNAM file ==================================")
    # Unknown header data
    unk = struct.unpack(lnam_bit_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Unknown: %08x"%(unk))

    unk = struct.unpack(lnam_bit_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("Unknown: %08x"%(unk))

    filesize = struct.unpack(lnam_bit_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("filesize: %08x"%(filesize))

    filesize_cp = struct.unpack(lnam_bit_order+"i", fdata[(indx):(indx+4)])[0]
    indx = indx + 4
    logging.debug("filesize_cp: %08x"%(filesize_cp))

    unk = struct.unpack(lnam_bit_order+"h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Unknown: %08x"%(unk))

    nnames = struct.unpack(lnam_bit_order+"h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Number of names: %s"%(nnames))


    if filesize_cp != filesize:
        logging.error("Bad file size! (%s != %s)"%(filesize_cp, filesize))
        raise ValueError("Bad file size!")



    for i in range(0, nnames):
        nbytes = int(fdata[indx])
        indx = indx + 1

        name = fdata[indx:(indx + nbytes)].decode('ISO-8859-1')
        indx = indx + nbytes

        name_list.append(name)
        logging.debug("name_list[%s] = %s"%(i, name))
                
    return name_list

