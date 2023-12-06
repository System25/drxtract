# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from ..sampled import SampledSound


#
# Base sound command class.
# 
class SoundCmd:
    """This class represents a sound command"""
    
    def __init__(self, command):
        self.command: int = command
        """Command identifier"""
        
    def get_frames(self, sound: SampledSound, param1: int,
                   param2: int, fdata: bytes) -> bytes:
        raise NotImplementedError()

