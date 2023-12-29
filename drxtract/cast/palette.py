# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_CLUT_TYPE
import logging
from typing import Dict, Any


#
# Palette header data parser class.
#
class PaletteParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_CLUT_TYPE)

    def parse(self, _: bytes, __: Dict[str, Any]) -> Dict[str, Any]:
        castData: Dict[str, Any] = {}
        
        # Palette reference
        logging.info("Is a palette")
        castData['type'] = 'palette'
        
        return castData
