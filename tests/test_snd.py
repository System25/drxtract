# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for SND extraction
#

import unittest
import os
import wave
from parameterized import parameterized

from drxtract.snd import snd_to_sampled, SampledSound


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'snd'))
    

    @parameterized.expand([
        ['bounce'],
        ['bumpuf'],
        
    ])
    def test_exe(self, dir_name: str):
        snd_file = os.path.join(dir_name, dir_name + ".snd_")
        wav_file = os.path.join(dir_name, dir_name + ".wav")

        with open(snd_file, mode='rb') as file:
            snd_data = file.read()
            # Parser SND file
            sampledSound: SampledSound = snd_to_sampled(snd_data)
            
            wf = wave.open(wav_file, 'rb')
            
            self.assertEqual(wf.getnchannels(), sampledSound.num_channels)
            self.assertEqual(wf.getsampwidth(), sampledSound.bits_per_sample/8)
            self.assertEqual(wf.getframerate(), sampledSound.sample_rate)
            
            data = wf.readframes(wf.getnframes())
            wf.close()        
            self.assertEqual(data, sampledSound.samples)

