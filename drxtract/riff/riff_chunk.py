# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

import struct
import logging
from ..lingosrc.util import to_ascii_string

#
# RIFF chunk class
# https://en.wikipedia.org/wiki/Resource_Interchange_File_Format
# 
# =============================================================================
class Chunk:
    """This class represents a RIFF chunk"""
    
    def __init__(self, identifier: str, data: bytes):
        self.identifier: str = identifier
        self.data: bytes = data


#
# Parse ASCII identifier
# 
# =============================================================================
def parse_chunk_id(riff_data: bytes, position: int, byte_order: str) -> str:
    """
    Parse a 4 bytes RIFF file chunk ASCII identifier and return its content
    as printable ASCII chars.
    
    Parameters
    ----------
    riff_data : bytes
        The bytes inside the RIFF file to parse.
    position : int
        The start position of the chunk to parse.
    byte_order : str
        Python's struct module byte order.
        
    Returns
    -------
    str
        a 4 ASCII chars ID.
        
        
    """
    index: int = position
    block_type = struct.unpack("cccc", riff_data[index:(index+4)])
    identifier: str = ''
    start = 0
    stop = 4
    step = 1
    if byte_order == "<":
        start = 3
        stop = -1
        step = -1
        
    for i in range(start, stop, step):
        c = to_ascii_string(block_type[i])
        if (c >= ' ' and c <= 'z'):
            identifier = identifier + c
        else:
            identifier = identifier + '_'
            
    return identifier

#
# Parse RIFF chunk
# 
# =============================================================================
def parse_chunk(riff_data: bytes, position: int, byte_order: str) -> Chunk:
    """
    Parse a RIFF file chunk and return its content.
    
    Parameters
    ----------
    riff_data : bytes
        The bytes inside the RIFF file to parse.
    position : int
        The start position of the chunk to parse.
    byte_order : str
        Python's struct module byte order.
        
    Returns
    -------
    Chunk
        an object that contains the data.
        
        
    """
    bt: str = parse_chunk_id(riff_data, position, byte_order)
    logging.info("==================================")
    logging.info(" Block type: %s", bt)

    block_size: int = struct.unpack(byte_order+"i", riff_data[
        (position+4):(position+8)])[0]
    logging.info(" Block size: %d", block_size)

    block_data : bytes = riff_data[(position+8):(position + 8 + block_size)]
    
    return Chunk(bt, block_data)

