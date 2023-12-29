# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_SND_TYPE
import logging
from typing import Dict, Any


#
# Sound header data parser class.
#
class SoundParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_SND_TYPE)

    def parse(self, _: bytes,
              basic_data: Dict[str, Any]) -> Dict[str, Any]:
        castData: Dict[str, Any] = {}
        
        # Director sound type
        logging.info("Is a sound")
        castData['type'] = 'sound'
        castData['loop'] = (basic_data['basic']['basic_data2'] != 0x10)
        
        return castData
