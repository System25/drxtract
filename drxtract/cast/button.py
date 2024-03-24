# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_PUSH_BUTTON_TYPE
import logging
import struct
from typing import Dict, Any
from ..lingosrc.util import vsprintf


#
# Push button header data parser class.
#
class ButtonParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_PUSH_BUTTON_TYPE)

    def parse(self, header_data: bytes, _: Dict[str, Any]) -> Dict[str, Any]:
        idx = 0
        castData: Dict[str, Any] = {}
        
        logging.info("Is a push button")
        castData['type'] = 'button'
        
        unknown0 =  int(header_data[idx])
        idx += 1            
        logging.debug("unknown0 = %s", unknown0)
        
        unknown1 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown1 = %s", unknown1) 
        
        unknown2 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown2 = %s", unknown2)             
        
        unknown3 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown3 = %s", unknown3)      
        
        bgcolor_red =  int(header_data[idx])
        idx += 1            
        logging.debug("bgcolor_red = %s", bgcolor_red)               
        
        unknown4 =  int(header_data[idx])
        idx += 1   
        logging.debug("unknown4 = %s", unknown4)           
        
        bgcolor_green =  int(header_data[idx])
        idx += 1            
        logging.debug("bgcolor_green = %s", bgcolor_green)               
        
        unknown5 =  int(header_data[idx])
        idx += 1   
        logging.debug("unknown5 = %s", unknown5)      
        
        bgcolor_blue =  int(header_data[idx])
        idx += 1            
        logging.debug("bgcolor_blue = %s", bgcolor_blue)               
        
        unknown6 =  int(header_data[idx])
        idx += 1   
        logging.debug("unknown6 = %s", unknown6)        
        
        unknown7 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown7 = %s", unknown7)             
        
        unknown8 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown8 = %s", unknown8)             
        
        unknown9 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown9 = %s", unknown9)            
        
        unknown10 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown10 = %s", unknown10)             
        
        unknown11 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown11 = %s", unknown11)  
        
        unknown12 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown12 = %s", unknown12)  
        
        unknown13 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown13 = %s", unknown13)  
        
        unknown14 =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("unknown14 = %s", unknown14)  
        
        buttonType =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        if buttonType == 1:
            buttonType = 'pushButton'
        if buttonType == 2:
            buttonType = 'checkBox'
        if buttonType == 3:
            buttonType = 'radioButton'
        
        logging.debug("buttonType = %s", buttonType)              
        
        castData['backgroundColor'] = vsprintf('#%02X%02X%02X',
            bgcolor_red, bgcolor_green, bgcolor_blue)
        castData['buttonType'] = buttonType
        
        return castData
