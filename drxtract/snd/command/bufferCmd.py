# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).


from .cmd import SoundCmd
from ..sampled import SampledSound
import logging
import struct

STANDARD = 0x00
EXTENDED = 0xFF
COMPRESSED = 0xFE

# MIDI notes values
MIDDLE_C = 60


        
#
# Buffer command class.
# Play a sampled sound.
# https://www.burgerbecky.com/burgerlib/docs/Sound_Manager.pdf
# 
class BufferCmd(SoundCmd):
    def __init__(self):
        super().__init__(0x8051)
        
    def _get_frames(self, sound: SampledSound, idx: int, fdata: bytes) -> bytes:
        # Read the sampled sound header (pag. 104)
        #
        # PACKED RECORD (standar sound header)
        #   samplePtr: Ptr; {if NIL, samples in sampleArea}
        #   length: LongInt; {number of samples in array}
        #   sampleRate: Fixed; {sample rate}
        #   loopStart: LongInt; {loop point beginning}
        #   loopEnd: LongInt; {loop point ending}
        #   encode: Byte; {sample's encoding option}
        #   baseFrequency: Byte; {base frequency of sample}
        #   sampleArea: PACKED ARRAY[0..0] OF Byte;
        # END;
        # 
        samplePtr = int(struct.unpack('>i', fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("samplePtr = %d", samplePtr)                             
    
        to_be_defined = int(struct.unpack('>i',fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("to_be_defined = %d", to_be_defined)
    
        sampleRateInt =  int(struct.unpack('>h', fdata[idx:idx+2])[0])
        idx += 2
        
        sampleRateDec =  int(struct.unpack('>h', fdata[idx:idx+2])[0])
        idx += 2
        
        logging.debug("sampleRate = %d.%d", sampleRateInt, sampleRateDec)
        
        loopStart = int(struct.unpack('>i', fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("loopStart = %s", loopStart)
    
        loopEnd = int(struct.unpack('>i', fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("loopEnd = %d", loopEnd)                            
    
        encode = int(fdata[idx])
        idx += 1
        logging.debug("encode = %d", encode)
    
        baseFrequency = int(fdata[idx])
        idx += 1
        logging.debug("baseFrequency = %d", baseFrequency)
        
        if samplePtr != 0:
            raise ValueError("samplePtr must be NIL")
        
        if baseFrequency != MIDDLE_C:
            raise ValueError("baseFrequency not supported")
        
        sound.sample_rate = sampleRateInt
        
        num_frames = 0
        length = 0
        if encode == STANDARD:
            # Standard sound header
            length = to_be_defined
            num_frames = int(length/sound.num_channels)
            
        elif encode == EXTENDED:
            # Extended sound header
            # PACKED RECORD
            #   samplePtr: Ptr; {if NIL, samples in sampleArea}
            #   numChannels: LongInt; {number of channels in sample}
            #   sampleRate: Fixed; {rate of original sample}
            #   loopStart: LongInt; {loop point beginning}
            #   loopEnd: LongInt; {loop point ending}
            #   encode: Byte; {sample's encoding option}
            #   baseFrequency: Byte; {base freq. of original sample}
            #   numFrames: LongInt; {total number of frames}
            #   AIFFSampleRate: Extended80; {rate of original sample}
            #   markerChunk: Ptr; {reserved}
            #   instrumentChunks: Ptr; {pointer to instrument info}
            #   AESRecording: Ptr; {pointer to audio info}
            #   sampleSize: Integer; {number of bits per sample}
            #   futureUse1: Integer; {reserved}
            #   futureUse2: LongInt; {reserved}
            #   futureUse3: LongInt; {reserved}
            #   futureUse4: LongInt; {reserved}
            #   sampleArea: PACKED ARRAY[0..0] OF Byte;
            # END;
            sound.num_channels = to_be_defined
            
            num_frames = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("num_frames = %d", num_frames)
            
            length = int(num_frames * sound.num_channels)
            
            aiff_sample_rate = fdata[idx:idx+10]
            idx += 10
            logging.debug("aiff_sample_rate = %d", aiff_sample_rate)         
            
            marker_chunk = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("marker_chunk = %d", marker_chunk)
            
            instruments_chunk = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("instruments_chunk = %d", instruments_chunk)
            
            aes_recording = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("aes_recording = %d", aes_recording)  
                 
            bps =  int(struct.unpack('>h', fdata[idx:idx+2])[0])
            idx += 2
            logging.debug("bps = %d", bps)
            sound.bits_per_sample = bps
                          
            future_use1 =  int(struct.unpack('>h', fdata[idx:idx+2])[0])
            idx += 2
            logging.debug("future_use1 = %d", future_use1)                       
                          
            future_use2 = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("future_use2 = %d", future_use2)                      
                       
            future_use3 = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("future_use3 = %d", future_use3)
                          
            future_use4 = int(struct.unpack('>i', fdata[idx:idx+4])[0])
            idx += 4
            logging.debug("future_use4 = %d", future_use4)

            
        
        else:
            raise ValueError("Compressed sound header not supported yet!")
        
        
        if sound.bits_per_sample == 8:
            # 8 bits per sample
            return fdata[idx:idx+length]
            
        elif sound.bits_per_sample == 16:
            # 16 bit per sample
            # Convert from big endian word to little endian word
            data = bytearray(length * 2)

            for i in range(0, length*2, 2):
                index_l = idx + i
                index_h = idx + i + 1
                l = i
                h = i + 1
                data[l] = fdata[index_h]
                data[h] = fdata[index_l]

            return bytes(data)
            
        else:
            raise ValueError("Unsupported bits per sample!")
        
    def get_frames(self, sound: SampledSound, param1: int,
                   param2: int, fdata: bytes) -> bytes:
        logging.debug("bufferCmd(%d, %d)", param1, param2)
        
        # param2: offset to sound header
        idx = param2
        return self._get_frames(sound, idx, fdata)
        
        
#
# Sampled sound command class.
# install a sampled sound as a voice.
# (this is similar to bufferCmd)
# https://www.burgerbecky.com/burgerlib/docs/Sound_Manager.pdf
# 
class SampledSoundCmd(BufferCmd):
    def __init__(self):
        super().__init__()
        self.command = 0x8050
        
    def get_frames(self, sound: SampledSound, param1: int,
                   param2: int, fdata: bytes) -> bytes:
        logging.debug("soundCmd(%d, %d)", param1, param2)
        
        # param2: offset to sound header
        idx = param2
        return self._get_frames(sound, idx, fdata)
