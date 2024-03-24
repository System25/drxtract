# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
import struct
import logging
from ..lingosrc.util import vsprintf, Dictionary
from ..fmap import FontInfo

#
# TextFormat class.
# 
class TextFormat(Dictionary):
    """This class represents a text format"""
    
    def __init__(self, color: str, start: int, bold: bool, italic: bool,
                 underline: bool, font_size: int, font_family: str):
        super().__init__()
        self['color'] = color
        self['start'] = start
        self['bold'] = bold
        self['italic'] = italic
        self['underline'] = underline
        self['font_size'] = font_size
        self['font_family'] = font_family
        

#
# TextData class.
# 
class TextData(Dictionary):
    """This class represents the text data in a STXT file"""
    
    def __init__(self, text: str, txt_format: List[TextFormat]):
        super().__init__()
        self['text'] = text
        self['txt_format'] = txt_format

#
# Reads text from a STXT file
# =============================================================================
def parse_stxt_data(fdata: bytes, fontmap: List[FontInfo]) -> TextData:
    """
    Parse a STXT file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the STXT file that contain a rich text.
    fontmap: List[FontInfo]
        The font map.
        
    Returns
    -------
    TextData
        an object that contains the text data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    idx = 0

    # Read STXT file header
    idxb = struct.unpack('>i', fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("base index = %08x", idxb)

    nchars =  struct.unpack('>i', fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("number of characters: %d", nchars)

    font_data_size =  struct.unpack('>i', fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("font_data_size = %08x", font_data_size)
    
    
    txt_data = fdata[idxb:idxb+nchars].decode('ISO-8859-1')
    idx = idxb+nchars
    

    txt_format = []
    nformat_info =  struct.unpack('>h', fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("nformat_info = %s", nformat_info)
    for _ in range(nformat_info):
        unknown2 =  struct.unpack('>h', fdata[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown2 = %s", unknown2)           
        
        start =  struct.unpack('>h', fdata[idx:idx+2])[0]
        idx += 2
        logging.debug("start = %s", start)             
        
        unknown4 =  struct.unpack('>h', fdata[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown4 = %s", unknown4)             
        
        unknown5 =  struct.unpack('>h', fdata[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown5 = %s", unknown5)            
        
        font_family_id =  struct.unpack('>h', fdata[idx:idx+2])[0]
        idx += 2
        
        font_family = vsprintf('unknown_%d', font_family_id)
        for font in fontmap:
            if font['id'] == font_family_id:
                font_family = font['name']

        logging.debug("font_family = %s", font_family)                    
                
        font_format =  int(fdata[idx])
        idx += 1
        logging.debug("font_format = %s", font_format)
        
        bold = False
        italic = False
        underline = False
        if (font_format & 1) != 0:
            bold = True

        if (font_format & 2) != 0:
            italic = True        
            
        if (font_format & 4) != 0:
            underline = True               
            
        unknown7 =  int(fdata[idx])
        idx += 1    
        logging.debug("unknown7 = %s", unknown7)
        
        font_size =  struct.unpack('>h', fdata[idx:idx+2])[0]
        idx += 2
        logging.debug("font_size = %s", font_size)
        
        fg_color_red =  int(fdata[idx])
        idx += 1    
        logging.debug("fg_color_red = %s", fg_color_red)            
        
        unknown9 =  int(fdata[idx])
        idx += 1    
        logging.debug("unknown9 = %s", unknown9)
        
        fg_color_green =  int(fdata[idx])
        idx += 1    
        logging.debug("fg_color_green = %s", fg_color_green)            
        
        unknown10 =  int(fdata[idx])
        idx += 1    
        logging.debug("unknown10 = %s", unknown10)
        
        fg_color_blue =  int(fdata[idx])
        idx += 1    
        logging.debug("fg_color_blue = %s", fg_color_blue)            
        
        unknown11 =  int(fdata[idx])
        idx += 1    
        logging.debug("unknown11 = %s", unknown11)              
        
        color = vsprintf('#%02X%02X%02X', fg_color_red, fg_color_green,
                         fg_color_blue)
        tformat = TextFormat(color, start, bold, italic, underline,
                             font_size, font_family)
        
        txt_format.append(tformat)

    
    return TextData(txt_data, txt_format)

