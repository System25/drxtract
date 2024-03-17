# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_IMAGE_TYPE
import logging
import struct
from typing import Dict, Any

from ..common import get_palette_name


#
# Image header data parser class.
#
class ImageParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_IMAGE_TYPE)

    def parse(self, header_data: bytes, _: Dict[str, Any]) -> Dict[str, Any]:
        idx = 0
        castData: Dict[str, Any] = {}
        
        # Director bitmap type
        logging.info("Is a bitmap")
        castData['type'] = 'bitmap'
        
        flags =  int(header_data[idx])
        idx += 1
        logging.debug("flags = %s", flags)

        bmp_bpp_val =  int(header_data[idx])
        idx += 1
        
        bmp_bpp = 8
        if bmp_bpp_val == 0x80:
            # 8 bit per pixel image
            bmp_bpp = 8
            
        elif bmp_bpp_val == 0x81:
            # 4 bit per pixel image
            bmp_bpp = 4

        elif bmp_bpp_val == 0x82:
            # 8 bit per pixel image
            bmp_bpp = 8

        elif bmp_bpp_val == 0x84:
            # 16 bit per pixel image
            bmp_bpp = 16

        elif bmp_bpp_val == 0x85:
            # 16 bit per pixel image (MAC format)
            bmp_bpp = 16

        elif bmp_bpp_val == 0x8A:
            # 24 bit per pixel image
            bmp_bpp = 24

        elif bmp_bpp_val == 0x0:
            # 2 bit per pixel image (Black and White)
            bmp_bpp = 2               
            
        else:
            logging.warning("Unknown BPP value: %s", bmp_bpp_val)

        logging.debug("bmp_bpp = %s", bmp_bpp)


        unknown_11 =  int(header_data[idx])
        idx += 1                
        logging.debug("unknown_11 = %s", unknown_11)

        h_padding =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("h_padding = %s", h_padding) 

        w_padding =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("w_padding = %s", w_padding) 

        bmp_height =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2                
        logging.debug("bmp_height = %s", bmp_height) 

        bmp_width =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2                
        logging.debug("bmp_width = %s", bmp_width) 

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
        
        locV =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("locV = %s", locV) 
        
        locH =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("locH = %s", locH)

        palette = 'systemMac'
        if (len(header_data) > 24):
            bitdepth =  struct.unpack(">h", header_data[idx:idx+2])[0]
            idx += 2
            logging.debug("bitdepth = %s", bitdepth)
            if bitdepth > bmp_bpp:
                bmp_bpp = bitdepth

            palette_id = struct.unpack(">h", header_data[idx:idx+2])[0]
            palette = str(palette_id)
            palette_txt =  get_palette_name(palette_id)
            idx += 2
            logging.debug("palette_txt = %s", palette_txt)
            

        castData['height'] = bmp_height
        castData['width'] = bmp_width
        castData['top'] = top
        castData['left'] = left
        castData['bottom'] = bottom
        castData['right'] = right            
        castData['h_padding'] = h_padding
        castData['w_padding'] = w_padding
        castData['locH'] = locH
        castData['locV'] = locV
        castData['depth'] = bmp_bpp
        if bmp_bpp == 8:
            castData['palette'] = palette
            castData['palette_txt'] = palette_txt
        
        return castData
                    