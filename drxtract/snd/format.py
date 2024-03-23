# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Classes to parse SND files.
# https://developer.apple.com/library/archive/documentation/mac/Sound/Sound-60.html
#

import struct
import logging
from typing import List
from enum import Enum
from ..lingosrc.util import vsprintf

# Mac bit order
mac_bit_order = '>'

#
# Sound initialization parameters enumeration.
# https://www.burgerbecky.com/burgerlib/docs/Sound_Manager.pdf
# 
class SoundInitParam(Enum):
    INIT_CHAN_LEFT = 0x0002     # left stereo channel
    INIT_CHAN_RIGHT = 0x0003    # right stereo channel
    WAVE_INIT_CHAN_0 = 0x0004   # wave-table channel 0
    WAVE_INIT_CHAN_1 = 0x0005   # wave-table channel 1
    WAVE_INIT_CHAN_2 = 0x0006   # wave-table channel 2
    WAVE_INIT_CHAN_3 = 0x0007   # wave-table channel 3
    INIT_MONO = 0x0080          # monophonic channel
    INIT_STEREO = 0x00C0        # stereo channel
    INIT_MACE3 = 0x0300         # 3:1 compression
    INIT_MACE6 = 0x0400         # 6:1 compression
    INIT_NO_INTERP = 0x0004     # no linear interpolation
    INIT_NO_DROP = 0x0008       # no drop-sample conversion

#
# Synth type.
# 
class SynthType(Enum):
    SQUARE = 0x0001         # square-wave data
    WAVE_TABLE = 0x0003     # wave-table data
    SAMPLED = 0x0005        # sampled-sound data

#
# Sound data type class.
#
class DataType:
    """This class represents a data type"""
    
    def __init__(self):
        self.synth: int = -1
        """Synth type"""
        
        self.initParam: int = -1
        """Sound init param"""

#
# Sound command class.
#
class SoundCommand:
    """This class represents a SoundCommand"""
    
    def __init__(self, command: int, param1: int, param2: int):
        self.command: int = command
        """Sound command number"""
        
        self.param1: int = param1
        """First parameter"""
        
        self.param2: int = param2
        """Second parameter"""

#
# Abstract SND format class.
#
class SndFormat:
    """This class represents the common content of the SND format"""
    
    def __init__(self, fmt):
        self.format: int = fmt
        """Format number"""
        
        self.commands: List[SoundCommand] = []
        """List of sound commands"""

    def get_num_channels(self):
        return 1

#
# SND format 1.
# 
class SndFormat1(SndFormat):
    """This class represents the common content of the SND format 1"""
    
    def __init__(self):
        super().__init__(1)
        self.formats: List[DataType] = []
        """List of formats"""

    def get_num_channels(self):
        if len(self.formats) > 0:
            fmt = self.formats[0]
            if (fmt.initParam & SoundInitParam.INIT_STEREO) != 0:
                return 2

        return 1

#
# SND format 2.
# 
class SndFormat2(SndFormat):
    """This class represents the common content of the SND format 2"""
    
    def __init__(self):
        super().__init__(2)
        self.refCount: int = -1
        """Reference count"""



#
# Parse SND format 1
# 
# =============================================================================
def parse_snd_commands(fdata: bytes, idx: int, sndData: SndFormat):
    """
    Parse the commands section of a SND file data.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the SND file.
    idx: int
        The index where the commands section starts.
    sndData: SndFormat
        The SndFormat object where the commands will be added.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    nsound_cmds =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("nsound_cmds = %s", nsound_cmds)

    # Parse the sound commands
    for _ in range(0, nsound_cmds):
        command =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        
        if command < 0:
            command = (0xFFFF + command) + 1
        logging.debug("command = %s", command)
        
        param1 =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        logging.debug("param1 = %s", param1)                             
    
        param2 = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("param2 = %s", param2)
        
        sndData.commands.append(SoundCommand(command, param1, param2))


#
# Parse SND format 1
# 
# =============================================================================
def parse_snd_fmt1(fdata: bytes) -> SndFormat1:
    """
    Parse a SND file data (format 1) and return its header.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the SND file.
        
    Returns
    -------
    SndFormat
        an object that contains the SND header data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    sndData = SndFormat1()
    idx = 2
    
    ndata_types =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("ndata_types = %s", ndata_types)
    
    for _ in range(0, ndata_types):
        data_type =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        logging.debug("data_type = %s", data_type)
        
        init_options = int(struct.unpack(mac_bit_order+"i",
                                         fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("init_options = %s", init_options)
        
        dt: DataType = DataType()
        dt.synth = data_type
        dt.initParam = init_options
        
        sndData.formats.append(dt)
        
    parse_snd_commands(fdata, idx, sndData)
    
    return sndData

#
# Parse SND format 2
# 
# =============================================================================
def parse_snd_fmt2(fdata: bytes) -> SndFormat2:
    """
    Parse a SND file data (format 2) and return its header.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the SND file.
        
    Returns
    -------
    SndFormat
        an object that contains the SND header data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    sndData = SndFormat2()
    idx = 2
    
    refcount =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("refcount = %s", refcount)
    sndData.refCount = refcount
    
    parse_snd_commands(fdata, idx, sndData)
    
    return sndData


#
# Parse SND format
# 
# =============================================================================
def parse_snd_fmt(fdata: bytes) -> SndFormat:
    """
    Parse a SND file data and return its header.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the SND file.
        
    Returns
    -------
    SndFormat
        an object that contains the SND header data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    idx = 0
    format_type =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("format_type = %s", format_type)
    
    if format_type == 1:
        # Format 1 Sound Resource
        return parse_snd_fmt1(fdata)
                    
    elif format_type == 2:
        # Format 2 Sound Resource
        return parse_snd_fmt2(fdata)
        
    else:
        msg = vsprintf("Unrecognized SND format: %d", format_type)
        raise ValueError(msg)

