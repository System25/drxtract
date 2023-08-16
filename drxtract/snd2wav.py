#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to convert a Machintosh "snd " file to Microsoft WAV (and then to MP3).
# More info: https://developer.apple.com/library/archive/documentation/mac/Sound/Sound-60.html#MARKER-9-400
# 

import sys
import os
import struct
import logging
import wave
import json

logging.basicConfig(level=logging.DEBUG)

# Mac bit order
mac_bit_order = '>'


# ==============================================================================
def processCommands(fdata, idx, wavef, num_channels):
    nsound_cmds =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("nsound_cmds = %s"%(nsound_cmds))

    # Process the sound commands
    for cmd in range(0, nsound_cmds):
        command =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        if command < 0:
            command = (0xFFFF + command) + 1
        logging.debug("command = %s"%(command))                        
        
        if command == 0x8051:
            # BufferCmd
            processBufferCmd(fdata, idx, wavef, num_channels)

        else:
            logging.error("Unsupported command = %s"%(command))
            sys.exit(-1)                   

    return

# ====================================================================================================================================
def processBufferCmd(fdata, idx, wavef, num_channels):
    bps = 8 
    sample_rate = 16000
    num_frames = 0
    
    param1 =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("param1 = %s"%(param1))                             

    param2 = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
    idx += 4
    logging.debug("param2 = %s"%(param2))  

    if param2 != idx:
        logging.error("Bad offset to sound header = %s"%(param2))
        sys.exit(-1)                              

    # Read the sampled sound header
    dataptr = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
    idx += 4
    logging.debug("data pointer = %s"%(dataptr))                             

    to_be_defined = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
    idx += 4
    logging.debug("to_be_defined = %s"%(to_be_defined))

    sample_rate =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("sample_rate = %s"%(sample_rate))                            

    sample_rate_ext =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
    idx += 2
    logging.debug("sample_rate_ext = %s"%(sample_rate_ext))    
    
    sample_loop_start = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
    idx += 4
    logging.debug("sample_loop_start = %s"%(sample_loop_start))

    sample_loop_end = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
    idx += 4
    logging.debug("sample_loop_end = %s"%(sample_loop_end))                            

    sample_encoding = int(fdata[idx])
    idx += 1
    logging.debug("sample_encoding = %s"%(sample_encoding))

    base_frecuency = int(fdata[idx])
    idx += 1
    logging.debug("base_frecuency = %s"%(base_frecuency))                            

    if base_frecuency != 0x3C:
        logging.error("Unsupported base fecuency = %s"%(base_frecuency))
        sys.exit(-1)                                 

    if sample_encoding == 0x00:
        # Standard sound header
        bytes_in_sample = to_be_defined
        logging.debug("number of bytes in sample = %s"%(bytes_in_sample))
        
        num_frames = int(bytes_in_sample/num_channels)

    elif sample_encoding == 0xFF:
        # Extended sound header
        num_channels = to_be_defined
        logging.debug("num_channels = %s"%(num_channels))
        
        num_frames = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("num_frames = %s"%(num_frames))      
        
        aiff_sample_rate = fdata[idx:idx+10]
        idx += 10
        logging.debug("aiff_sample_rate = %s"%(aiff_sample_rate))         
        
        marker_chunk = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("marker_chunk = %s"%(marker_chunk))     
        
        instruments_chunk = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("instruments_chunk = %s"%(instruments_chunk))
        
        aes_recording = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("aes_recording = %s"%(aes_recording))        
             
        bps =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        logging.debug("bps = %s"%(bps))                     
                      
        future_use1 =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        logging.debug("future_use1 = %s"%(future_use1))                       
                      
        future_use2 = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("future_use2 = %s"%(future_use2))                      
                   
        future_use3 = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("future_use3 = %s"%(future_use3))
                      
        future_use4 = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
        idx += 4
        logging.debug("future_use4 = %s"%(future_use4))

    elif sample_encoding == 0xFE:
        # Compressed sound header                            
        logging.error("Compressed sound header not supported yet!")
        sys.exit(-1)                             
    
    logging.debug("------- WAV generation ---------") 
    logging.debug("num_channels = %s"%(num_channels)) 
    logging.debug("sample_rate = %s"%(sample_rate)) 
    logging.debug("bps = %s"%(bps))
    logging.debug("num_frames = %s"%(num_frames))
    
    # Get cast file data
    castData = {}
    with open(os.path.join(sys.argv[1], 'data.json'), mode='r', encoding='utf-8') as jsfile:
        text = jsfile.read()
        castData = json.loads(text)
        
    # Add sound file information
    castData['sampleSize'] = bps
    castData['sampleRate'] = sample_rate
    castData['channelCount'] = num_channels
      
    # Write CAST data to JSON file
    with open(os.path.join(sys.argv[1], 'data.json'), 'wb') as jsfile:
        jsfile.write(json.dumps(castData, indent=4, sort_keys=True).encode('utf-8'))        
    
    nsamples = int(num_frames*num_channels)

    # Write wave file
    wavef.setnchannels(num_channels)
    wavef.setsampwidth(int(bps/8)) 
    wavef.setframerate(sample_rate)

    if bps == 8:
        # 8 bit per sample
        wavef.writeframesraw( fdata[idx:idx+nsamples] )

    elif bps == 16:
        # 16 bit per sample
        # Convert from big endian word to little endian word
        for f in range(0, nsamples):
            sample =  int(struct.unpack(">H", fdata[idx:idx+2])[0])
            idx += 2
            data = struct.pack('<H', sample)
            wavef.writeframesraw( data )

    else:
        logging.error("Bad number of bits per sample! (%s)"%(bps))
        sys.exit(-1)

    wavef.writeframes(b'')
    wavef.close()    
    
    
    return

