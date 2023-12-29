# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_SHAPE_TYPE
import logging
import struct
from typing import Dict, Any

from ..common import get_shape_name


#
# Shape header data parser class.
#
class ShapeParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_SHAPE_TYPE)

    def parse(self, header_data: bytes, _: Dict[str, Any]) -> Dict[str, Any]:
        idx = 0
        castData: Dict[str, Any] = {}
        
        logging.info("Is a shape")
        castData['type'] = 'shape'
        
        unknown00 =  int(header_data[idx])
        idx += 1                
        logging.debug("unknown00 = %s", unknown00) 

        shape_type =  get_shape_name(
            struct.unpack(">h", header_data[idx:idx+2])[0])
        idx += 2
        logging.debug("shape_type = %s", shape_type)
        
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
        
        unknown02 =  int(header_data[idx])
        idx += 1                
        logging.debug("unknown02 = %s", unknown02)             
        
        pattern =  int(header_data[idx])
        idx += 1                
        logging.debug("pattern = %s", pattern)        
        
        fgColor =  int(header_data[idx])
        idx += 1                
        logging.debug("fgColor = %s", fgColor)                
        
        bgColor =  int(header_data[idx])
        idx += 1                
        logging.debug("bgColor = %s", bgColor)              
        
        filled =  int(header_data[idx])
        idx += 1                
        logging.debug("filled = %s", filled)
        
        line_width =  int(header_data[idx]) - 1
        idx += 1                
        logging.debug("line_width = %s", line_width)                 
        
        unknown08 =  int(header_data[idx])
        idx += 1                
        logging.debug("unknown08 = %s", unknown08)   
        
        castData['shapeType'] = shape_type            
        castData['top'] = top            
        castData['left'] = left            
        castData['bottom'] = bottom            
        castData['right'] = right
        castData['pattern'] = pattern     
        castData['foreColor'] = fgColor     
        castData['backColor'] = bgColor     
        castData['filled'] = filled
        castData['lineSize'] = line_width
        
        return castData
                    