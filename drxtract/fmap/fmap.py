# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
import struct
import logging
from ..lingosrc.util import vsprintf, Dictionary

#
# FontInfo class.
# 
class FontInfo(Dictionary):
    """This class represents a font in the fontmap"""
    
    def __init__(self, name: str, font_id: int):
        super().__init__()
        self['name'] = name
        self['id'] = font_id

#
# Reads from Fmap file the fonts information
# =============================================================================
def parse_fmap_data(fdata: bytes) -> List[FontInfo]:
    """
    Parse a Fmap file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the Fmap file that contain the font map.
        
    Returns
    -------
    List[FontInfo]
        a dictionary that contains the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    fmap_data = []
    idx = 0

    header_size = struct.unpack('>i', fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("header_size = %04x", header_size)
        
    additional_size = struct.unpack('>i', fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("additional_size = %08x", additional_size)
    
    if 8 + header_size + additional_size != len(fdata):
        msg = vsprintf("Bad data size! (%d != %d)",
                       (8 + header_size + additional_size), len(fdata))
        raise ValueError(msg)
    
    header_data = fdata[idx:idx + header_size]
    idx += header_size
    
    basic_data = fdata[idx:idx + additional_size]
    idx += additional_size
        
    # Parse header data
    idx = 0
    unknown01 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown01 = %s", unknown01)         
    
    unknown02 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown02 = %s", unknown02)         
    
    unknown03 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown03 = %s", unknown03)         
    
    unknown04 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown04 = %s", unknown04)                
    
    nfonts =  struct.unpack('>i', header_data[idx:idx+4])[0]
    idx += 4
    logging.debug("Number of fonts = %s", nfonts)        
    
    nfonts_cap =  struct.unpack('>i', header_data[idx:idx+4])[0]
    idx += 4
    logging.debug("Number of fonts (including non used ones) = %s", nfonts_cap)         
    
    unknown5 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown5 = %s", unknown5)
    
    font_meta_size =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("Font metadata size = %s", font_meta_size)          
    
    unknown6 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown6 = %s", unknown6)  
    
    unknown7 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown7 = %s", unknown7)  
    
    unknown8 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown8 = %s", unknown8)  
    
    unknown9 =  struct.unpack('>h', header_data[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown9 = %s", unknown9)  
    
    metadata = []
    for i in range(nfonts_cap):
        logging.debug("--------------------------")             
        displacement =  struct.unpack('>i', header_data[idx:idx+4])[0]
        idx += 4
        logging.debug("displacement = %s", displacement)             
    
        unknown00 =  struct.unpack('>h', header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown00 = %s", unknown00)     
    
        font_id =  struct.unpack('>h', header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("font_id = %s", font_id)
        
        data = {}
        data['displacement'] = displacement
        data['font_id'] = font_id
        
        metadata.append(data)
        
        
    logging.debug("--------------------------")
    
    # Parse font data
    for i in range(nfonts):
        logging.debug("--------------------------")        
        idx = metadata[i]['displacement']
        nchars =  struct.unpack('>i', basic_data[idx:idx+4])[0]
        idx += 4
        logging.debug("nchars = %s", nchars)   
        
        font_name = basic_data[idx:idx+nchars].decode('ISO-8859-1')
        idx = idx+nchars       
        logging.debug("font_name = %s", font_name)
        
        fmap_data.append(FontInfo(font_name, metadata[i]['font_id']))
        
    logging.debug("--------------------------")        
    
    return fmap_data

