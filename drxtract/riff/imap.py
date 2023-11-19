# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

import struct
import logging

#
# Input MAP class
# 
# =============================================================================
class InputMAP:
    """This class represents a Director File Input MAP"""
    
    def __init__(self, count: int, offset: int, file_version: int,
                 reserved: int, unknown: int, reserved2: int):
        self.count: int = count
        self.offset: int = offset
        self.file_version: int = file_version
        self.reserved: int = reserved
        self.unknown: int = unknown
        self.reserved2: int = reserved2

#
# Parse Input MAP file data
# 
# =============================================================================
def parse_imap(fdata: bytes, byte_order: str) -> InputMAP:
    """
    Parse a IMAP file data and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the IMAP file to parse.
    byte_order: str
        Python's struct module byte order.
        
    Returns
    -------
    InputMAP
        an object that contains the data.
        
        
    """
    # Input MAP
    # https://docs.google.com/document/d/1jDBXE4Wv1AEga-o1Wi8xtlNZY4K2fHxW2Xs8RgARrqk/edit#heading=h.dq1rrg8abhxt
    logging.debug("==================================")
    logging.debug(" Parse input map: %d bytes", len(fdata))
    content = struct.unpack(byte_order+"iiihhii", fdata)
    logging.debug("IMAP[0] Memory MAP count: %d", content[0])
    logging.debug("IMAP[1] Memory MAP offset: %d", content[1])
    logging.debug("IMAP[2] Memory MAP file version: %d", content[2])
    logging.debug("IMAP[3] Reserved: %d", content[3])
    logging.debug("IMAP[4] Unknown: %d", content[4])
    logging.debug("IMAP[5] Reserved2: %d", content[5])
    
    return InputMAP(content[0], content[1], content[2], content[3],
                    content[4], content[5])

