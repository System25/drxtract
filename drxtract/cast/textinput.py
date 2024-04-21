# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_TEXT_INPUT_TYPE
import logging
import struct
from typing import Dict, Any
from ..lingosrc.util import vsprintf


#
# Text input header data parser class.
#
class TextInputParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_TEXT_INPUT_TYPE)

    def parse(self, header_data: bytes, _: Dict[str, Any]) -> Dict[str, Any]:
        idx = 0
        castData: Dict[str, Any] = {}
        
        logging.info("Is a text input field")
        castData['type'] = 'field'            

        unknown0 =  int(header_data[idx])
        idx += 1            
        logging.debug("unknown0 = %s", unknown0)  

        border =  int(header_data[idx])
        idx += 1            
        logging.debug("border = %s", border)  
        
        margin =  int(int(header_data[idx])/2)
        idx += 1            
        logging.debug("margin = %s", margin)               

        boxDropShadow =  int(int(header_data[idx])/2)
        idx += 1            
        logging.debug("boxDropShadow = %s", boxDropShadow)               

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
        
        logging.debug("boxType = %s", boxTypeName)         
        
        alignment =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        
        if alignment == 0:
            alignment = 'left'
        elif alignment == 1:
            alignment = 'center'
        elif alignment == -1:
            alignment = 'right'
        else:
            logging.warning("Unknown text alignment = %s", alignment)  
        
        logging.debug("alignment = %s", alignment)
        
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
        
        scrollTop =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("scrollTop = %s", scrollTop)
        
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
        
        pageHeight =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("pageHeight = %s", pageHeight)

        dropShadow =  int(header_data[idx])
        idx += 1            
        logging.debug("dropShadow = %s", dropShadow)

        options =  int(header_data[idx])
        idx += 1            
        logging.debug("options = %s", options)
        
        wordWrap = True
        editable = False
        autoTab = False
        if options & 0x4:
            wordWrap = False
        if options & 0x1:
            editable = True                
        if options & 0x2:
            autoTab = True            

        scrollHeight =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("scrollHeight = %s", scrollHeight)

        
        castData['wordWrap'] = wordWrap    
        castData['boxType'] = boxTypeName  
        castData['editable'] = editable    
        castData['autoTab'] = autoTab
        castData['alignment'] = alignment 
        castData['border'] = border 
        castData['margin'] = margin 
        castData['boxDropShadow'] = boxDropShadow 
        castData['dropShadow'] = dropShadow 
        castData['backgroundColor'] = vsprintf('#%02X%02X%02X',
            bgcolor_red, bgcolor_green, bgcolor_blue)
        castData['height'] = bottom - top 
        castData['width'] = right - left
        castData['pageHeight'] = pageHeight
        castData['scrollHeight'] = scrollHeight
        castData['scrollTop'] = scrollTop
        
        return castData
                    