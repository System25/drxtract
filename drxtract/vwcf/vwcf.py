# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import Dict, Any
import struct
import logging

from ..common import get_palette_name

#
# Reads from VWCF data the basic information
# =============================================================================
def parse_vwcf_file_data(fdata: bytes) -> Dict[str, Any]:
    """
    Parse a VWCF file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the VWCF file that contain the basic information of
        a Director file.
        
    Returns
    -------
    Dict[str, Any]
        a dictionary that contains the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    indx = 0
    dataSize = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Data size: %d", dataSize)
    
    if (len(fdata) != dataSize):
        logging.error("Bad data size!")
        raise ValueError("Bad data size!")
        
    version = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Director version: 0x%04x", version)
    
    stageTop = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Stage top: %d", stageTop)
    
    stageLeft = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Stage left: %d", stageLeft)
    
    
    stageBottom = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Stage bottom: %d", stageBottom)
    
    
    stageRight = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Stage right: %d", stageRight)
    
    castArrayStart = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Cast array start: %d", castArrayStart)
    
    castArrayEnd = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Cast array end: %d", castArrayEnd)
    
    currentFrameRate = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("Current frame rate?: %d", currentFrameRate)
    
    indx += 9
    stageColor = int(fdata[indx])
    indx += 1
    
    logging.debug("Stage color: %d", stageColor)

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
        
    logging.info("Director version: %s", version)
    
    # The default palette position depends on the director version
    if version == 'dir4': 
        indx = 0x46
        palette = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        palette = get_palette_name(palette)
    elif version == 'dir5':
        indx = 0x4E
        palette = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        palette = get_palette_name(palette)
    else:
        palette = 'unknonw'
        
        
    logging.debug("palette (%d): %s", indx, palette)
    
    config: Dict[str, Any] = {}
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
