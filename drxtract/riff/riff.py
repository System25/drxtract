# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

import struct
import logging
from typing import List
from .riff_chunk import parse_chunk, Chunk, parse_chunk_id
from ..lingosrc.util import vsprintf

MV93_FILE_TYPE = 'MV93'
RIFX_FILE_FORMAT = 'RIFX'
IMAP_FILE_FORMAT = 'imap'
MMAP_FILE_FORMAT = 'mmap'
FREE_FILE_FORMAT = 'free'
JUNK_FILE_FORMAT = 'junk'

RIFX_LE_HEADER = 'XFIR'
MV93_LE_HEADER = '39VM'

#
# RIFF data class
# 
# =============================================================================
class RiffData:
    """This class represents the data inside a RIFF file"""
    
    def __init__(self, byte_order: str):
        self.byte_order: str = byte_order
        self.chunks : List[Chunk] = []

    def get_by_offset(self, offset: int) -> Chunk:
        index: int = 12
        for c in self.chunks:
            if index == offset:
                return c
            l = len(c.data)
            index += 8 + l + (l%2)
            
        raise IndexError('Offset not found')

#
# Parse Input MAP file data
# 
# =============================================================================
def parse_riff(fdata: bytes, offset: int, byte_order: str) -> RiffData:
    """
    Parse a RIFF file data and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the RIFF file.
    offset: int
        Offset to the RIFF file (> 0 in case of EXE file).
    byte_order: str
        Python's struct module byte order.
        
    Returns
    -------
    RiffData
        an object that contains the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    file_format: str = parse_chunk_id(fdata, offset, byte_order)
    logging.info(" File format: %s", file_format)
    if RIFX_FILE_FORMAT != file_format:
        err : str = vsprintf("File format is not %s", RIFX_FILE_FORMAT);
        logging.error(err)
        raise TypeError(err)
    
    # Read file length
    file_length = struct.unpack(byte_order+"i", fdata[offset+4:offset+8])[0]
    logging.info(" File contains %s bytes of information.", file_length)
    
    if len(fdata) != file_length + 8 + offset:
        logging.warning(" Using %d as file length", len(fdata))
    
    # Check Macromedia Director MV93 header
    mv93_format: str = parse_chunk_id(fdata, offset + 8, byte_order)
    logging.info(" Data format: %s", mv93_format)
    if MV93_FILE_TYPE != mv93_format:
        err = vsprintf("Data format is not %s", MV93_FILE_TYPE);
        logging.error(err)
        raise TypeError(err)
    
    riffData : RiffData = RiffData(byte_order)
    index = offset + 12
    while index < len(fdata):
        chunk: Chunk = parse_chunk(fdata, index, byte_order)
        riffData.chunks.append(chunk)
        padding = (len(chunk.data) % 2)
        index = index + 8 + len(chunk.data) + padding
    
    return riffData

#
# Tries to find the RIFF start offset inside a Windows EXE file
# 
# =============================================================================
def find_riff_in_exe(content: bytes) -> int:
    """
    Parse a Windows EXE file and tries to find the offset of the RIFF data.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the EXE file.
        
    Returns
    -------
    Offset
        the offset to the RIFF data structure.
        
    """
    rifx_offset: int = 0
    index: int = content.find(RIFX_LE_HEADER.encode('ascii'))
    found: bool = False
    while index >= 0 and not found:
        rifx_offset += index
        content = content[index:]
        if content[8:12].decode('ascii', errors="replace") == MV93_LE_HEADER:
            found = True
        else:
            content = content[4:]
            rifx_offset += 4
            index = content.find(RIFX_LE_HEADER.encode('ascii'))
    logging.info("Use %s as RIFX index inside EXE", rifx_offset)
    
    return rifx_offset
