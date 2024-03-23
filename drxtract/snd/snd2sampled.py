# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Classes to generate a sampled sound from SND files.
#

import io
from ..lingosrc.util import vsprintf, get_keys
from .format import parse_snd_fmt, SndFormat
from .command import SOUND_COMMANDS, SoundCmd
from .sampled import SampledSound
import logging

#
# Generates a sampled sound object from SND file data.
# 
# =============================================================================
def snd_to_sampled(fdata : bytes) ->  SampledSound:
    """
    Process a SND file data and return a WAV file data.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the SND file.
        
    Returns
    -------
    SampledSound
        Sample sound object.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    sndData: SndFormat = parse_snd_fmt(fdata)
    bytesIo: io.BytesIO = io.BytesIO()
    sound: SampledSound = SampledSound()
    
    
    # Process the sound commands
    for cmd in sndData.commands:
        command = cmd.command
        logging.debug("Processing command: %d", command)
        if command in get_keys(SOUND_COMMANDS):
            soundCmd:SoundCmd = SOUND_COMMANDS[command]
            bytesIo.write(soundCmd.get_frames(sound, cmd.param1, cmd.param2,
                                              fdata))
            
        else:
            msg = vsprintf('Unsupported sound command: %d', cmd.command)
            raise ValueError(msg)

    sound.samples = bytesIo.getvalue()
    bytesIo.close()
    
    return sound
