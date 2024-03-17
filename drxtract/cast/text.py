# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_TEXT_TYPE
import logging
import struct
from typing import Dict, Any


#
# Text header data parser class.
#
class TextParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_TEXT_TYPE)

    def parse(self, header_data: bytes, _: Dict[str, Any]) -> Dict[str, Any]:
        idx = 0
        castData: Dict[str, Any] = {}
        
        logging.info("Is a text label")
        castData['type'] = 'richText'
        
        h_padding =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("h_padding = %s", h_padding) 

        w_padding =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("w_padding = %s", w_padding) 

        txt_height =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2                
        logging.debug("txt_height = %s", txt_height) 

        txt_width =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2                
        logging.debug("txt_width = %s", txt_width) 

        top =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("top = %s", top) 

        left =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("left = %s", left) 

        bottom =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("bottom = %s", bottom) 

        right =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("right = %s", right) 
        
        antialias =  int(header_data[idx])
        idx += 1            
        if antialias==0:
            antialias = False
        else:
            antialias = True                
        logging.debug("antiAlias = %s", antialias)
        
        boxType =  int(header_data[idx])
        idx += 1            
        logging.debug("boxType = %s", boxType)               
        
        boxTypeName = str(boxType)
        if boxType == 0:
            boxTypeName = 'adjust'
        if boxType == 1:
            boxTypeName = 'scroll'
        if boxType == 2:
            boxTypeName = 'fixed'
        if boxType == 3:
            boxTypeName = 'limit'
        
        unknown2 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown2 = %s", unknown2)

        anti_threshold =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        if anti_threshold < 0:
            anti_threshold = 0
        logging.debug("anti_threshold = %s", anti_threshold)
        
        
        castData['boxType'] = boxTypeName
        castData['antiAlias'] = antialias
        castData['antiAliasThreshold'] = anti_threshold
        castData['width'] = txt_width
        castData['height'] = txt_height
        castData['top'] = top
        castData['left'] = left
        castData['bottom'] = bottom
        castData['right'] = right            
        castData['h_padding'] = h_padding
        castData['w_padding'] = w_padding
        
        return castData
                    