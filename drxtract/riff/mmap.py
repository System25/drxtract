# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

import struct
import logging
from typing import List
from .riff_chunk import parse_chunk_id

#
# Memory MAP resource class
# 
# =============================================================================
class MMapResource:
    """This class represents a Director File Memory MAP Resource"""
    
    def __init__(self, chunkID: str, size: int, offset: int, flags: int,
                 unused: int, nextResourceID: int):
        self.chunkID: str = chunkID
        self.size: int = size
        self.offset: int = offset
        self.flags: int = flags
        self.unused: int = unused
        self.nextResourceID: int = nextResourceID

#
# Memory MAP class
# 
# =============================================================================
class MemoryMAP:
    """This class represents a Director File Memory MAP"""
    
    def __init__(self, propertiesSize: int, resourceSize: int,
                 maxResourceCount: int, usedResourceCount: int,
                 firstJunkResourceID: int, oldMemoryMapResourceID: int,
                 firstFreeResourceID: int):
        self.propertiesSize: int = propertiesSize
        self.resourceSize: int = resourceSize
        self.maxResourceCount: int = maxResourceCount
        self.usedResourceCount: int = usedResourceCount
        self.firstJunkResourceID: int = firstJunkResourceID
        self.oldMemoryMapResourceID: int = oldMemoryMapResourceID
        self.firstFreeResourceID: int = firstFreeResourceID
        self.resources: List[MMapResource] = []

#
# Parse a Memory MAP resource data
# 
# =============================================================================
def parse_mmap_resource(fdata: bytes, offset: int, byte_order: str
                        ) -> MMapResource:
    """
    Parse a MMAP resource data and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the MMAP file to parse.
    offset: int
        The offset to this MMapResource
    byte_order: str
        Python's struct module byte order.
        
    Returns
    -------
    MMapResource
        an object that contains the data.
        
        
    """
    logging.debug("--------------------------")
    chunkID: str = parse_chunk_id(fdata, offset, byte_order)
    logging.debug("chunkID: %s", chunkID)

    size: int = struct.unpack(byte_order+"i", fdata[(offset+4):(offset+8)])[0]
    logging.debug("size: %s", size)

    off: int = struct.unpack(byte_order+"i", fdata[(offset+8):(offset+12)])[0]
    logging.debug("offset: %s", off)   
    
    flag: int = struct.unpack(byte_order+"h", fdata[(offset+12):(offset+14)])[0]
    logging.debug("flags: %s", flag)  

    unus: int = struct.unpack(byte_order+"h", fdata[(offset+14):(offset+16)])[0]
    logging.debug("unused: %s", unus)  
    
    nrID: int = struct.unpack(byte_order+"i", fdata[(offset+16):(offset+20)])[0]
    logging.debug("nextResourceID: %s", nrID)  
    
    return MMapResource(chunkID, size, off, flag, unus, nrID)

#
# Parse a Memory MAP file data
# 
# =============================================================================
def parse_mmap(fdata: bytes, byte_order: str) -> MemoryMAP:
    """
    Parse a MMAP file data and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the IMAP file to parse.
    byte_order: str
        Python's struct module byte order.
        
    Returns
    -------
    MemoryMAP
        an object that contains the data.
        
        
    """
    logging.debug("==================================")
    logging.debug(" Parse memory map: %d bytes", len(fdata))
    content = struct.unpack(byte_order+"hhiiiii", fdata[0:24])
    logging.debug("MMAP[0] Property size: %s", content[0])
    logging.debug("MMAP[1] Resource size: %s", content[1])
    logging.debug("MMAP[2] Max resources count: %d", content[2])
    logging.debug("MMAP[3] Used resources count: %d", content[3])
    logging.debug("MMAP[4] First junk resource ID: %d", content[4])
    logging.debug("MMAP[5] old memory map resource ID: %d", content[5])
    logging.debug("MMAP[6] First free resource ID: %d", content[6])

    mmap = MemoryMAP(content[0], content[1], content[2], content[3],
                     content[4], content[5], content[6])
    
    offset = 24
    for _ in range(0, mmap.usedResourceCount):
        resource = parse_mmap_resource(fdata, offset, byte_order)
        mmap.resources.append(resource)
        offset += 20
    
    return mmap

