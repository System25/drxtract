#!/usr/bin/python3

# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Script to convert a Machintosh "snd " file to Microsoft WAV (and then to MP3).
# More info: https://developer.apple.com/library/archive/documentation/mac/Sound/Sound-60.html
# 

import sys
import os
import logging
import wave
import json
from .snd import snd_to_sampled, SampledSound

logging.basicConfig(level=logging.DEBUG)


# ==============================================================================
def main():
    if len(sys.argv) < 3:
        print("USAGE: snd2wav <work directory> <snd_ file name>")

    else:

        if not os.path.isdir(sys.argv[1]):
            logging.error(" '%s' is not a directory", sys.argv[1])
            sys.exit(-1)

        if not os.path.isfile(os.path.join(sys.argv[1], sys.argv[2])):
            logging.error(" '%s' is not a file", os.path.join(sys.argv[1],
                                                              sys.argv[2]))
            sys.exit(-1)
        
        if not sys.argv[2].endswith('.snd_'):
            logging.error(" '%s' does not end in '.snd_'", sys.argv[2])
            sys.exit(-1)
            
        # Generate the WAV file
        snd_file = os.path.join(sys.argv[1], sys.argv[2])
        with open(snd_file, mode='rb') as file:
            fdata = file.read()
            
            # Parse SND file
            sound: SampledSound = snd_to_sampled(fdata)
            
            # Get cast file data
            castData = {}
            with open(os.path.join(sys.argv[1], 'data.json'), mode='r',
                      encoding='utf-8') as jsfile:
                text = jsfile.read()
                castData = json.loads(text)
                
            # Add sound file information
            castData['sampleSize'] = sound.bits_per_sample
            castData['sampleRate'] = sound.sample_rate
            castData['channelCount'] = sound.num_channels
              
            # Write CAST data to JSON file
            with open(os.path.join(sys.argv[1], 'data.json'), 'wb') as jsfile:
                jsfile.write(json.dumps(castData, indent=4, sort_keys=True)
                             .encode('utf-8'))
            
            # Generate wave file
            wav_name = "%s.%s"%(os.path.basename(snd_file)[:-5], 'wav')
            mp3_name = "%s.%s"%(os.path.basename(snd_file)[:-5], 'mp3')
            
            wavef = wave.open(os.path.join(sys.argv[1], wav_name),'w')
            wavef.setnchannels(sound.num_channels)
            wavef.setsampwidth(int(sound.bits_per_sample/8)) 
            wavef.setframerate(sound.sample_rate)
            
            wavef.writeframesraw(sound.samples)
            wavef.writeframes(b'')
            wavef.close()
            

            # Transform it to mp3            
            in_name = os.path.join(sys.argv[1], wav_name)
            out_name = os.path.join(sys.argv[1], mp3_name)
            
            os.system('ffmpeg -y -i %s -acodec libmp3lame %s'%(
                in_name, # input file
                out_name #output file
            )) 
        
if __name__ == '__main__':
    main()
