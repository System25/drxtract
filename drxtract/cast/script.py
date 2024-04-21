# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .castparser import CastParser, DIR_LSCR_TYPE
import logging
from typing import Dict, Any


#
# Script header data parser class.
#
class ScriptParser(CastParser):  
    def __init__(self):
        super().__init__(DIR_LSCR_TYPE)

    def parse(self, _: bytes, __: Dict[str, Any]) -> Dict[str, Any]:
        castData: Dict[str, Any] = {}
        
        # Director Lingo Script reference
        logging.info("Is a script reference")
        castData['type'] = 'script'
        
        return castData
