# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_TRAN_TYPE
import logging
import struct
from typing import Dict, Any

from ..common import get_transition_name


#
# Transition header data parser class.
#
class TransitionParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_TRAN_TYPE)

    def parse(self, header_data: bytes, _: Dict[str, Any]) -> Dict[str, Any]:
        idx = 0
        castData: Dict[str, Any] = {}
        
        # Director transition type
        logging.info("Is a transition")
        castData['type'] = 'transition'
            
        smoothness =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("smoothness = %s", smoothness)
        
        transition =  header_data[idx]
        idx += 1                
        logging.debug("transition = %s", transition) 
        
        stage_or_area =  header_data[idx]
        idx += 1                
        logging.debug("stage_or_area = %s", stage_or_area)
        
        # Duration in millisenconds
        duration =  struct.unpack(">h", header_data[idx:idx+2])[0]
        idx += 2
        logging.debug("duration = %s", duration)
        
        castData['transition'] = {}
        castData['transition']['type'] = get_transition_name(transition)
        castData['transition']['smoothness'] = smoothness
        castData['transition']['duration'] = duration
        castData['transition']['in_changing_area'] = (stage_or_area == 2)
        return castData
