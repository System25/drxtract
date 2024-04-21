# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, Dict

from .cmd import SoundCmd
from .nullCmd import NullCmd
from .bufferCmd import BufferCmd, SampledSoundCmd

SOUND_CMD_LIST: List[SoundCmd] = [
    NullCmd(),
    BufferCmd(),
    SampledSoundCmd()
]

SOUND_COMMANDS: Dict[int, SoundCmd] = {}
for cmd in SOUND_CMD_LIST:
    idx: int = cmd.command
    SOUND_COMMANDS[idx] = cmd
    
__all__ = ['SOUND_COMMANDS', 'SoundCmd']
