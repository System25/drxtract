# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).


from .cmd import SoundCmd
from ..sampled import SampledSound
import logging

#
# Null command class.
# Do nothing!
# https://www.burgerbecky.com/burgerlib/docs/Sound_Manager.pdf
# 
class NullCmd(SoundCmd):
    def __init__(self):
        super().__init__(0)
        
    def get_frames(self, sound: SampledSound, param1: int,
                   param2: int, fdata: bytes) -> bytes:
        logging.debug("nullCmd(%d, %d)", param1, param2)
        return bytes()