# ====================================================================================================================================
def snd2wav(snd_file):
    clutData = None
    
    with open(snd_file, mode='rb') as file:
        fdata = file.read()
        
        file_ext = 'wav'
        file_name = "%s.%s"%(os.path.basename(snd_file)[:-5], file_ext)

        wavef = wave.open(os.path.join(sys.argv[1], file_name),'w')
        idx = 0

        # Read SND file header
        
        format_type =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
        idx += 2
        logging.debug("format_type = %s"%(format_type)) 

        num_channels =  1

        
        if format_type == 1:
            # Format 1 Sound Resource
            ndata_types =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
            idx += 2
            logging.debug("ndata_types = %s"%(ndata_types))
            
            # Process the data types
            for ndatatype in range(0, ndata_types):
                data_type =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
                idx += 2
                logging.debug("data_type = %s"%(data_type)) 
                
                if data_type == 5:
                    # Sampled sound data
                    
                    init_options = int(struct.unpack(mac_bit_order+"i", fdata[idx:idx+4])[0])
                    idx += 4
                    logging.debug("init_options = %s"%(init_options))
                    
                    if (init_options & 0x80):
                        # Mono
                        num_channels =  1
                    else:
                        # Stereo
                        num_channels =  2
                        
                    processCommands(fdata, idx, wavef, num_channels)
                    
                else:
                    logging.error("Unsupported data type = %s"%(format_type))
                    sys.exit(-1)
                    
        elif format_type == 2:
            # Format 2 Sound Resource
            
            refcount =  int(struct.unpack(mac_bit_order+"h", fdata[idx:idx+2])[0])
            idx += 2
            logging.debug("refcount = %s"%(refcount))
            
            processCommands(fdata, idx, wavef, num_channels)
            
        else:
            logging.error("Bad format type = %s"%(format_type))

    return


# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: snd2wav <work directory> <snd_ file name>")

    else:

        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory"%(sys.argv[1]))
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file"%(os.path.join(sys.argv[2], sys.argv[3])))
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.snd_'):
            logging.error(" '%s' does not end in '.snd_'"%(sys.argv[2]))
            sys.exit(-1)
            
        # Generate the WAV file
        snd_file = os.path.join(sys.argv[1], sys.argv[2])
        snd2wav(snd_file)
        
        in_name = os.path.join(sys.argv[1], "%s.%s"%(sys.argv[2][:-5], 'wav'))
        out_name = os.path.join(sys.argv[1], "%s.%s"%(sys.argv[2][:-5], 'mp3'))
        
        # Transform it to mp3
        os.system('ffmpeg -y -i %s -acodec libmp3lame %s'%(
            in_name, # input file
            out_name #output file
        ))        
